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

        workshop={

            "title":data.get("title"),

            "description":data.get("description"),

            "district":data.get("district"),

            "mode":data.get("mode"),

            "location":data.get("location"),

            "date":data.get("date"),

            "time":data.get("time"),

            "capacity":int(data.get("capacity",0)),

            "registered":0,

            "resource":"",

            "created_at":datetime.utcnow()

        }

        return self.collection.insert_one(workshop)

    def register(self,id):

        return self.collection.update_one(

            {"_id":ObjectId(id)},

            {"$inc":{"registered":1}}

        )