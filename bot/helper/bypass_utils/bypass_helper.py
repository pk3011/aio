import re
import requests 
import time 
from base64 import b64decode
from bs4 import BeautifulSoup 
from urllib.parse import urlparse, unquote
from playwright.sync_api import Page, sync_playwright
from tenacity import retry

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

#==============TYPE_1_DICT===============

shortner_type_one_dict =  {
     "https://tekcrypt.in/tek/": [
         "https?://(tekcrypt\.in/tek/)\S+",
         "https://tekcrypt.in/tek/",
         20
     ],
     "https://link.short2url.in/": [
         "https?://(link\.short2url\.in/)\S+",
         "https://technemo.xyz/blog/",
         10
     ],
     "https://go.rocklinks.net/": [
         "https?://(go\.rocklinks\.net/)\S+",
         "https://blog.disheye.com/",
         10
     ],
     "https://rocklinks.net/": [
         "https?://(rocklinks\.net/)\S+",
         "https://blog.disheye.com/",
         10
     ],
     "https://earn.moneykamalo.com/": [
         "https?://(earn\.moneykamalo\.com/)\S+",
         "https://go.moneykamalo.com//",
         5
     ],
     "https://m.easysky.in/": [
         "https?://(m\.easysky\.in/)\S+",
         "https://techy.veganab.co/",
         5
     ],
     "https://indianshortner.in/": [
         "https?://(indianshortner\.in/)\S+",
         "https://indianshortner.com/",
         5
     ],
     "https://open.crazyblog.in/": [
         "https?://(open\.crazyblog\.in/)\S+",
         "https://hr.vikashmewada.com/",
         7
     ],
     "https://link.tnvalue.in/": [
         "https?://(link\.tnvalue\.in/)\S+",
         "https://internet.webhostingtips.club/",
         5
     ],
     "https://shortingly.me/": [
         "https?://(shortingly\.me/)\S+",
         "https://go.techyjeeshan.xyz/",
         5
     ],
     "https://dulink.in/": [
         "https?://(dulink\.in/)\S+",
         "https://tekcrypt.in/tek/",
         20
     ],
     "https://bindaaslinks.com/": [
          "https?://(bindaaslinks\.com/)\S+",
          "https://www.techishant.in/blog/",
           5
     ],
     "https://pdiskshortener.com/": [
         "https?://(pdiskshortener\.com/)\S+",
         "https://pdiskshortener.com/",
         10
      ],
      "https://mdiskshortner.link/": [
          "https?://(mdiskshortner\.link/)\S+",
          "https://mdiskshortner.link/",
          15
      ],
      "http://go.earnl.xyz/": [
          "https?://(go\.earnl\.xyz/)\S+",
          "https://v.earnl.xyz/",
          5
      ],
      "https://g.rewayatcafe.com/": [
           "https?://(g\.rewayatcafe\.com/)\S+",
           "https://course.rewayatcafe.com/",
           7
      ],
      "https://ser2.crazyblog.in/": [
          "https?://(ser2\.crazyblog\.in/)\S+",
          "https://ser3.crazyblog.in/",
          12
      ],
      "https://za.uy/" : [
           "https?://(za\.uy/)\S+",
           "https://za.uy/",
           5
      ],
      "https://bitshorten.com/": [
          "https?://(bitshorten\.com/)\S+",
          "https://bitshorten.com/",
          21
      ],
      "http://rocklink.in/":[
         "http?://(rocklink\.in/)\S+",
         "https://rocklink.in/",
         6
      ]
 
 }

#==============TYPE_2_DICT===============

