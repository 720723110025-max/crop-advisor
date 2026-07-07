from app.utils.database import get_collection

class AppointmentModel:

    def __init__(self):
        self.collection = get_collection("appointments")

    def create(self, data):
        return self.collection.insert_one(data)

    def get_all(self):
        return list(self.collection.find())