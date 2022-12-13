import json
import requests 
from bs4 import BeautifulSoup as bs
from urllib.parse import quote

from bot.helper.ext_utils.exceptions import DirectDownloadLinkException

proxy = {'https': 'http://qlpnvaem:tuqexrxbkpsh@185.199.228.220:7300'}


def amzn(query):
    input = quote(query)
    req = requests.get(f"https://www.primevideo.com/search/ref=atv_sr_sug_7?phrase={input}&ie=UTF8", proxies=proxy).text
    data = bs(req, "html.parser")

    image_raw_link = data.find("div", class_="_1Opa2_ dvui-packshot av-grid-packshot").a.img["src"]
    image_id = image_raw_link.split(".")[2].split("/")[4]
    image = f"https://m.media-amazon.com/images/S/pv-target-images/{image_id}.jpg"

    title = data.find("div", class_="_1Opa2_ dvui-packshot av-grid-packshot").a["aria-label"]

    year = json.loads(data.find_all("script", type="text/template")[2].text)['props']['results']['items'][0]['year']['text']

    dir = {
        'image': image,
        'title': title,
        'year': year
    }
    return dir


def nf(query):
    headers = {'referrer': 'http://unogs.com', 'referer': 'https://unogs.com', 'Host': 'unogs.com'}

    params = {'query': query}

    IDres = requests.get('https://unogs.com/api/search', params=params, headers=headers).text

    IDres_in_json = json.loads(IDres)

    ID = IDres_in_json["results"][0]["nfid"]
    title = IDres_in_json["results"][0]["title"]
    year = IDres_in_json["results"][0]["year"]

    IMGres = requests.get(f"https://unogs.com/api/title/bgimages?netflixid={ID}").text

    IMGres_in_json = json.loads(IMGres)

    IMG = IMGres_in_json["bo1280x448"][0]["url"]
    
    dir = {
        'image': IMG,
        'title': title,
        'year': year
    }
    return dir


def bd(query):
    params = {
        'quicksearch': '1',
        'quicksearch_country': 'US',
        'quicksearch_keyword': query,
        'section': 'bluraymovies',
    }

    data = requests.get('https://www.blu-ray.com/search/', params=params, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}).text

    res = bs(data, 'html.parser').find("td", width="728").find_all('div', style="display: inline-block")

    if len(res) >= 3:
        i = 3
    elif len(res) == 2:
        i = 2
    elif len(res) == 1:
        i = 1

    try:
        lst = ""
        for x in range(i):
            title = res[x].a['title']
            img = res[x].a.img['src'].replace('medium', 'front')
            lst += f"{title}:\n{img}\n" + "\n"
        lst = lst.strip()
    except:
        raise DirectDownloadLinkException("Somthing Went Wrong")
        
#    dir = {
#        'image': img,
#        'title': title,
#    }
    return lst


def imdbLinkInput(x):
    if x[-1] == "/":
        id = x[0:-1].split("/")[-1]
    else:
        id = x.split("/")[-1]

    return id

def inputWithYear(x):
    year = x.split(" (")[-1].split(")")[0]
    title = x.split(" (")[0]
    dir = {'year':year, 'title':title}

    return dir

def imdb(query):
    if "(" in query:
        title = inputWithYear(query)["title"]
        year = inputWithYear(query)["year"]
        id = None
    elif "imdb.com" in query:
        id = imdbLinkInput(query)
        title = None
        year = None
    else:
        title = query
        year = None
        id = None

    params = {
        't': title,
        'y': year,
        'i': id,
        'apikey': '1438ed03',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }

    res = requests.get('https://www.omdbapi.com/', params=params, headers=headers).json()
    posBaseUrl = "https://m.media-amazon.com/images/M/"
    try:
        posID = res['Poster'].split("/", -1)[-1].split(".")[0]
        movieName = res["Title"]
        movieYear = res["Year"]
        imdbRating = res["imdbRating"]
        imdbVotes = res["imdbVotes"]
        
        url = f"{posBaseUrl}{posID}.jpg"
        title = f"{movieName} ({movieYear})"
        rating = f"{imdbRating}/10 ({imdbVotes})"
    except:
        raise DirectDownloadLinkException("Please Check The Spelling of Input or This Movie/Series is not available on IMDb")
 
    dir = {
        'image': url,
        'title': title,
        'rating': rating
    }
    return dir
