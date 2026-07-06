from bson import ObjectId
from app.utils.database import get_collection

class LandModel:

    def __init__(self):
        self.collection = get_collection("lands")

    def get_all(self):
        return list(self.collection.find())

    def get_by_id(self, land_id):
        return self.collection.find_one({"_id": ObjectId(land_id)})

    def create(self, data):
        return self.collection.insert_one(data)

    def update(self, land_id, data):
        return self.collection.update_one(
            {"_id": ObjectId(land_id)},
            {"$set": data}
        )

    def delete(self, land_id):
        return self.collection.delete_one(
            {"_id": ObjectId(land_id)}
        )