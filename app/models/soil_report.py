from app.utils.database import get_collection

class SoilReportModel:

    def __init__(self):
        self.collection = get_collection("soil_reports")

    def get_all(self):
        return list(self.collection.find())

    def create(self, data):
        return self.collection.insert_one(data)