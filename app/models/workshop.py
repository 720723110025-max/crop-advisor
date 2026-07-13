from app.utils.database import get_collection
from bson import ObjectId
from datetime import datetime


class WorkshopModel:

    def __init__(self):
        self.collection = get_collection("workshops")

    def get_all(self):
        return list(
            self.collection.find().sort(
                "date",1
            )
        )

    def get(self,id):
        return self.collection.find_one(
            {"_id":ObjectId(id)}
        )

    def create(self,data):

        workshop = {

                    "title": data.get("title"),

                    "description": data.get("description"),

                    "district": data.get("district"),

                    "mode": data.get("mode"),

                    "location": data.get("location"),

                    "date": data.get("date"),

                    "time": data.get("time"),

                    "capacity": int(data.get("capacity",0)),

                    "registered": 0,

                    "resource": data.get("resource"),

                    "speaker": data.get("speaker"),

                    "status": "Upcoming",

                    "feedback": [],

                    "attendance": [],

                    "created_at": datetime.utcnow()

                }

        return self.collection.insert_one(workshop)
    
    def update(self, id, data):

     return self.collection.update_one(

        {"_id": ObjectId(id)},

        {"$set": {

            "title": data.get("title"),

            "description": data.get("description"),

            "district": data.get("district"),

            "mode": data.get("mode"),

            "location": data.get("location"),

            "date": data.get("date"),

            "time": data.get("time"),

            "capacity": int(data.get("capacity", 0)),

            "speaker": data.get("speaker"),

            "resource": data.get("resource"),

            "status": data.get("status", "Upcoming"),

            "updated_at": datetime.utcnow()

        }}

    )

    def register(self,id):

        return self.collection.update_one(

            {"_id":ObjectId(id)},

            {"$inc":{"registered":1}}

        )
    def delete(self, id):

        return self.collection.delete_one(

        {"_id": ObjectId(id)}

       )
    
    def upload_resource(self, id, filename):

        return self.collection.update_one(

        {"_id": ObjectId(id)},

        {"$set": {

            "resource": filename

        }}

    )
