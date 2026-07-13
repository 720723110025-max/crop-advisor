from app.utils.database import get_collection
from bson import ObjectId
from datetime import datetime


class SoilReportModel:

    def __init__(self):
        self.collection = get_collection("soil_reports")

    def get_all(self):

        return list(

            self.collection.find().sort(

                "created_at", -1

            )

        )

    def get(self, report_id):

        return self.collection.find_one(

            {

                "_id": ObjectId(report_id)

            }

        )

    def create(self, data):

        report = {

            "farmer": data.get("farmer"),

            "soil_image": data.get("soil_image"),

            "soil_type": data.get("soil_type"),

            "ph": float(data.get("ph", 0)),

            "nitrogen": float(data.get("nitrogen", 0)),

            "phosphorus": float(data.get("phosphorus", 0)),

            "potassium": float(data.get("potassium", 0)),

            "crop_recommendation": data.get("crop_recommendation"),

            "fertilizer": data.get("fertilizer"),

            "irrigation": data.get("irrigation"),

            "soil_health": data.get("soil_health"),

            "created_at": datetime.utcnow()

        }

        return self.collection.insert_one(report)

    def update(self, report_id, data):

        return self.collection.update_one(

            {

                "_id": ObjectId(report_id)

            },

            {

                "$set": data

            }

        )

    def delete(self, report_id):

        return self.collection.delete_one(

            {

                "_id": ObjectId(report_id)

            }

        )

    def count(self):

        return self.collection.count_documents({})