from app.utils.database import get_collection

class CropModel:

    def __init__(self):
        self.collection = get_collection("crop_recommendations")

    def get_all(self):
        return list(self.collection.find())

    def create(self, data):
        return self.collection.insert_one(data)