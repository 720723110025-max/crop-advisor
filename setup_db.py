"""
MongoDB Atlas Setup Script for Crop Advisory System
Run this once to initialize the database
"""

import os
from datetime import datetime
from pymongo import MongoClient
import bcrypt

MONGO_URI = 'mongodb+srv://720723110025_db_user:720723110025@cluster0.k67dodz.mongodb.net/?appName=Cluster0'
DB_NAME = 'crop_advisory_db'

def setup_database():
    print("🌱 Setting up MongoDB Atlas for Crop Advisory System...")
    print(f"📡 Connecting to MongoDB Atlas...")
    
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        
        db = client[DB_NAME]
        print(f"📚 Using database: {DB_NAME}")
        
        # 1. Create Admin User
        users = db['users']
        if not users.find_one({'username': 'admin'}):
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), salt)
            
            admin = {
                'username': 'admin',
                'email': 'admin@cropadvisory.com',
                'password_hash': password_hash,
                'full_name': 'System Administrator',
                'phone': '+1234567890',
                'address': 'Admin Office',
                'farm_size': 0,
                'farm_location': 'Global',
                'is_admin': True,
                'is_active': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            users.insert_one(admin)
            print("✅ Admin user created (username: admin, password: admin123)")
        else:
            print("ℹ️ Admin user already exists")
        
        # 2. Create Sample Farmer
        if not users.find_one({'username': 'farmer1'}):
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw('farmer123'.encode('utf-8'), salt)
            
            farmer = {
                'username': 'farmer1',
                'email': 'farmer1@example.com',
                'password_hash': password_hash,
                'full_name': 'John Farmer',
                'phone': '+9876543210',
                'address': '123 Farm Road, Agriculture District',
                'farm_size': 25.5,
                'farm_location': 'California, USA',
                'is_admin': False,
                'is_active': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            users.insert_one(farmer)
            print("✅ Sample farmer created (username: farmer1, password: farmer123)")
        
        # 3. Create Sample Crops
        crops = db['crops']
        if crops.count_documents({}) == 0:
            sample_crops = [
                {
                    'name': 'Rice',
                    'scientific_name': 'Oryza sativa',
                    'category': 'cereal',
                    'season': 'Kharif',
                    'soil_type': 'Clayey loam',
                    'min_temperature': 20,
                    'max_temperature': 35,
                    'ideal_ph': 6.0,
                    'nitrogen_need': 120,
                    'phosphorus_need': 60,
                    'potassium_need': 60,
                    'water_requirement': 250,
                    'growing_days': 120,
                    'yield_per_acre': 4.5,
                    'description': 'A staple cereal crop grown in tropical regions.',
                    'is_active': True,
                    'created_at': datetime.utcnow()
                },
                {
                    'name': 'Wheat',
                    'scientific_name': 'Triticum aestivum',
                    'category': 'cereal',
                    'season': 'Rabi',
                    'soil_type': 'Loamy',
                    'min_temperature': 10,
                    'max_temperature': 25,
                    'ideal_ph': 6.5,
                    'nitrogen_need': 150,
                    'phosphorus_need': 60,
                    'potassium_need': 40,
                    'water_requirement': 150,
                    'growing_days': 110,
                    'yield_per_acre': 3.5,
                    'description': 'A major cereal grain cultivated worldwide.',
                    'is_active': True,
                    'created_at': datetime.utcnow()
                },
                {
                    'name': 'Maize',
                    'scientific_name': 'Zea mays',
                    'category': 'cereal',
                    'season': 'Kharif',
                    'soil_type': 'Well-drained loam',
                    'min_temperature': 18,
                    'max_temperature': 30,
                    'ideal_ph': 6.0,
                    'nitrogen_need': 180,
                    'phosphorus_need': 80,
                    'potassium_need': 60,
                    'water_requirement': 200,
                    'growing_days': 100,
                    'yield_per_acre': 5.0,
                    'description': 'A versatile grain crop used for food, feed, and fuel.',
                    'is_active': True,
                    'created_at': datetime.utcnow()
                },
                {
                    'name': 'Sugarcane',
                    'scientific_name': 'Saccharum officinarum',
                    'category': 'cash',
                    'season': 'Kharif',
                    'soil_type': 'Deep loamy',
                    'min_temperature': 25,
                    'max_temperature': 35,
                    'ideal_ph': 6.5,
                    'nitrogen_need': 200,
                    'phosphorus_need': 100,
                    'potassium_need': 120,
                    'water_requirement': 300,
                    'growing_days': 300,
                    'yield_per_acre': 6.0,
                    'description': 'A tropical grass used for sugar production.',
                    'is_active': True,
                    'created_at': datetime.utcnow()
                },
                {
                    'name': 'Cotton',
                    'scientific_name': 'Gossypium hirsutum',
                    'category': 'cash',
                    'season': 'Kharif',
                    'soil_type': 'Black soil',
                    'min_temperature': 25,
                    'max_temperature': 35,
                    'ideal_ph': 7.0,
                    'nitrogen_need': 100,
                    'phosphorus_need': 60,
                    'potassium_need': 60,
                    'water_requirement': 150,
                    'growing_days': 150,
                    'yield_per_acre': 2.5,
                    'description': 'A fiber crop used for textile production.',
                    'is_active': True,
                    'created_at': datetime.utcnow()
                }
            ]
            crops.insert_many(sample_crops)
            print(f"✅ {len(sample_crops)} crops added to database")
        
        print("\n✅ Database setup completed successfully!")
        print("📌 Login credentials:")
        print("   Admin: admin / admin123")
        print("   Farmer: farmer1 / farmer123")
        
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")

if __name__ == '__main__':
    setup_database()