from flask import Flask, render_template, request, redirect, url_for, session
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import hashlib
import time
import Elastik_Motoru
from get_profil import extract_number_from_url , ara_telefon_numarası ,temizle_metin
import psutil
import re
def check_memory_usage():
    memory_info = psutil.virtual_memory()
    print(f"Memory usage: {memory_info.percent}%")

app = Flask(__name__, template_folder="templates")
app.secret_key = 'supersecretkey'

USER_CREDENTIALS = {
    'username': 'admin',
    'password': hashlib.sha256('F.user.41'.encode()).hexdigest()
}

@app.route('/', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if username == USER_CREDENTIALS['username'] and hashed_password == USER_CREDENTIALS['password']:
            session['logged_in'] = True
            session['username'] = ''
            session['password'] = ''
            return redirect(url_for('search'))
        else:
            error_message = 'Kullanıcı adı veya şifre hatalı.'

    session.pop('logged_in', None)
    return render_template('login.html', error_message=error_message)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session['username'] = ''
    session['password'] = ''
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        Link = request.form['Link']
        key = request.form.get('Anahtar', '').strip()
        members, group_name = fscrap(Link,key)

        return render_template('results.html', members=members, count=len(members), group_name=group_name )
    return render_template('search.html')

def fscrap(Link, key):
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

        driver.get(Link)
        time.sleep(4)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        group_name_tag = soup.find('a', {
            'class': 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1xlr1w8'})
        if group_name_tag:
            group_name = group_name_tag.text.strip()
        kisi_sayisi_text = soup.find('span',class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 x1j85h84").text
        sayı = re.findall(r'\d+\.\d+', kisi_sayisi_text)
        # kişi sayısı 8000 üzerinde ise filtrleme gerçelişir
        if sayı and float(sayı[0]) > 8:
            print("İkincil filtrleme aktif")
            wait = WebDriverWait(driver, 20)
            input_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Bir üyeyi bul']"))
            )
            input_element.send_keys(key)
            input_element.send_keys(Keys.RETURN)
        
        scroll_pause_time = 1
        scroll_attempts = 0
        max_attempts = 20
        last_height = driver.execute_script("return document.body.scrollHeight")
        print("Sayfa kaydırma aktif")
        sayac=0
        while True:
            sayac +=1
            print(f"Kaydırma Sayisi: {sayac}")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                scroll_attempts += 1
            else:
                scroll_attempts = 0

            if scroll_attempts >= max_attempts:
                break
            last_height = new_height
        print("Sayfa kaydırma bitti")

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        members = soup.find_all('a', {'class': 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u x1s688f'})
        soup = ""
        for member in members:
            name = member.text.strip()
            profile_link = member['href']
            liste_kisi.append({'name': name, 'link': f"https://www.facebook.com/profile.php?id={extract_number_from_url(profile_link)}"})

        print(f"Toplam kişi uzunluğu:: {len(liste_kisi)}")
        if key:
            liste_kisi = Elastik_Motoru.elastik(liste_kisi, key)
        print(f"Bulunan kişi uzunluğu: {len(liste_kisi)}")
        for kisi in liste_kisi:
            driver.get(kisi['link'])
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)        
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            page_text = soup.get_text()
            page_text = temizle_metin(page_text)
            phone_numbers = ara_telefon_numarası(page_text)

            if phone_numbers:
                kisi['phone'] = phone_numbers
                final_liste_kisi.append(kisi)
        soup=""
    except Exception as e:
        print("Hata fscrap:", e)
    finally:
        driver.quit()
    return final_liste_kisi, group_name

@app.before_request
def before_request():
    if request.endpoint == 'search' and 'logged_in' not in session:
        return redirect(url_for('login'))

@app.after_request
def after_request(response):
    if response.status_code == 200 and request.endpoint == 'search' and 'logged_in' in session:
        session['username'] = ''
        session['password'] = ''
    return response


if __name__ == '__main__':
    app.run(debug=True)