from app.utils.database import get_collection

class ExpertModel:

    def __init__(self):
        self.collection = get_collection("experts")