import datetime
import pickle
import os
import json
import sys
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import magic
import argparse

parser = argparse.ArgumentParser(description=f">>> Stream Extractor <<<")
parser.add_argument("--path", dest="path", help="Enter The File/Folder Path")
args = parser.parse_args()

#VARS
userpath = args.path

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
fid = "102uQxwrUmhV31g3WAFhlqH9m3R1gk_k0"
flag = "NOTDONE"
statement = "NOTDONE"

def get_mime_type(file_path):
    m = magic.from_file(file_path, mime=True)
    return m

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    #print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    #print(SCOPES)

    cred = None

    pickle_file = f'token.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        #print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES) 

#print(dir(service))

def createfolder(folderpath , cf):
 tests = [folderpath]
 for test in tests:
    file_metadata = {
        'name': test,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [cf]
    }
 h = service.files().create(body=file_metadata, supportsAllDrives=True).execute()
 id = h['id']
 flag = "DONE"
 return id

def upload(path, folder): 
 global flag , statement    
 if os.path.isdir(path):
    base = os.path.basename(path)
    folder_id = createfolder(base, folder)
    if flag=="NOTDONE": 
     statement = "https://drive.google.com/drive/folders/" + folder_id
     flag = 'DONE'
    filenames = os.listdir(path)
    for filename in os.listdir(path):  
      file = os.path.join(path, filename)
      upload(file, folder_id)
 else:   
    filenames = [path]
    ff = folder
    for filename in filenames:
      file = filename
    mime = get_mime_type(file)
    file_metadata = {
        'name': os.path.basename(filename),
        'mimeType': mime,
        'parents': [ff]
    }
    media = MediaFileUpload(file, mimetype=mime, resumable=True,
                                     chunksize=50 * 1024 * 1024)
    done = service.files().create(body=file_metadata, media_body=media, fields='id', supportsAllDrives=True).execute()
    finallink = done['id']
    if flag=="NOTDONE": 
     statement = "https://drive.google.com/uc?id="+ finallink + "&export=download"
     flag = 'DONE'

def gdrive(object):
 global fid  
 upload(object, fid)
 return statement

gdrivelink = gdrive(userpath)
#gdrivelink = gdrive("test")
print(gdrivelink)
