from app.utils.database import db_instance

collections = [
    "users",
    "crop_recommendations",
    "disease_reports",
    "fertilizer_recommendations",
    "yield_predictions",
    "irrigation_schedules",
    "notifications"
]

for name in collections:
    try:
        result = db_instance.get_collection(name).delete_many({})
        print(f"{name}: {result.deleted_count} documents deleted")
    except Exception as e:
        print(f"{name}: {e}")

print("\nDatabase cleared successfully.")