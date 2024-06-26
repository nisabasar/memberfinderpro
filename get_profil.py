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



def temizle_metin(text):
    text = text.replace('Facebook', '')
    additional_chars = '·'

    translator = str.maketrans('', '', string.punctuation + string.whitespace + additional_chars)
    return text.translate(translator)




def ara_telefon_numarası(text):
    phone_pattern1 = re.compile(r'(?<!\d)0?\d{10}(?!\d)|(?<!\d)905\d{9}(?!\d)|05\d{9}')

    liste_phone1 = phone_pattern1.findall(text)
    liste_phone = [l[-10:] for l in liste_phone1]
    return list(set(liste_phone))


def extract_number_from_url(url):

    pattern = r'/(\d+)/$'

    match = re.search(pattern, url)

    if match:

        return match.group(1)
    else:
        return None
