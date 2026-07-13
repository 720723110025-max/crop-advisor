from app.utils.database import get_collection
from bson import ObjectId
from datetime import datetime


class ExpertModel:

    def __init__(self):
        self.collection = get_collection("experts")

    def get_all(self):
        return list(self.collection.find())

    def get(self, expert_id):
        return self.collection.find_one(
            {"_id": ObjectId(expert_id)}
        )

    def create(self, data):

        expert = {

            "name": data.get("name"),

            "username": data.get("username"),

            "password": data.get("password"),

            "district": data.get("district"),

            "specialization": data.get("specialization"),

            "languages": data.get("languages"),

            "experience": int(data.get("experience", 0)),

            "phone": data.get("phone"),

            "email": data.get("email"),

            "rating": 5.0,

            "availability": "Available",

            "photo": data.get("photo", ""),

            "created_at": datetime.utcnow()

        }

        return self.collection.insert_one(expert)

    def update(self, expert_id, data):

        return self.collection.update_one(

            {"_id": ObjectId(expert_id)},

            {"$set": data}

        )

    def delete(self, expert_id):

        return self.collection.delete_one(

            {"_id": ObjectId(expert_id)}

        )