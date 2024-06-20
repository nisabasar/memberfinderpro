from fuzzywuzzy import fuzz
from googletrans import Translator


def elastik(liste_isim, keys):
    print("Elastik motoru aktif")
    elektrik_ile_ilgili_isimler = []

    esik_degeri = 70

    gorusen_cinsler = set()
    tekrarsiz_liste = []
    for l in liste_isim:
        # Eğer cins daha önce görülmediyse
        if l['link'] not in gorusen_cinsler:

            gorusen_cinsler.add(l['link'])

            tekrarsiz_liste.append(l)

    translator = Translator()
    anahtar_kelimeler = []
    for key in keys:
        translation = translator.translate(key, src='tr', dest='en')
        anahtar_kelimeler.append(translation.text)
        anahtar_kelimeler.append(key)
    print(f"Anahtar eklimeler: {anahtar_kelimeler}")
    for isim in tekrarsiz_liste:
        name = isim['name']
        for anahtar_kelime in anahtar_kelimeler:
            eslesme_orani = fuzz.partial_ratio(anahtar_kelime.lower(), name.lower())
            if eslesme_orani >= esik_degeri:
                elektrik_ile_ilgili_isimler.append(isim)
                break

    return elektrik_ile_ilgili_isimler