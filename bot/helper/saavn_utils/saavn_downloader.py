import requests
import json
import os
import sys
import base64
import urllib.request
import html
from mutagen.mp4 import MP4, MP4Cover
from PIL import Image
from pySmartDL import SmartDL
from pyDes import *

from bot import DOWNLOAD_DIR
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException

client = requests.Session()

def addtags(title, filename, json_data):
    audio = MP4(filename)
    audio['\xa9nam'] = html.unescape(json_data["title"])
    audio['\xa9ART'] = html.unescape(json_data["more_info"]["music"])
    audio['\xa9alb'] = html.unescape(json_data["more_info"]["album"])
    cover_url = json_data["image"].rsplit("-", maxsplit=1)[0] + '-500x500.jpg'
    fd = urllib.request.urlopen(cover_url)
    temp_dir = f"{DOWNLOAD_DIR}{title}temp.jpg"
    thumb_dir = f"{DOWNLOAD_DIR}{title}.jpg"
    with open(temp_dir, "wb") as f: f.write(fd.read())
    Image.open(temp_dir).convert("RGB").save(thumb_dir, "JPEG")
    os.remove(temp_dir)
    cover = MP4Cover(fd.read(), getattr(MP4Cover, 'FORMAT_PNG' if cover_url.endswith('png') else 'FORMAT_JPEG'))
    fd.close()
    audio['covr'] = [cover]
    audio.save()

def decrypt_url(url):
    des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0",pad=None, padmode=PAD_PKCS5)
    enc_url = base64.b64decode(url.strip())
    dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
    dec_url = dec_url.replace("_96.mp4", "_320.mp4")
    return dec_url

def get_SongID(JioSawanURL):
    token = JioSawanURL.split("/")[-1]
    input_url = f"https://www.jiosaavn.com/api.php?__call=webapi.get&token={token}&type=song&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0"
    response = client.get(input_url)
    songID = response.json()["songs"][0]["id"]
    return songID

def get_title_and_URL(URL):
    id = get_SongID(URL)
    payload = {
        '_marker': '0',
        'cc': '',
        'pids': id,
        'ctx': 'android',
        'network_operator': '',
        'v': '224',
        'app_version': '6.8.2',
        'build': 'Pro',
        'api_version': '4',
        'network_type': 'WIFI',
        '_format': 'json',
        '__call': 'song.getDetails',
        'manufacturer': 'Samsung',
        'readable_version': '6.8.2',
        'network_subtype': '',
        'model': 'Samsung Galaxy S10'
    }
    response = client.post("https://www.jiosaavn.com/api.php", data=payload).text # POST request
    response = json.loads(response)
    title = response[id]["title"]
    e_url = response[id]["more_info"]['encrypted_media_url']
    d_url = decrypt_url(e_url)
    return d_url, title, response[id]


def download(input_url):
    urlandtitle = get_title_and_URL(input_url)
    url = urlandtitle[0]
    title = html.unescape(urlandtitle[1])
    jsonData = urlandtitle[2]
    location = f"{DOWNLOAD_DIR}{title}.m4a"
    thumb = f"{DOWNLOAD_DIR}{title}.jpg"
    try:
        obj = SmartDL(url, location, progress_bar=False)
        obj.start()
        addtags(title, location, jsonData)
    except:
        raise DirectDownloadLinkException("ERROR: Something went wrong while Downloading track!")
    return thumb, location
