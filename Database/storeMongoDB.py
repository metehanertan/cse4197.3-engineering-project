from pymongo import MongoClient

client = MongoClient()
db = client.test_database  # use a database called "test_database"
collection = db.files   # and inside that DB, a collection called "files"

f = open('test_file_name.txt')  # open a file
text = f.read()    # read the entire contents, should be UTF-8 text

# build a document to be inserted
text_file_doc = {"file_name": "test_file_name.txt", "contents" : text }
# insert the contents into the "file" collection
collection.insert(text_file_doc)