shortner_type_two_dict =  {
     "https://droplink.co/": [
         "https?://(droplink\.co/)\S+",
         "https://droplink.co/",
         "https://yoshare.net",
         4
     ],
     "https://tnlink.in/": [
         "https?://(tnlink\.in\/)\S+",
         "https://gadgets.usanewstoday.club/",
         "https://usanewstoday.club/",
         9
     ],
     "https://ez4short.com/":[
         "https?://(ez4short\.com/)\S+",
         "https://ez4short.com/",
         "https://techmody.io/",
         5
     ],
     "https://xpshort.com/": [
         "https?://(xpshort\.com/)\S+",
         "https://push.bdnewsx.com/",
         "https://veganho.co/",
         10
      ],
      "http://vearnl.in/": [
          "http?://(vearnl\.in/)\S+",
          "https://go.urlearn.xyz/",
          "https://v.modmakers.xyz/",
          5
     ],
     "https://adrinolinks.in/":[
         "https?://(adrinolinks\.in/)\S+",
         "https://adrinolinks.in/",
         "https://wikitraveltips.com/",
         5
     ],
     "https://techymozo.com/": [
         "https?://(techymozo\.com/)\S+",
         "https://push.bdnewsx.com/",
         "https://veganho.co/",
         8
     ],
     "https://linkbnao.com/":[
         "https?://(linkbnao\.com/)\S+",
         "https://go.linkbnao.com/",
         "https://doibihar.org/",
         2
     ],
     "https://linksxyz.in/":[
         "https?://(linksxyz\.in/)\S+",
         "https://blogshangrila.com/insurance/",
         "https://cypherroot.com/",
         13
      ],
      "https://short-jambo.com/" :[
           "https?://(short\-jambo\.com/)\S+",
           "https://short-jambo.com/",
           "https://aghtas.com/how-to-create-a-forex-trading-plan/",
           10
     ],
     "https://ads.droplink.co.in/": [
         "https?://(ads\.droplink\.co\.in/)\S+",
         'https://go.droplink.co.in/',
         "https://go.droplink.co.in/",
         5
     ],
     "https://linkpays.in/": [
         "https?://(linkpays\.in/)\S+",
         "https://m.techpoints.xyz//",
         "https://www.filmypoints.in/",
         10
     ],
     "https://pi-l.ink/" : [
         "https?://(pi\-l\.ink/)\S+",
         "https://go.pilinks.net/",
         "https://poketoonworld.com/",
         5
      ],
      "https://link.tnlink.in/": [
          "https?://(link\.tnlink\.in/)\S+",
          "https://gadgets.usanewstoday.club/",
          "https://usanewstoday.club/",
          8
      ],
       "https://earn4link.in/": [
         "https?://(earn4link\.in/)\S+",
         "https://m.open2get.in/",
         "https://ezeviral.com/2022/03/01/why-is-cloud-hosting-the-ideal-solution/",
         3
     ],
     "https://open2get.in/": [
         "https?://(open2get\.in/)\S+",
         "https://m.open2get.in/",
         "https://ezeviral.com/2022/03/01/why-is-cloud-hosting-the-ideal-solution/",
         3
     ],
     
     
     
}  

#==============SHORTENER_1===============

def shortner_type_one_bypass(shortner_url:str, domain: str, sleep_time:int)-> str:
    
    shortner_url = shortner_url[:-1] if shortner_url[-1] == '/' else shortner_url
    token = shortner_url.split("/")[-1]
    
    client = requests.Session()
    response = client.get(domain+token, headers={"referer":domain+token, 'cache-control': 'private, max-age=0, no-cache'})
    
    soup = BeautifulSoup(response.content, "html.parser")   
    inputs = soup.find(id="go-link").find_all(name="input")
    data = { input.get('name'): input.get('value') for input in inputs }
    
 
    time.sleep(sleep_time)
    headers={"x-requested-with": "XMLHttpRequest"}
    bypassed_url = client.post(domain+"links/go", data=data, headers=headers).json()["url"]
    return bypassed_url
    
 
def shortner_type_one_bypass_handler(shortner_url: str) ->  str:
    for (key,value) in shortner_type_one_dict.items():
        if bool(re.match(FR"{value[0]}", shortner_url)): return shortner_type_one_bypass(shortner_url=shortner_url, domain=value[1], sleep_time=value[2])
    return None

#==============SHORTENER_2===============

def shortner_type_two_bypass(shortner_url:str, domain:str, referer:str, sleep_time:int) -> str:
    shortner_url = shortner_url[:-1] if shortner_url[-1] == '/' else shortner_url
    token = shortner_url.split("/")[-1]
 
    
    client = requests.Session()
    response = client.get(domain+token, headers={"referer": referer, 'cache-control': 'private, max-age=0, no-cache'})
    
    soup = BeautifulSoup(response.content, "html.parser")   
    inputs = soup.find(id="go-link").find_all(name="input")
    data = { input.get('name'): input.get('value') for input in inputs }
    
    time.sleep(sleep_time)
    headers={"x-requested-with": "XMLHttpRequest"}
    bypassed_url = client.post(domain+"links/go", data=data, headers=headers).json()["url"]
    return bypassed_url 
        
 
def shortner_type_two_bypass_handler(shortner_url: str) ->  str:
    
    for (key,value) in shortner_type_two_dict.items():
        if bool(re.match(FR"{value[0]}", shortner_url)): return shortner_type_two_bypass(shortner_url=shortner_url, domain=value[1], referer=value[2],sleep_time=value[3])
    return None 

#==============BITLY===============

def bitly_bypass(bitly_url: str) -> str:
	response = requests.get(bitly_url).url
	return response

#==============GTLINKS===============

