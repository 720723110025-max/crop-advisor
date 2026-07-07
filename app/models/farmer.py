from app.utils.database import get_collection

class FarmerModel:

    def __init__(self):
        self.collection = get_collection("farmers")

    def get(self, user_id):
        return self.collection.find_one({"user_id": user_id})

    def create(self, data):
        return self.collection.insert_one(data)

    def update(self, user_id, data):
        return self.collection.update_one(
            {"user_id": user_id},
            {"$set": data}
        )