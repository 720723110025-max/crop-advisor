"""
Models package — lazy imports to avoid circular dependencies.
"""

__all__ = ['User']


def __getattr__(name):
    if name == 'User':
        from app.models.user import User
        return User
    raise AttributeError(name)
