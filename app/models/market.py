from app.utils.database import get_collection
from datetime import datetime


class MarketModel:

    def __init__(self):
        self.collection = get_collection("market_prices")

    def get_prices(self):
        return list(
            self.collection.find().sort("created_at", -1)
        )

    def create(self, data):

        market = {

            "crop": data.get("crop"),

            "district": data.get("district"),

            "market": data.get("market"),

            "price": float(data.get("price")),

            "unit": data.get("unit"),

            "trend": data.get("trend"),

            "created_at": datetime.utcnow()

        }

        return self.collection.insert_one(market)

    def delete(self, market_id):

        from bson import ObjectId

        return self.collection.delete_one(
            {"_id": ObjectId(market_id)}
        )

    def update(self, market_id, data):

        from bson import ObjectId

        return self.collection.update_one(
            {"_id": ObjectId(market_id)},
            {"$set": data}
        )