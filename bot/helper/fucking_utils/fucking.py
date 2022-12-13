import os
import requests,re,time
import json as js
from aiohttp import ClientSession
from asyncio import run,sleep,create_task,gather
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from base64 import b64encode, b64decode
from datetime import datetime
from playwright.sync_api import Page, sync_playwright
from tenacity import retry

from bot.helper.bypass_utils.regex_helper import *
from bot.helper.bypass_utils.bypass_helper import *
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException

# ------------------------------------------------------------
# Cloudfare Bypass

@retry
def ensure_html_fetch(page: Page) -> str:
    return page.content()
    
    
def detect_challenge(html: str) -> bool:
    challenge_uri_paths = (
        "/cdn-cgi/challenge-platform/h/[bg]/orchestrate/managed/v1",
        "/cdn-cgi/challenge-platform/h/[bg]/orchestrate/jsch/v1",
    )

    return any(re.search(uri_path, html) for uri_path in challenge_uri_paths)


def solve_challenge(page: Page) -> None:
    verify_button_pattern = re.compile("Verify (I am|you are) (not a bot|(a )?human)")
    verify_button = page.get_by_role("button", name=verify_button_pattern)
    spinner = page.locator("#challenge-spinner")

    while detect_challenge(ensure_html_fetch(page)):
        if spinner.is_visible():
            spinner.wait_for(state="hidden")

        challenge_stage = page.query_selector("div#challenge-stage")
        captcha_box = page.query_selector("div.hcaptcha-box")

        if verify_button.is_visible():
            verify_button.click()
            challenge_stage.wait_for_element_state("hidden")
        elif captcha_box is not None:
            page.reload()


def cloudfare(url):
    with sync_playwright() as playwright:
        browser = playwright.webkit.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/605.1.15 (KHTML, like Gecko)")
        ms_timeout = int(25000)
        context.set_default_timeout(ms_timeout)
        page = context.new_page()
        page.goto(url)
        solve_challenge(page)
        cookies = page.context.cookies()
        res = page.content()
        cookie_value = "".join(
            cookie["value"] for cookie in cookies if cookie["name"] == "cf_clearance"
        )
    return res, cookie_value

# -------------------------------------------

def gtl(url):
    list = []
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/605.1.15 (KHTML, like Gecko)'}
    try:
        if os.path.isfile("cf_gtl.txt"):
            with open("cf_gtl.txt", "r") as c:
                cf_value = c.read()
            cookies = {'cf_clearance': cf_value}
            res_content = requests.get(url, headers=headers, cookies=cookies).text
            if "<title>Just a moment...</title>" in res_content:
                res_content, cf_value = cloudfare(url)
                soup = bs(res_content, "html.parser").find('div', class_="entry-content").findAll("a")
                for i in soup:
                    try:
                        list.append(i['href'])
                    except KeyError:
                        pass
                open('cf_gtl.txt', 'w').write(cf_value)
            else:
                soup = bs(res_content, "html.parser").find('div', class_="entry-content").findAll("a")
                for i in soup:
                    try:
                        list.append(i['href'])
                    except KeyError:
                        pass
        else:
            res_content, cf_value = cloudfare(url)
            soup = bs(res_content, "html.parser").find('div', class_="entry-content").findAll("a")
            for i in soup:
                try:
                    list.append(i['href'])
                except KeyError:
                    pass
            open('cf_gtl.txt', 'w').write(cf_value)
    except:
        raise DirectDownloadLinkException("ERROR: Something went wrong while bypassing Get-to.Link.")
    return list


# -------------------------------------------

