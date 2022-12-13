import datetime
import pickle
import os
import io
import json
import sys
import argparse
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']


link = sys.argv[1]

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    cred = None

    pickle_file = f'token.pickle'

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

def filedownload(fileid):
  fileid = fileid.replace("/"," ").split()
  fileid= max(fileid, key=len)  
  request = service.files().get_media(fileId=fileid)
  requestt = service.files().get(fileId=fileid, supportsTeamDrives=True)
  response = requestt.execute()
  name = response['name']

  fh = io.BytesIO()
  downloader = MediaIoBaseDownload(fd=fh, request=request)

  done =False
  while not done:
    status, done = downloader.next_chunk()

  fh.seek(0)  
  with open(os.path.join(name), 'wb') as f:
    f.write(fh.read())
    f.close()
  return name 

#path = filedownload("https://drive.google.com/file/d/13t7Prruo0K4hVl1G3_8-ZhWSl25jNCU9/view?usp=share_link")
path = filedownload(link)
print(path)