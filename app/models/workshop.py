from app.utils.database import get_collection
from bson import ObjectId

class WorkshopModel:

    def __init__(self):
        self.collection = get_collection("workshops")

    def all(self):
        return list(self.collection.find())

    def create(self, data):
        return self.collection.insert_one(data)

    def get(self, workshop_id):
        return self.collection.find_one(
            {"_id": ObjectId(workshop_id)}
        )

    def update(self, workshop_id, data):
        return self.collection.update_one(
            {"_id": ObjectId(workshop_id)},
            {"$set": data}
        )

    def delete(self, workshop_id):
        return self.collection.delete_one(
            {"_id": ObjectId(workshop_id)}
        )