def psa(input):
    n = 8
    now = datetime.now()
    d = now.strftime("%d%m%y")
    coo = {'LstVstD':b64encode(str(d).encode()).decode(), 'VstCnt':b64encode(str(n).encode()).decode()}

    req = requests.post(input, headers={'user-agent': 'Mozilla/5.0 (Linux; Android 11; M2101K7BI Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'x-requested-with': 'idm.internet.download.manager.plus', 'referer': 'https://psa.pm/', 'accept-language':'en,en-US;q=0.9'}, cookies=coo).text

#    if f"ouo" not in req:
#        req = requests.post(input, headers={'user-agent': 'Mozilla/5.0 (Linux; Android 11; M2101K7BI Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'x-requested-with': 'idm.internet.download.manager.plus', 'referer': 'https://psa.pm/', 'accept-language': 'en,en-US;q=0.9'}).text

    data = bs(req, "html.parser")
    link = data.find("form")["action"]

    try:
        getlink = ouo_bypass(link)
    except:
        raise DirectDownloadLinkException("ERROR: Something went wrong, Try again!")
    return getlink

# -------------------------------------------

def pmz(url):
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/605.1.15 (KHTML, like Gecko)'}
    try:
        if os.path.isfile("cf_pmz.txt"):
            with open("cf_pmz.txt", "r") as c:
                cf_value = c.read()
            cookies = {'cf_clearance': cf_value}
            r = requests.get(url, headers=headers, cookies=cookies).text
            if "<title>Just a moment...</title>" in r:
                res, cf_value = cloudfare(url)
                gtlink = re.findall(r"https?:\/\/gtlinks\.[a-z]+\/[_\w]+", res)[0]
                final_link = gtlinks_bypass(gtlink)
                open('cf_pmz.txt', 'w').write(cf_value)
                return final_link
            elif "gtlinks" in r:
                gtlink = re.findall(r"https?:\/\/gtlinks\.[a-z]+\/[_\w]+", r)[0]
                final_link = gtlinks_bypass(gtlink)
                return final_link
            else:
                raise DirectDownloadLinkException("ERROR: Something went wrong, Try again!")
        else:
            res, cf_value = cloudfare(url)
            gtlink = re.findall(r"https?:\/\/gtlinks\.[a-z]+\/[_\w]+", res)[0]
            final_link = gtlinks_bypass(gtlink)
            open('cf_pmz.txt', 'w').write(cf_value)
            return final_link
    except:
        raise DirectDownloadLinkException("ERROR: Something went wrong, Try again!")

# -------------------------------------------

def toon(url):
    try:
        r_link = requests.get(url).url
        final_link = shortner_type_one_bypass_handler(r_link)
    except:
        raise DirectDownloadLinkException("ERROR: Something went wrong, Try again!")
    return final_link

# -------------------------------------------

def vega(url):
    turl=requests.get(url).url
    agent="Mozilla/5.0 (Linux; Android 10; Redmi 8A Dual) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36"
    resp = requests.get(turl,headers={'user-agent':agent},allow_redirects=1).text
    data=js.loads(re.search('item\s=\s(\S+)\;',resp).group(1))
    data['new'] = False
    options=js.loads(re.search('options\s=\s(\S+)\;',                resp).group(1))
    data['action'] = options['soralink_z']
    purl=options['soralink_ajaxurl']
    #time.sleep(10)
    resp = requests.post(purl,headers={'user-agent':agent,'referer':data['post']},data=data,allow_redirects=False)
    return resp.headers.get('location')

# -------------------------------------------

class sora:
      def __init__(self,url,client,sleep_time):
          self.client = client
          self.url = url
          self.sleep_time = sleep_time

      def data(data):
          data={i.get('name'): i.get('value') for i in data}
          return data

      async def sora_parser(self):
          async with self.client as rq:
                  url = self.url
                  sleep_time = self.sleep_time
                  h = {
                       'user-agent': "Mozilla/5.0 (Linux; Android 10; Redmi 8A Dual) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36",
                       'origin': 'null',
                      }
                  #cook = await rq.get(self.url)
                  #cook = cook.headers.get('set-cookie').split(";",1)[0].split('=',1)
                  c = {
                      #cook[0]: cook[1]
                      }
                  #print(c)
                  req_1 = await rq.get(url,headers=h,cookies=c)
                  parse_1=bs( await req_1.read(),'html.parser').find_all('input')
                  data_1=sora.data(parse_1)
                  #print(data_1)
                  req_2 = await rq.post(url.split('?',1)[0],headers=h,cookies=c,data=data_1)
                  f = await req_2.read()
                  #print(f.decode())
                  #exit()
                  parse_2=bs(await req_2.read(),'html.parser').find('form',{'id':"landing"})
                  data_2=sora.data(parse_2.find_all('input'))
                  #print(data_2)
                  req_3 = await rq.post(parse_2.get('action'),headers=h,cookies=c,data=data_2)
                  #print(parse_2.get('action'))
                  #url.rsplit('/?',1)[0]+
                  req_3 = await req_3.read()
                  #find post requests. for final result
                  #print(req_3.decode())
                  #exit()
                  re_1=re.search(r"var[\s]+[\w_]+\=([\w_]+)\[([\w\\\'_]+)?([\w_]+\(\'0x\d\d\'\))?\]\([\w_]+\(\'0x\d\d\'\)\,\'[\w \\\']+'\)",req_3.decode()).group(1)
                  #print(re_1)
                  re_2=re.search(f'{re_1}\=\S+\;',req_3.decode()).group(0).split('=',1)[1].replace(';','')
                  #now the last brain teaser. for decoding string
                  puzzle=[i for i in re_2.replace("SJhf89ue8fj489f", "==").replace("nmf90ewurw8jf", "=")]
                  puzzle.reverse()
                  puzzle=b64decode(''.join(puzzle)).decode()
                  j=js.loads(puzzle)
                  list_1=[i for i in j]
                  #print(j)
                  data_3={
                          'c': None,
                          'soramode': 'default',
                          list_1[0]: j[list_1[0]]
                         }
                  url_1=f'{j[list_1[1]]}/?{list_1[0]}={j[list_1[2]]}'
                  data_4=js.loads(js.dumps(data_3))
                  #ok now very final step one last post request and boom
                  await sleep(sleep_time)
                  req_4 = await rq.post(url_1,headers=h,cookies=c,data=data_4,allow_redirects=False)
                  req_4 = req_4.headers.get('location')
                  return req_4


async def sora_main(url,sleep_time):
    async with ClientSession() as client:
         return await sora(url,client,sleep_time).sora_parser()

# -------------------------------------------

class shortner:

      def __init__(self,url,client,domain,regex,config,cookies={}):
          self.regex  = regex
          self.domain = domain
          self.client = client
          self.cookie = cookies
          self.url,self.redirects,self.cookie_mode,self.sleep_time = config(url,domain,regex).values()
          self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'

      async def post_data(self,form):
          url=self.url
          form = bs(form,'html.parser').form
          soup=form.findAll('input')
          data = dict( (i.get('name'),i.get('value')) for i in soup)
          await sleep(self.sleep_time)
          #print(f'{self.regex.search(url)[1]}{form.get("action")}')
          #print(self.cookie)
          header={'user-agent': self.user_agent,'x-requested-with': 'XMLHttpRequest'}
          async with self.client.post(f'{self.regex.search(url)[1]}{form.get("action")}',headers=header,cookies=self.cookie[self.domain],data=data,allow_redirects=False) as resp:
                return await resp.json()

      async def set_cookie(self):
            if self.cookie_mode:
               async with self.client.get(self.url,headers={'user-agent':self.user_agent},allow_redirects=self.redirects) as resp:
                     resp=resp.headers.getall('set-cookie')
               cookie=dict(i.split(';',1)[0].split('=',1) for i in resp)
            else:
               cookie={}
            self.cookie[self.domain] = cookie
            return cookie

      async def shortner(self):
            if self.domain not in self.cookie.keys():
               cookie = await self.set_cookie()
            else:
               cookie = self.cookie[self.domain]
            #print(cookie,self.url)
            #print(self.user_agent)
            async with self.client.get(self.url,headers={'user-agent': self.user_agent,'referer': self.url},cookies=cookie,allow_redirects=self.redirects) as resp:
               return await resp.read()

def site_config(url,domain,regex,bool=False):
    url=regex.search(url)
    config = {
    'try2link.net': {
                     'method': f'{url.group(1)}/{url.group(3)}/?d={int(time.time()+300)}',
                     'redirects': 1,
                     'cookie': True,
                     'sleep': 7
                        },
    'go.rocklinks.net': {
                     'method': f'https://blog.disheye.com/{url[3]}',
                     'redirects': 1,
                     'cookie': True,
                     'sleep': 10

                        },
    'ser2.crazyblog.in': {
                      'method': f'https://ser3.crazyblog.in/{url[3]}',
                      'redirects': 1,
                      'cookie': True,
                      'sleep': 12

                        },
    'open.crazyblog.in': {
                      'method': f'https://hr.vikashmewada.com/{url[3]}',
                      'redirects': 1,
                      'cookie': True,
                      'sleep': 10
                        },
    'link.short2url.in': {
	              'method': f'https://technemo.xyz/blog/{url[3]}',
	              'redirects': False,
	              'cookie': True,
                      'sleep': 10
                        },
    'ez4short.com': {
                  'method': f'https://ez4short.com/{url[3]}',
                  'redirects': False,
                  'cookie': False,
                  'sleep': 10

                        },
    'gplinks.co': {
                  'method': f'https://gplinks.co/{url[3]}', 
                  'redirects': True,
                  'cookie': True,
                  'sleep': 10

                        }
    }

    if bool:
       if domain in config.keys():
          return True
       else:
          return False
    else:
       return config[domain]


async def process(url,client):
       regex=re.compile(r'(https?:\/\/([^\/]+))\/([^\/]+)')
       isdomain=False
       while not isdomain:
          get = await client.get(url,headers={'referer': url})
          reg = re.search(r'var\surl\s\=\s\"(.*?)\"',str(await get.read()))
          if reg:
             reg=reg.group(1)
             #print(reg)
             domain=regex.search(str(reg)).group(2)
             isdomain=site_config(str(reg),domain,regex,True)
          await sleep(4)
       url=reg
       main=shortner(url,client,domain,regex,site_config)
       resp = await main.shortner()
       resp = await main.post_data(resp)
       return resp["url"]

async def ola_main(url):
  async with ClientSession() as client:
    tasks=[]
    for i in range(1):
        task = create_task(process(url,client))
        tasks.append(task)
        await sleep(1)
    return await gather(*tasks)

# -------------------------------------------

def pahe(url):
    lngee = run(sora_main(url,12))
    par_lngee=bs(requests.get(lngee,allow_redirects=False).content,'html.parser').find_all('script')
    link_lngee=b64decode(re.search(r'atob\(\'(.*?)\'\)',str(par_lngee[-3])).group(1)).decode()
    return link_lngee

# -------------------------------------------
