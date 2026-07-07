from app.utils.database import get_collection

class MarketModel:

    def __init__(self):
        self.collection = get_collection("market_prices")

    def get_all(self):
        return list(self.collection.find())

    def add_price(self, data):
        return self.collection.insert_one(data)