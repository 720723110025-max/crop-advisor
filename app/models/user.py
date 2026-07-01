"""
User model for MongoDB.
Handles user accounts and authentication.
"""

from datetime import datetime
from flask_login import UserMixin


class User(UserMixin):

    @staticmethod
    def _get_collection():
        from app.utils.database import db_instance
        return db_instance.get_collection('users')

    def __init__(self, username, email, password, full_name, **kwargs):
        self.id = None  # set after save / from_dict
        self.username = username
        self.email = email
        self.full_name = full_name
        self.phone = kwargs.get('phone', '')
        self.address = kwargs.get('address', '')
        self.farm_size = kwargs.get('farm_size', 0)
        self.farm_location = kwargs.get('farm_location', '')
        self.is_admin = kwargs.get('is_admin', False)
        self.active = kwargs.get('is_active', True)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.password_hash = b''
        if password:
            self.set_password(password)

    # ------------------------------------------------------------------
    # Password helpers — use flask_bcrypt via app extension
    # ------------------------------------------------------------------

    def set_password(self, password):
        import bcrypt as _bcrypt
        salt = _bcrypt.gensalt()
        pw = password.encode('utf-8') if isinstance(password, str) else password
        self.password_hash = _bcrypt.hashpw(pw, salt)

    def check_password(self, password):
        try:
            import bcrypt as _bcrypt
            pw = password.encode('utf-8') if isinstance(password, str) else password
            ph = self.password_hash
            if isinstance(ph, str):
                ph = ph.encode('utf-8')
            return _bcrypt.checkpw(pw, ph)
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Flask-Login interface
    # ------------------------------------------------------------------

    @property
    def is_active(self):
        return bool(self.active)

    def get_id(self):
        return str(self.id) if self.id else None

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self):
        user_data = {
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address,
            'farm_size': self.farm_size,
            'farm_location': self.farm_location,
            'is_admin': self.is_admin,
            'is_active': self.active,
            'created_at': self.created_at,
            'updated_at': datetime.utcnow(),
        }
        result = self._get_collection().insert_one(user_data)
        self.id = str(result.inserted_id)
        return self.id

    def update(self, data):
        from bson import ObjectId
        data['updated_at'] = datetime.utcnow()
        # Mirror any attribute updates onto the in-memory object
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
        result = self._get_collection().update_one(
            {'_id': ObjectId(self.id)},
            {'$set': data}
        )
        return result.modified_count > 0

    # ------------------------------------------------------------------
    # Class / static finders
    # ------------------------------------------------------------------

    @staticmethod
    def find_by_username(username):
        data = User._get_collection().find_one({'username': username})
        return User.from_dict(data) if data else None

    @staticmethod
    def find_by_email(email):
        data = User._get_collection().find_one({'email': email})
        return User.from_dict(data) if data else None

    @staticmethod
    def find_by_id(user_id):
        from bson import ObjectId
        try:
            data = User._get_collection().find_one({'_id': ObjectId(user_id)})
            return User.from_dict(data) if data else None
        except Exception:
            return None

    @staticmethod
    def from_dict(data):
        if not data:
            return None
        user = User(
            username=data.get('username', ''),
            email=data.get('email', ''),
            password='',
            full_name=data.get('full_name', ''),
            phone=data.get('phone', ''),
            address=data.get('address', ''),
            farm_size=data.get('farm_size', 0),
            farm_location=data.get('farm_location', ''),
            is_admin=data.get('is_admin', False),
            is_active=data.get('is_active', True),
        )
        user.id = str(data['_id'])
        user.password_hash = data.get('password_hash', b'')
        user.created_at = data.get('created_at', datetime.utcnow())
        user.updated_at = data.get('updated_at', datetime.utcnow())
        return user

    def get_profile_data(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': getattr(self, 'phone', ''),
            'address': getattr(self, 'address', ''),
            'farm_size': getattr(self, 'farm_size', 0),
            'farm_location': getattr(self, 'farm_location', ''),
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<User {self.username}>'
