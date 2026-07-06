from pymongo import MongoClient

MONGO_URI = "mongodb+srv://720723110025_db_user:720723110025@cluster0.k67dodz.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client["crop_advisory_db"]

collections = db.list_collection_names()

print("Collections:", collections)

for collection in collections:
    result = db[collection].delete_many({})
    print(f"{collection}: {result.deleted_count} documents deleted")

print("\n✅ Database cleared successfully!")