def gtlinks_bypass(url: str) -> str:
	
	url = url[:-1] if url[-1] == '/' else url
	url = requests.get(url).url
	token = url.split("=")[-1]
	
	domain = "https://go.theforyou.in/"

	client = requests.Session()
	response = client.get(domain+token, headers={"referer":domain+token, 'cache-control': 'private, max-age=0, no-cache'})
	soup = BeautifulSoup(response.content, "html.parser")
	
	inputs = soup.find(id="go-link").find_all(name="input")
	data = { input.get('name'): input.get('value') for input in inputs }
	
	time.sleep(5)
	headers={"x-requested-with": "XMLHttpRequest"}
	bypassed_url = client.post(domain+"links/go", data=data, headers=headers).json()["url"]
	return bypassed_url

#==============OUO+RECAPTCHAV3===============

def RecaptchaV3(ANCHOR_URL):
    url_base = 'https://www.google.com/recaptcha/'
    post_data = "v={}&reason=q&c={}&k={}&co={}"
    client = requests.Session()
    client.headers.update({
        'content-type': 'application/x-www-form-urlencoded'
    })
    matches = re.findall('([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0]
    url_base += matches[0]+'/'
    params = matches[1]
    res = client.get(url_base+'anchor', params=params)
    token = re.findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
    params = dict(pair.split('=') for pair in params.split('&'))
    post_data = post_data.format(params["v"], token, params["k"], params["co"])
    res = client.post(url_base+'reload', params=f'k={params["k"]}', data=post_data)
    answer = re.findall(r'"rresp","(.*?)"', res.text)[0]    
    return answer

ANCHOR_URL = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8uaW86NDQz&hl=en&v=1B_yv3CBEV10KtI2HJ6eEXhJ&size=invisible&cb=4xnsug1vufyr'

def ouo_bypass(url: str):
    client = requests.Session()
    tempurl = url.replace("ouo.press", "ouo.io")
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]
    
    res = client.get(tempurl, headers={'cache-control': 'private, max-age=0, no-cache'})
    next_url = f"{p.scheme}://{p.hostname}/go/{id}"

    for _ in range(2):
        if res.headers.get('Location'):
            break
            
        bs4 = BeautifulSoup(res.content, 'html.parser')
        inputs = bs4.form.findAll("input", {"name": re.compile(r"token$")})
        data = { input.get('name'): input.get('value') for input in inputs }
        
        ans = RecaptchaV3(ANCHOR_URL)
        data['x-token'] = ans        
        res = client.post(next_url, data=data, headers={'content-type': 'application/x-www-form-urlencoded'}, allow_redirects=False)
        next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"
    
    bypassed_link= str(res.headers.get("Location"))
    return bypassed_link

#==============PKIN===============
	
def pkin_bypass(url: str) -> str:
	
	url = url[:-1] if url[-1] == '/' else url
	token = url.split("/")[-1]
	
	domain = "https://go.paisakamalo.in/"
	referer = "https://techkeshri.com/"
	token = url.split("/")[-1]
	user_agent= "Mozilla/5.0 (Linux; Android 11; 2201116PI) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
	
	
	
	client = requests.Session()
	response = client.get(domain+token, headers={"referer": referer, "user-agent": user_agent})
	
	
	soup = BeautifulSoup(response.content, "html.parser")  
	
	inputs = soup.find(id="go-link").find_all(name="input")
	data = { input.get('name'): input.get('value') for input in inputs }
	
	time.sleep(3)
	headers={"x-requested-with": "XMLHttpRequest", "user-agent": user_agent}
	bypassed_url = client.post(domain+"links/go", data=data, headers=headers).json()["url"]
	return bypassed_url 

#==============SHAREUS===============
	
def shareus_bypass(shareus_url: str) -> str:
	
	token = shareus_url.split("=")[-1]
	domain = "https://us-central1-my-apps-server.cloudfunctions.net/r?shortid="
		
	bypassed_url = domain+token
	response = requests.get(bypassed_url).text
	return response

#==============SHORTE.ST===============
	
def shortest_bypass(url: str) -> str:
  
    parsed_url = urlparse(url)
  
    client = requests.Session()
    resp = client.get(url, headers={'referer': url})
    session_id = re.findall('''sessionId(?:\s+)?:(?:\s+)?['|"](.*?)['|"]''', resp.text)[0]
    final_url = f"{parsed_url.scheme}://{parsed_url.netloc}/shortest-url/end-adsession"
    params = {
        'adSessionId': session_id,
        'callback': '_'
    }
    
    time.sleep(5)
    response = client.get(final_url, params=params, headers={'referer': url})
    dest_url = re.findall('"(.*?)"', response.text)[1].replace('\/','/')
    
    return dest_url

#==============SHORTLY===============

