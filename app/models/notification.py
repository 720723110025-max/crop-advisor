from app.utils.database import get_collection
from datetime import datetime

class NotificationModel:

    def __init__(self):
        self.collection = get_collection("notifications")

    def get_all(self):
        return list(self.collection.find().sort("_id", -1))

   

    def create(self, data):

     notification = {

        "title": data.get("title"),

        "message": data.get("message"),

        "district": data.get("district"),

        "type": data.get("type", "General"),

        "created_at": datetime.utcnow(),

        "status": "Active"

    }

     return self.collection.insert_one(notification)
    
    def delete(self, id):

        from bson import ObjectId

        return self.collection.delete_one(

        {"_id": ObjectId(id)}

    )
    def get(self, id):

        from bson import ObjectId

        return self.collection.find_one(

        {"_id": ObjectId(id)}

    )