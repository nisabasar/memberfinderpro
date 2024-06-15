
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

"""

def deneme ():
    final_liste_kisi = []
    group_name=""
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--log-level=3")  # 3 seviyesi sadece hataları gösterir
    chrome_options.add_argument("--headless")  # Headless modunu etkinleştirin
    chrome_options.add_argument("--disable-gpu")  # GPU kullanımını devre dışı bırakın (bazı durumlarda gereklidir)
    chrome_options.add_argument("--window-size=1920x1080")  # Pencere boyutunu ayarlayın
    chrome_options.add_argument('--disable-extensions')
    prefs = {
        "profile.default_content_setting_values": {
            "images": 2,  # Görselleri yüklemeyi engeller
        }
    }
    chrome_options.add_experimental_option("prefs",prefs)
    service = Service('chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(45)  # Sayfa yükleme zaman aşımı süresini arttırma
    driver.set_script_timeout(45)     # Script çalıştırma zaman aşımı süresini arttırma
    
    driver.get('https://www.facebook.com/')
    time.sleep(2)

    liste_kisi = []

    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'email'))
        )
        password_input = driver.find_element(By.ID, 'pass')

        email_input.send_keys('fscraping5@gmail.com')
        password_input.send_keys('t.n.f.24')
        password_input.send_keys(Keys.RETURN)

        time.sleep(2)

        driver.get("https://www.facebook.com/groups/1572275056335456/members")
        time.sleep(4)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        group_name_tag = soup.find('a', {
            'class': 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1xlr1w8'})
        if group_name_tag:
            group_name = group_name_tag.text.strip()
        kisi_sayisi = soup.find('span',class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 x1j85h84").text
        sayılar = re.findall(r'\d+\.\d+', kisi_sayisi)
        print(f"grup name: {group_name} \nkişi sayısı: {sayılar}")
    except Exception as e:
        print("Hata fscrap:", e)
    finally:
        driver.close()
        driver.quit()
        return final_liste_kisi, group_name    
        
        # wait = WebDriverWait(driver, 20)
        # input_element = wait.until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Bir üyeyi bul']"))
        # )
        # input_element.send_keys(key)

        # # Girilen metni göndermek için ENTER tuşuna basma (isteğe bağlı)
        # input_element.send_keys(Keys.RETURN)

deneme( )
"""

# Metindeki gereksiz kelimeleri, boşlukları, noktalama işaretlerini temizler
def temizle_metin(text):

    text=text.replace('Facebook','')
    additional_chars = '·'
    # Noktalama işaretlerini ve boşlukları kaldır
    translator = str.maketrans('', '', string.punctuation + string.whitespace + additional_chars)
    return text.translate(translator)
# Metinden Telefon numarası ara

def ara_telefon_numarası(text):
    phone_pattern1 = re.compile(r'(?<!\d)0?\d{10}(?!\d)|(?<!\d)905\d{9}(?!\d)')
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
