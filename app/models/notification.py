from app.utils.database import get_collection

class NotificationModel:

    def __init__(self):
        self.collection = get_collection("notifications")

    def get_all(self):
        return list(self.collection.find().sort("_id", -1))

    def create(self, data):
        return self.collection.insert_one(data)

    def by_district(self, district):
        return list(
            self.collection.find(
                {"district": district}
            )
        )