def shortly_bypass(shortly_url: str) -> str:
	
	shortly_url= shortly_url[:-1] if shortly_url[-1] == '/' else shortly_url
	token = shortly_url.split("/")[-1]

	shortly_bypass_api = "https://www.shortly.xyz/getlink.php/"
	response = requests.post(shortly_bypass_api, data={"id":token}, headers={"referer":"https://www.shortly.xyz/link"}).text
	
	return response

#==============SIRIGAN===============
	
def sirigan_bypass(srigan_link: str) -> str:
    
    client = requests.Session()
    response = client.get(srigan_link)
    
    url = response.url.split('=', maxsplit=1)[-1]
    url = b64decode(url).decode('utf-8')

    while True:
        try: url = b64decode(url).decode('utf-8')
        except: break
    return url.split('url=')[-1]

#==============THINFI===============
    
def thinfi_bypass(thinfi_url: str) -> str :
	response = requests.get(thinfi_url)
	soup = BeautifulSoup(response.content,  "html.parser").p.a.get("href")
	return soup

#==============TINYURL===============

def tinyurl_bypass(tinyurl_url: str) -> str:
	response = requests.get(tinyurl_url).url
	return response

#==============TRY2LINK===============
	
def try2link_bypass(url):
	client = requests.Session()
	
	url = url[:-1] if url[-1] == '/' else url
	
	params = (('d', int(time.time()) + (60 * 4)),)
	r = client.get(url, params=params, headers= {'Referer': 'https://newforex.online/', 'cache-control': 'private, max-age=0, no-cache'})
	
	soup = BeautifulSoup(r.text, 'html.parser')
	inputs = soup.find(id="go-link").find_all(name="input")
	data = { input.get('name'): input.get('value') for input in inputs }	
	time.sleep(7)
	
	headers = {'Host': 'try2link.com', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://try2link.com', 'Referer': url}
	
	bypassed_url = client.post('https://try2link.com/links/go', headers=headers,data=data)
	return bypassed_url.json()["url"]

def linkvertise_bypass(url: str) -> str:
	
	linkvertise_bypass_api = "https://bypass.pm/bypass2?url="
	try: response = requests.get(linkvertise_bypass_api+url).json()["destination"]
	except: return None
	
	return response

def decrypt_url(code):
    a, b = '', ''
    for i in range(0, len(code)):
        if i % 2 == 0: a += code[i]
        else: b = code[i] + b

    key = list(a + b)
    i = 0

    while i < len(key):
        if key[i].isdigit():
            for j in range(i+1,len(key)):
                if key[j].isdigit():
                    u = int(key[i]) ^ int(key[j])
                    if u < 10: key[i] = str(u)
                    i = j					
                    break
        i+=1
    
    key = ''.join(key)
    decrypted = b64decode(key)[16:-16]

    return decrypted.decode('utf-8')


def adfly_bypass(url:str) -> str:
    res = requests.get(url).text
    
    out = {'error': False, 'src_url': url}
    
    try:
        ysmm = re.findall("ysmm\s+=\s+['|\"](.*?)['|\"]", res)[0]
    except:
        out['error'] = True
        return out
        
    url = decrypt_url(ysmm)

    if re.search(r'go\.php\?u\=', url):
        url = b64decode(re.sub(r'(.*?)u=', '', url)).decode()
    elif '&dest=' in url:
        url = unquote(re.sub(r'(.*?)dest=', '', url))       
    out['bypassed_url'] = url
    
    return out['bypassed_url'] 

#==============GPLINKS===============

def gplinks_bypass(url: str) -> str:
 res, cf_value = cloudfare(url)
 cookies = {'cf_clearance': cf_value}
 h = {'user-agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/605.1.15 (KHTML, like Gecko)'}

 url = url[:-1] if url[-1] == '/' else url
 token = url.split("/")[-1]
 
 domain ="https://gplinks.co/"
 referer = "https://mynewsmedia.co/"

 
 client = requests.Session()
 vid = client.get(url, cookies=cookies, headers=h, allow_redirects= False).headers["Location"].split("=")[-1]
 url = f"{url}/?{vid}"

 response = client.get(url, cookies=cookies, headers=h, allow_redirects=False)
 soup = BeautifulSoup(response.content, "html.parser")
 
 
 inputs = soup.find(id="go-link").find_all(name="input")
 data = { input.get('name'): input.get('value') for input in inputs }
 
 h2 = {'user-agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/605.1.15 (KHTML, like Gecko)', "x-requested-with": "XMLHttpRequest"}
 time.sleep(5)
 bypassed_url = client.post(domain+"links/go", data=data, headers=h2, cookies=cookies).json()["url"]
 return bypassed_url 
 
