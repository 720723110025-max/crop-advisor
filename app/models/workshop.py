from app.utils.database import get_collection
from bson import ObjectId

class WorkshopModel:

    def __init__(self):
        self.workshops = get_collection("workshops")
        self.registrations = get_collection("workshop_registrations")

    def get_all(self):
        return list(self.workshops.find())

    def get(self, workshop_id):
        return self.workshops.find_one({"_id": ObjectId(workshop_id)})

    def create(self, data):
        return self.workshops.insert_one(data)

    def update(self, workshop_id, data):
        return self.workshops.update_one(
            {"_id": ObjectId(workshop_id)},
            {"$set": data}
        )

    def delete(self, workshop_id):
        return self.workshops.delete_one(
            {"_id": ObjectId(workshop_id)}
        )

    def register(self, data):
        return self.registrations.insert_one(data)

    def registrations(self):
        return list(self.registrations.find())