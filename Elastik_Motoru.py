from fuzzywuzzy import fuzz
from googletrans import Translator

def elastik(liste_isim,key):
    print("Elastik motoru aktif")
    elektrik_ile_ilgili_isimler = []

    esik_degeri = 70

    translator = Translator()
    translation = translator.translate(key, src='tr', dest='en')
    anahtar_kelime_ingilizce = translation.text


    anahtar_kelimeler = [key, anahtar_kelime_ingilizce]

    for isim in liste_isim:
        di = isim['name']
        for anahtar_kelime in anahtar_kelimeler:
            eslesme_orani = fuzz.partial_ratio(anahtar_kelime.lower(), di.lower())
            if eslesme_orani >= esik_degeri:
                elektrik_ile_ilgili_isimler.append(isim)
                break

    return elektrik_ile_ilgili_isimler