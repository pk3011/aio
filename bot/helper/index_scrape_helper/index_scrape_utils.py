import requests
import base64 
import json
import urllib

from bot.helper.ext_utils.exceptions import DirectDownloadLinkException

next_page = False
next_page_token = "" 

  
 
def authorization_token(username, password):
  user_pass = f"{username}:{password}"
  token ="Basic "+ base64.b64encode(user_pass.encode()).decode()
  return token

    
def decrypt(string): 
     return base64.b64decode(string[::-1][24:-20]).decode('utf-8')  

  
def func(payload_input, url, username, password): 
    global next_page 
    global next_page_token
    
    url = url + "/" if  url[-1] != '/' else url
         
    try: headers = {"authorization":authorization_token(username,password)}
    except: raise DirectDownloadLinkException("Username/Password combination is wrong.")
 
    encrypted_response = requests.post(url, data=payload_input, headers=headers)
    if encrypted_response.status_code == 401: raise DirectDownloadLinkException("Username/Password combination is wrong.")
   
    try: decrypted_response = json.loads(decrypt(encrypted_response.text))
    except: raise DirectDownloadLinkException("Something went wrong. Check Index Link in your browser\nMake sure your link contains files.")
       
    page_token = decrypted_response["nextPageToken"] 
    if page_token == None: 
        next_page = False 
    else: 
        next_page = True 
        next_page_token = page_token 
   
     
    result = ""
   
    if list(decrypted_response.get("data").keys())[0] == "error": pass
    else :
      file_length = len(decrypted_response["data"]["files"])
      for i, _ in enumerate(range(file_length)):
        
         files_type   = decrypted_response["data"]["files"][i]["mimeType"] 
         files_name   = decrypted_response["data"]["files"][i]["name"] 
       
 
         if files_type == "application/vnd.google-apps.folder": pass
         else:
             direct_download_link = url + urllib.parse.quote(files_name)
             result += f"<a href='{direct_download_link}'>{files_name}</a>\n\n"
      return result
         
 
def main(url, username="none", password="none"):
 x = 0
 payload = {"page_token":next_page_token, "page_index": x}
 page = func(payload, url, username, password)
 while next_page == True:
  payload = {"page_token":next_page_token, "page_index": x}
  page += func(payload, url, username, password)
  x += 1
 return page
