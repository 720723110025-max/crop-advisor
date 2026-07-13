from app.utils.database import get_collection
from datetime import datetime


class YieldModel:

    def __init__(self):
        self.collection = get_collection("yield_history")

    def get_all(self, user_id):

        return list(

            self.collection.find(

                {"user_id": user_id}

            ).sort("created_at", -1)

        )

    def create(self, data):

        data["created_at"] = datetime.utcnow()

        return self.collection.insert_one(data)

    def total_profit(self, user_id):

        records = self.get_all(user_id)

        total = 0

        for item in records:

            total += item["profit"]

        return total