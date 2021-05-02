import pymongo


def mConnectDB(my_client, db_name):
    database = my_client[db_name]
    Tutanak = database.get_collection("Tutanak")
    Oturum = database.get_collection("Oturum")
    Konusma = database.get_collection("Konusma")
    return database, Tutanak, Oturum, Konusma


def mCreateDB(my_client, db_name):
    db_list = my_client.list_database_names()
    if not db_name in db_list:
        database = my_client[db_name]
        Tutanak = database.create_collection("Tutanak")
        Oturum = database.create_collection("Oturum")
        Konusma = database.create_collection("Konusma")
        return database, Tutanak, Oturum, Konusma


def mCreateAnalysisDB(my_client, db_name):
        database = my_client[db_name]
        Lemma = database.create_collection("Lemma")
        NER = database.create_collection("NER")
        Topic = database.create_collection("Topic")
        return database, Lemma, NER, Topic


def mConnectAnalysisDB(my_client, db_name):
    database = my_client[db_name]
    Lemma = database.get_collection("Lemma")
    NER = database.get_collection("NER")
    Topic = database.get_collection("Topic")
    return database, Lemma, NER, Topic


def mStoreTutanak(Tutanak, TutanakID, Tutanaktext):
    mydict = {"TutanakID": TutanakID, "Tutanaktext": Tutanaktext}
    Tutanak.insert_one(mydict)


def mStoreOturum(Oturum, OturumID, Oturumtext):
    mydict = {"OturumID": OturumID, "Oturumtext": Oturumtext}
    Oturum.insert_one(mydict)


def mStoreKonusma(Konusma, KonusmaID, Konusmatext):
    mydict = {"KonusmaID": KonusmaID, "Konusmatext": Konusmatext}
    Konusma.insert_one(mydict)


def mStoreLemma(Lemma, KonusmaID, Lemmas):
    mydict = {"KonusmaID": KonusmaID, "Lemmas": Lemmas}
    Lemma.insert_one(mydict)


def mStoreNER(NER, KonusmaID, NERs):
    mydict = {"KonusmaID": KonusmaID, "NERs": NERs}
    NER.insert_one(mydict)


def mStoreTopic(Topic, KonusmaID, Topics, Sentiments):
    mydict = {"KonusmaID": KonusmaID, "Topics": Topics, "Sentiments": Sentiments}
    Topic.insert_one(mydict)


def mPrintAllDB(Tutanak, Oturum, Konusma):
    print("Tutanak:")
    mPrintTable(Tutanak)
    print("Oturum:")
    mPrintTable(Oturum)
    print("Konusma:")
    mPrintTable(Konusma)


def mPrintTable(table):
    for data in table.find({}):
        print(data, end=", ")
    print()


def lastTutanakID(Tutanak):
    biggest = 0
    for data in Tutanak.find({}):
        if data.get("TutanakID") > biggest:
            biggest = data.get("TutanakID")
    return biggest


def lastOturumID(Oturum):
    biggest = 0
    for data in Oturum.find({}):
        if data.get("OturumID") > biggest:
            biggest = data.get("OturumID")
    return biggest


def lastKonusmaID(Konusma):
    biggest = 0
    for data in Konusma.find({}):
        if data.get("KonusmaID") > biggest:
            biggest = data.get("KonusmaID")
    return biggest


"""
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
database, Tutanak, Oturum, Konusma = mConnectDB(my_client, "TBMMDatabase")
mPrintAllDB(Tutanak, Oturum, Konusma)
my_client.drop_database("TBMMDatabase")
database, Tutanak, Oturum, Konusma = mCreateDB(my_client, "TBMMDatabase")
mStoreTutanak(Tutanak, 1, "Tutanaktxt")
mStoreOturum(Oturum, 1, "Oturumtxt")
mStoreKonusma(Konusma, 1, "Konusmatxt")
mPrintAllDB(Tutanak, Oturum, Konusma)
print(lastTutanakID(Tutanak))
print(lastOturumID(Oturum))
print(lastKonusmaID(Konusma))
"""
