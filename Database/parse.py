import codecs
import os
import sys
import pymongo
import re

from Database.storeMongo import *
from Database.storeMySql import *


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


def getSehir(konusmaciTam):  # konuşmacı stringinden şehri veya "devamla"yı çıkaran fonksiyon
    if konusmaciTam == "BAŞKAN ":
        return ""
    sehir = konusmaciTam[konusmaciTam.find("(") + 1:konusmaciTam.find(")")]
    return sehir


def getKonusmaci(konusmaciTam):  # konuşmacı stringinden milletvekili adını veya "BAŞKAN"ı
    if konusmaciTam == "BAŞKAN ":
        return "BAŞKAN"
    konusmaci = konusmaciTam[:konusmaciTam.find("(")]
    konusmaci = konusmaci.strip()
    return konusmaci


def getKonusma(oturum, OturumID, KonusmaID):  # oturumu alıp içinden konuşmaları çıkaran fonksiyon
    pattern = ['[A-ZĞÜŞIÖÇİ\s*]{2,}\([a-zğüşıöçA-ZĞÜŞIÖÇİ]+\)', 'BAŞKAN ']
    regex = re.compile(r'(' + '|'.join(pattern) + r')')
    oturum = oturum[
             oturum.find("BAŞKAN "):]  # konuşmaları daha doğru alabilmek için başkanın oturumu açmasını bekliyoruz
    x = regex.findall(oturum)  # bütün konuşmacı ve konuşmacılar, çift indexler konuşmacı, tek indexler konuşma
    konusmalar = regex.split(oturum)
    konusmalar.pop(0)  # boş index
    konusmaSayısı = int(len(konusmalar) / 2)

    for konusmaSırası in range(konusmaSayısı):  # Bütün konuşmalar; konuşmacı,şehir, konuşma sırası şeklinde
        konusmaciTam = konusmalar[konusmaSırası * 2]
        konusma = konusmalar[(konusmaSırası * 2) + 1]
        konusmaciSehir = getSehir(konusmaciTam)
        konusmaci = getKonusmaci(konusmaciTam)

        KonusmaID += 1
        # MongoDB store Konusma
        mStoreKonusma(KonusmaT, KonusmaID, konusma)
        # MySql store Konusma
        storeKonusma(mySqlDB, OturumID, 0, konusmaSırası, KonusmaID)

    return OturumID, KonusmaID


def getOturum(tutanak):
    return


def getAllTutanaks(path):
    print("Reading all Tutanaks in: ", path)
    tutanakNames = os.listdir(path)
    for tutanakName in tutanakNames:
        if tutanakName.endswith(".html"):
            file = path + tutanakName
            if os.path.getsize(file) != 0:
                tutanakArr = []
                tutanakArr.append(tutanakName)
                f = open(file, "r", encoding="utf8")
                tutanak = f.read()
                tutanak = remove_html_markup(tutanak)
                tutanak = tutanak.replace(u'\xa0', u'')
                tutanak = tutanak.replace("\n\n", " ")
                tutanak = tutanak.replace("  ", " ")
                tutanakArr.append(tutanak)
                tutanaklar.append(tutanakArr)
    print("All Tutanaks read.")
    return tutanaklar


