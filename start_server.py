#!/usr/bin/python
# -*- encoding: utf-8 -*-

from bottle import *
from urllib import request as urlrllibrequest
import json

'''
    Na spodnji povezavi so menjalni tecaji z interneta. 
    V nadaljevanju naloge bo funkcija obiskala in posodobila menjalne tecaje s tistimi iz interneta.
'''

menjalni_tecaji_api_url ="https://api.exchangeratesapi.io/latest"
privzeta_vrednost = 10.0
privzeta_valuta = "EUR"
#Zacetne valute, kasneje jih posodobimo s tistimi iz interneta
valute = [("EUR",1), ("USD",1.13), ("GBP", 0.9), ("CHF", 1.06), ("JPY", 120.83), ("INR", 84.93), ("PLN", 4.47), ("CNY",7.91), ("CAD",1.54), ("BRL", 6.02), ("RUB",79.93),  ("BAM",1.96), ("HRK", 7,52)]


def posodobi_valute():
    r = urlrllibrequest.urlopen(url = menjalni_tecaji_api_url) 
    loadeddata = json.loads(r.read())
    valuteDict = loadeddata.get("rates").items()
    seznamValut =  [(k, v) for k, v in loadeddata.get("rates").items()]
    #Pridobljene valute so bazirane na EUR, vendar ta ni pridobljen preko API-ja, zato ga dodamo
    seznamValut.append(['EUR', 1])
    #Posodobimo valute za vse uporabnike!
    global valute
    valute = seznamValut

'''
    Pomozna funkcija, ki vzame vhodno vrednost in valute z
    njihovimi menjalnimi tecaji ter vrne seznam izhodnih vrednosti
    z njihovimi valutami.
    Recimo
    15, [(1,EUR), (1.2,USD), (2, SIT)] vrne:
    [(15,EUR), (15.30, USD), (30, SIT)]
'''
def pretvori_vhodno_vrednost_v_druge_valute(vhodna_vrednost, valute):
    vrednosti_v_drugih_valutah = []
    for valuta in valute:
        ime_valute = valuta[0]
        menjalni_tecaj = valuta[1]
        vrednost_v_drugi_valuti = menjalni_tecaj * vhodna_vrednost 
        vrednosti_v_drugih_valutah.append([ime_valute, menjalni_tecaj, vrednost_v_drugi_valuti])
    return vrednosti_v_drugih_valutah

'''
    Funkcija vzame vhodno vrednost in izbrano valuto (Recimo: 10 EUR)
    in vrne seznam, vhodne valute pretvorjene v vse valute.
    (Recimo [(10,EUR), (1.23, USD),..])
'''
def pretvori_vhodno_vrednost_in_valuto_v_ostale_valute(vhodna_vrednost, izbrana_valuta):
    valute_z_novimi_menjalnimi_tecaji = pretvori_menjalne_tecaje_na_bazo_izbrane_valute(izbrana_valuta)
    return pretvori_vhodno_vrednost_v_druge_valute(vhodna_vrednost, valute_z_novimi_menjalnimi_tecaji)

'''
    Funkcija vrne adaptiran seznam valut z menjalnimi tecaji
    na bazo izbrane valute.
    To je:
    [("EUR",2), ("CHZ",4), ("SER", 8)]
    na bazo "CHZ"
    [("EUR",0.5), ("CHZ",1), ("SER", 2)]
'''
def pretvori_menjalne_tecaje_na_bazo_izbrane_valute(izbrana_valuta):
    valute_s_spremenjeno_bazo = []
    for valuta in valute:
        if valuta[0] ==  izbrana_valuta:
            menjalni_tecaj_izbrane_valute = valuta[1]
    for valuta in valute:
        #spremenjen_menjalni_tecaj = valuta[1] / menjalni_tecaj_izbrane_valute
        #valute_s_spremenjeno_bazo.append((valuta[0], spremenjen_menjalni_tecaj) 
        valute_s_spremenjeno_bazo.append((valuta[0],valuta[1]/menjalni_tecaj_izbrane_valute))
    return valute_s_spremenjeno_bazo


################## SPLETNA STRAN
@route('/',  method="GET")
def index():
     return privzeta_stran()

@route ('/', method="POST")
def index():
    try:
        #ce uporabnik v okno vpise kaj cudnega, se nastavi privzeta vrednost
        return uporabnikova_stran()
    except Exception as e:
        print(e)
        return  privzeta_stran()
    
@route ('/posodobi', method="GET")
def posodobi():
    posodobi_valute()
    return  privzeta_stran()

def privzeta_stran():
        return template('glavna.html', valute=pretvori_vhodno_vrednost_in_valuto_v_ostale_valute(privzeta_vrednost, privzeta_valuta),  izbrana_vrednost = privzeta_vrednost, izbrana_valuta = privzeta_valuta)

def uporabnikova_stran():
        vrednost = float(request.forms.get("vrednost"))
        izbrana_valuta = request.forms.get("izbrana_valuta")
        return template('glavna.html', valute=pretvori_vhodno_vrednost_in_valuto_v_ostale_valute(vrednost, izbrana_valuta), izbrana_vrednost = vrednost, izbrana_valuta = izbrana_valuta)
    

######################################################################
# Posodobimo valute
posodobi_valute()
# Zazenemo server
run(host='localhost', port=8080)


