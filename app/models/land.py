from app.utils.database import get_collection
from bson import ObjectId
from datetime import datetime


class LandModel:

    def __init__(self):
        self.collection = get_collection("lands")

    def get_all(self):
        return list(
            self.collection.find().sort("created_at", -1)
        )

    def get_by_user(self, user_id):
        return list(
            self.collection.find(
                {"user_id": user_id}
            ).sort("created_at", -1)
        )

    def create(self, data):

        land = {

            "user_id": data.get("user_id"),

            "land_name": data.get("land_name"),

            "district": data.get("district"),

            "block": data.get("block"),

            "village": data.get("village"),

            "area": float(data.get("area", 0)),

            "soil_type": data.get("soil_type"),

            "previous_crop": data.get("previous_crop"),

            "current_crop": data.get("current_crop"),

            "gps_latitude": data.get("gps_latitude"),

            "gps_longitude": data.get("gps_longitude"),

            "soil_image": data.get("soil_image"),

            "yield_history": data.get("yield_history", []),

            "estimated_profit": data.get("estimated_profit", 0),

            "created_at": datetime.utcnow(),

            "updated_at": datetime.utcnow()

        }

        return self.collection.insert_one(land)

    def get(self, land_id):

        return self.collection.find_one(
            {
                "_id": ObjectId(land_id)
            }
        )

    def update(self, land_id, data):

        data["updated_at"] = datetime.utcnow()

        return self.collection.update_one(

            {
                "_id": ObjectId(land_id)
            },

            {
                "$set": data
            }

        )

    def delete(self, land_id):

        return self.collection.delete_one(
            {
                "_id": ObjectId(land_id)
            }
        )

    def count(self):

        return self.collection.count_documents({})

    def get_by_district(self, district):

        return list(

            self.collection.find(

                {
                    "district": district
                }

            )

        )

    def search(self, keyword):

        return list(

            self.collection.find(

                {

                    "$or": [

                        {
                            "land_name": {
                                "$regex": keyword,
                                "$options": "i"
                            }
                        },

                        {
                            "village": {
                                "$regex": keyword,
                                "$options": "i"
                            }
                        },

                        {
                            "district": {
                                "$regex": keyword,
                                "$options": "i"
                            }
                        }

                    ]

                }

            )

        )