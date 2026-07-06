from app.utils.database import get_collection
from bson import ObjectId

class ExpertModel:

    def __init__(self):
        self.collection = get_collection("experts")

    def get_all(self):
        return list(self.collection.find())

    def get(self, expert_id):
        return self.collection.find_one({"_id": ObjectId(expert_id)})

    def create(self, data):
        return self.collection.insert_one(data)

    def update(self, expert_id, data):
        return self.collection.update_one(
            {"_id": ObjectId(expert_id)},
            {"$set": data}
        )

    def delete(self, expert_id):
        return self.collection.delete_one({"_id": ObjectId(expert_id)})