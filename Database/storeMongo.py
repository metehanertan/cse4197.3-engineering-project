import pymongo

# Create Database
db_name = "TBMMDatabase"
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
db_list = my_client.list_database_names()
database = my_client[db_name]
tutanak = database["tutanak"]
oturum = database["oturum"]
konuşma = database["konuşma"]
print(database.name, " created.")

tutanaklar = []
tutanaklar.append(({"TutanakID": "1"}, {"Tutanak": "2"}))
#tutanak.insert_many(tutanaklar)

oturumlar = []
oturumlar.append(({"OturumID": "7"}, {"Oturum": "8"}))
#oturum.insert_many(oturumlar)

konuşmalar = []
konuşmalar.append(({"KonuşmaID": "10"}, {"Konuşma": "11"}))
#konuşma.insert_many(konuşmalar)

tutanak.delete_many({})
oturum.delete_many({})
konuşma.delete_many({})
