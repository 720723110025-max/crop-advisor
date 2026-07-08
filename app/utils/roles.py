from functools import wraps
from flask import abort
from flask_login import current_user


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != "admin":
            abort(403)
        return func(*args, **kwargs)
    return wrapper


def expert_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != "expert":
            abort(403)
        return func(*args, **kwargs)
    return wrapper


def farmer_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != "farmer":
            abort(403)
        return func(*args, **kwargs)
    return wrapper