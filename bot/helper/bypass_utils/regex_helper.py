import re
from bot.helper.bypass_utils.bypass_helper import shortner_type_one_dict, shortner_type_two_dict
    
def is_shortener_type_one_link(url):
    for (key,value) in shortner_type_one_dict.items():
        if bool(re.match(FR"{value[0]}", url)):
            return True

def is_shortener_type_two_link(url):
    for (key,value) in shortner_type_two_dict.items():
        if bool(re.match(FR"{value[0]}", url)):
            return True

def is_bitly_link(url: str):
    url = re.match(r'https?://(bit\.ly\/)\S+', url)
    return bool(url)

def is_gtlinks_link(url: str):
    url = re.match(r'https?://(gtlinks\.me\/)\S+', url)
    return bool(url)

def is_gplink_link(url: str):
    url = re.match(r'https?://(gplinks\.co\/)\S+', url)
    return bool(url)
    
def is_ouo_link(url: str):
    url = re.match(r'https?://(ouo\.(io|press)\/)\S+', url)
    return bool(url)
    
def is_pkin_link(url: str):
    url = re.match(r'https?://(pkin\.me/)\S+', url)
    return bool(url)
    
def is_shareus_link(url: str):
    url = re.match(r'https?://(shareus\.in\/\?i=)\S+', url)
    return bool(url)
    
def is_shortest_link(url: str):
    url = re.match(r'https?://(shorte|festyy|gestyy|corneey|destyy|ceesty)\.(st|com)\/\S+', url)
    return bool(url)
    
def is_shortly_link(url: str):
    url = re.match(r'https://(www\.shortly\.xyz\/)\S+', url)
    return bool(url)
    
def is_sirigan_link(url: str):
    url = re.match(r'https?://(sirigan\.my\.id\/)\S+', url)
    return bool(url)
    
def is_thinfi_link(url: str):
    url = re.match(r'https?://(thinfi\.com\/)\S+', url)
    return bool(url)
    
def is_tinyurl_link(url: str):
    url = re.match(r'https?://(tinyurl\.com\/)\S+', url)
    return bool(url)
    
def is_try2link_link(url: str):
    url = re.match(r'https?://(try2link\.com\/)\S+', url)
    return bool(url)

def is_linkvertise_link(url: str):
    url = re.match(r'https?://(linkvertise\.com/)\S+', url)
    return bool(url)

def is_adfly_link(url: str):
    url = re.match(r'https?://(adf\.ly/)\S+', url)
    return bool(url)
