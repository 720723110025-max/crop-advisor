from app.utils.database import get_collection

class AdminModel:

    def __init__(self):
        self.users = get_collection("users")
        self.feedback = get_collection("feedback")
        self.workshops = get_collection("workshops")
        self.notifications = get_collection("notifications")

    def users_count(self):
        return self.users.count_documents({})

    def feedback_count(self):
        return self.feedback.count_documents({})

    def workshop_count(self):
        return self.workshops.count_documents({})

    def notification_count(self):
        return self.notifications.count_documents({})