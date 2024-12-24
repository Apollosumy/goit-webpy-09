import json
from pymongo import MongoClient


client = MongoClient("mongodb+srv://sumyultras88:Ghbdtn_123456@cluster0.4nl1k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


db = client["quotes_db"]
quotes_collection = db["quotes"]
authors_collection = db["authors"]

def load_json_to_mongodb():
  
    with open("quotes.json", "r", encoding="utf-8") as quotes_file:
        quotes_data = json.load(quotes_file)

    with open("authors.json", "r", encoding="utf-8") as authors_file:
        authors_data = json.load(authors_file)

   
    quotes_collection.delete_many({})
    authors_collection.delete_many({})

 
  
    quotes_collection.insert_many(quotes_data)
    
    authors_collection.insert_many(authors_data)

 

if __name__ == "__main__":
    load_json_to_mongodb()
