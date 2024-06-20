from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import re
import requests
import string


# Metindeki gereksiz kelimeleri, boşlukları, noktalama işaretlerini temizler
def temizle_metin(text):
    text = text.replace('Facebook', '')
    additional_chars = '·'
    # Noktalama işaretlerini ve boşlukları kaldır
    translator = str.maketrans('', '', string.punctuation + string.whitespace + additional_chars)
    return text.translate(translator)


# Metinden Telefon numarası ara

def ara_telefon_numarası(text):
    phone_pattern1 = re.compile(r'(?<!\d)0?\d{10}(?!\d)|(?<!\d)905\d{9}(?!\d)|05\d{9}')
    # phone_pattern2 = re.compile(r'(?<!\d)0?(322|416|272|472|382|358|312|242|478|466|256|266|378|488|458|228|426|434|374|248|224|286|376|364|258|412|380|284|424|446|442|222|342|454|438|456|326|476|246|324|212|216|232|370|338|474|366|352|372|354|226|432|276|428|462|356|282|486|414|346|368|484|362|264|464|328|452|388|384|436|252|482|236|422|274|332|262|344|348|385|288|318)\d{7}')
    liste_phone1 = phone_pattern1.findall(text)
    liste_phone = [l[-10:] for l in liste_phone1]
    return list(set(liste_phone))


def extract_number_from_url(url):
    # URL desenini belirliyoruz
    pattern = r'/(\d+)/$'

    # Verilen deseni URL'de arıyoruz
    match = re.search(pattern, url)

    if match:
        # Eşleşen grup (numara) varsa döndürüyoruz
        return match.group(1)
    else:
        return None
