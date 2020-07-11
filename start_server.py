#!/usr/bin/python
# -*- encoding: utf-8 -*-

from bottle import *

privzeta_vrednost = 10
privzeta_valuta = "EUR"

#seznam parov (ime_valute,univerzalni_menjalni_tecaj)
valute = [("EUR",1), ("CHZ",1.5)]

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
        valute_s_spremenjeno_bazo.append((valuta[0],valuta[1]/menjalni_tecaj_izbrane_valute))
    return valute_s_spremenjeno_bazo


##################SPLETNA STRAN
@route('/',  method="GET")
def index():
     return privzeta_stran()

@route ('/', method="POST")
def index():
    try:
        #ce uporabnik v okno vpise kaj cudnega, se nastavi privzeta vrednost
        vrednost = float(request.forms.get("vrednost"))
        izbrana_valuta = request.forms.get("izbrana_valuta")
        return template('glavna.html', valute=pretvori_vhodno_vrednost_in_valuto_v_ostale_valute(vrednost, izbrana_valuta), izbrana_vrednost = vrednost, izbrana_valuta = izbrana_valuta)
    except:
        return  privzeta_stran()

def privzeta_stran():
        return template('glavna.html', valute=pretvori_vhodno_vrednost_in_valuto_v_ostale_valute(privzeta_vrednost, privzeta_valuta),  izbrana_vrednost = privzeta_vrednost, izbrana_valuta = privzeta_valuta)
    
######################################################################
# Zazenemo server
run(host='localhost', port=8080)


