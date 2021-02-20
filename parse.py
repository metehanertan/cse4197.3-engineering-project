import codecs
import os
import re
from bs4 import BeautifulSoup

def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif (c == '"' or c == "'") and tag:
            quote = not quote
        elif not tag:
            out = out + c

    return out

def getSehir(konusmaciTam): #konuşmacı stringinden şehri veya "devamla"yı çıkaran fonksiyon
    if konusmaciTam=="BAŞKAN ":
        return ""
    sehir=konusmaciTam[konusmaciTam.find("(")+1:konusmaciTam.find(")")]
    return sehir

def getKonusmaci(konusmaciTam): #konuşmacı stringinden milletvekili adını veya "BAŞKAN"ı
    if konusmaciTam=="BAŞKAN ":
            return "BAŞKAN"
    konusmaci=konusmaciTam[:konusmaciTam.find("(")]
    konusmaci=konusmaci.strip()
    return konusmaci
    
def getKonusma(oturum): #oturumu alıp içinden konuşmaları çıkaran fonksiyon
    pattern=['[A-ZĞÜŞIÖÇİ\s*]{2,}\([a-zğüşıöçA-ZĞÜŞIÖÇİ]+\)','BAŞKAN ']
    regex = re.compile(r'('+'|'.join(pattern)+r')')
    oturum=oturum[oturum.find("BAŞKAN "):] #konuşmaları daha doğru alabilmek için başkanın oturumu açmasını bekliyoruz
    x = regex.findall(oturum) #bütün konuşmacı ve konuşmacılar, çift indexler konuşmacı, tek indexler konuşma
    konusmalar=regex.split(oturum)
    konusmalar.pop(0) #boş index
    konusmaSayısı=int(len(konusmalar)/2)
    
    for i in range(konusmaSayısı): #Bütün konuşmalar; konuşmacı,şehir, konuşma sırası şeklinde
        konusmaciTam = konusmalar[i*2]
        konusma = konusmalar[(i*2)+1]
        konusmaciSehir = getSehir(konusmaciTam)
        konusmaci = getKonusmaci(konusmaciTam)
        print(konusmaci,konusmaciSehir,i) #bu değişkenler database yüklenmeli
    

def getOturum(tutanak):
    return

tutanakAdi="https__wwwtbmmgovtr_tutanak_donem27_yil4_ham_b01001hhtm.html" 
f = open(tutanakAdi, "r",encoding="utf8")

tutanak = f.read()
tutanak = remove_html_markup(tutanak)
tutanak = tutanak.replace(u'\xa0', u'')
tutanak = tutanak.replace("\n\n", " ")
tutanak = tutanak.replace("  ", " ")
tutanakSon=len(tutanak)

oturumNumaras=["BİRİNCİ","İKİNCİ","ÜÇÜNCÜ","DÖRDÜNCÜ","BEŞİNCİ",
              "ALTINCI","YEDİNCİ","SEKİZİNCİ","DOKUZUNCU","ONUNCU",
              "ON BİRİNCİ","ON İKİNCİ","ON ÜÇÜNCÜ","ON DÖRDÜNCÜ","ON BEŞİNCİ",
              "ON ALTINCI","ON YEDİNCİ","ON SEKİZİNCİ","ON DOKUZUNCU","YİRMİNCİ",
              "YİRMİ BİRİNCİ","YİRMİ İKİNCİ","YİRMİ ÜÇÜNCÜ","YİRMİ DÖRDÜNCÜ","YİRMİ BEŞİNCİ",
              "YİRMİ ALTINCI","YİRMİ YEDİNCİ","YİRMİ SEKİZİNCİ","YİRMİ DOKUZUNCU","OTUZUNCU"]

oturumlar=[] # bütün oturumları tutacağımız değişken, bu değişken ayrılma işlemi sonrası tek tek db yüklenmeli
oturumBaşlangıçIndex=0
oturumSonIndex=0
oturumIndex=0

# !!!!!!! OTURUM 0 yok ama aşağıdaki loop BİRİNCİ OTURUM
# başlayana kadar olan kısımı alıp append ediyor yani
# 0. indeximiz oturumlar öncesi kısım için ayrılmış //bu kısım bazı tutanaklarda var
# ve keza her oturumumuz kendi indexinde 1==>BİRİNCİ gibi !!!!!!!

for oturumNumara in oturumNumaras: #oturumlara ayırıyoruz
    
    oturumBaşlangıç = oturumNumara + " OTURUM Açılma Saati:"
    oturumSonIndex=tutanak.find(oturumBaşlangıç)
    if oturumSonIndex == -1: #eğer oturum yoksa son oturum demek
        oturumSonIndex=tutanakSon
        oturum=tutanak[oturumBaşlangıçIndex:oturumSonIndex]
        oturumlar.append(oturum)
        break

    oturum=tutanak[oturumBaşlangıçIndex:oturumSonIndex]
    oturumlar.append(oturum)
    oturumBaşlangıçIndex=oturumSonIndex
    oturumIndex += 1

getKonusma(oturumlar[1]) #örnek bir oturum

    