def sendTutanakToDB(tutanak, TutanakID, OturumID, KonusmaID):
    tutanakSon = len(tutanak)

    oturumNumaras = ["BİRİNCİ", "İKİNCİ", "ÜÇÜNCÜ", "DÖRDÜNCÜ", "BEŞİNCİ",
                     "ALTINCI", "YEDİNCİ", "SEKİZİNCİ", "DOKUZUNCU", "ONUNCU",
                     "ON BİRİNCİ", "ON İKİNCİ", "ON ÜÇÜNCÜ", "ON DÖRDÜNCÜ", "ON BEŞİNCİ",
                     "ON ALTINCI", "ON YEDİNCİ", "ON SEKİZİNCİ", "ON DOKUZUNCU", "YİRMİNCİ",
                     "YİRMİ BİRİNCİ", "YİRMİ İKİNCİ", "YİRMİ ÜÇÜNCÜ", "YİRMİ DÖRDÜNCÜ", "YİRMİ BEŞİNCİ",
                     "YİRMİ ALTINCI", "YİRMİ YEDİNCİ", "YİRMİ SEKİZİNCİ", "YİRMİ DOKUZUNCU", "OTUZUNCU"]
    oturumlar = []  # bütün oturumları tutacağımız değişken, bu değişken ayrılma işlemi sonrası tek tek db yüklenmeli
    oturumBaşlangıçIndex = 0
    oturumSonIndex = 0
    oturumIndex = 0

    # !!!!!!! OTURUM 0 yok ama aşağıdaki loop BİRİNCİ OTURUM
    # başlayana kadar olan kısımı alıp append ediyor yani
    # 0. indeximiz oturumlar öncesi kısım için ayrılmış //bu kısım bazı tutanaklarda var
    # ve keza her oturumumuz kendi indexinde 1==>BİRİNCİ gibi !!!!!!!

    for oturumNumara in oturumNumaras:  # oturumlara ayırıyoruz

        oturumBaşlangıç = oturumNumara + " OTURUM Açılma Saati:"
        oturumSonIndex = tutanak.find(oturumBaşlangıç)
        if oturumSonIndex == -1:  # eğer oturum yoksa son oturum demek
            oturumSonIndex = tutanakSon
            oturum = tutanak[oturumBaşlangıçIndex:oturumSonIndex]
            oturumlar.append(oturum)
            break

        oturum = tutanak[oturumBaşlangıçIndex:oturumSonIndex]
        oturumlar.append(oturum)
        oturumBaşlangıçIndex = oturumSonIndex
        oturumIndex += 1

    for oturumNo in range(1, len(oturumlar)):
        OturumID += 1
        # MongoDB store Oturum
        mStoreOturum(OturumT, OturumID, oturumlar[oturumNo])
        # MySql store Oturum
        storeOturum(mySqlDB, TutanakID, oturumNo, OturumID)
        OturumID, KonusmaID = getKonusma(oturumlar[oturumNo], OturumID, KonusmaID)
    return TutanakID, OturumID, KonusmaID

# Creating databases
db_name = "testdatabase"

# MongoDB
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_client.drop_database(db_name)
mongoDb, TutanakT, OturumT, KonusmaT = mCreateDB(my_client, db_name)

# MySql
deleteDB(db_name)
mySqlDB = createDB(db_name)
storeMilletvekili(mySqlDB, "BASKAN", "BASKENT", 0)

# Reading all Tutanak htmls
path = "tutanak\\"
tutanaklar = []
tutanaklar = getAllTutanaks(path)

# Storing all Tutanak
print("Storing all Tutanaks in DBs.")
TutanakID = lastTutanakID(TutanakT)
OturumID = lastOturumID(OturumT)
KonusmaID = lastKonusmaID(KonusmaT)
for tutanak in tutanaklar:
    TutanakID += 1
    # MongoDB store Tutanak
    mStoreTutanak(TutanakT, TutanakID, tutanak[1])
    # MySql store Tutanak
    urlArr = tutanak[0].split('_')
    donem = urlArr[4].split('m')[1]
    donemYil = urlArr[5].split('l')[1]
    birlesimNo = 0
    storeTutanak(mySqlDB, donem, donemYil, "Tarih", birlesimNo, tutanak[0], TutanakID)
    # Oturumlara parçalama
    TutanakID, OturumID, KonusmaID = sendTutanakToDB(tutanak[1], TutanakID, OturumID, KonusmaID)
    if TutanakID == 3:
        break
print("All Tutanaks Stored.")
#mPrintAllDB(TutanakT, OturumT, KonusmaT)
#printAllDB(mySqlDB)

print("MySql Oturumlar:")
printTable(mySqlDB, "Oturum")
#print("MySql Konusmalar:")
#printTable(mySqlDB, "Konusma")
print("MySql Tutanaklar:")
printTable(mySqlDB, "Tutanak")