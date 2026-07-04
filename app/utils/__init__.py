"""
Utils package initialization.
"""

__all__ = ['MongoDatabase', 'db_instance']


def __getattr__(name):
    if name in ('MongoDatabase', 'db_instance', 'get_collection',
                 'insert_one', 'find_one', 'find_many', 'update_one',
                 'delete_one', 'count'):
        import app.utils.database as _db
        return getattr(_db, name)
    raise AttributeError(name)
