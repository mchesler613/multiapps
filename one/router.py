# This class routes the database operations
# Reference: https://docs.djangoproject.com/en/3.2/topics/db/multi-db/
class DbRouter:
    apps = [ 'one', 'two' ]

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'one':
            return 'one_db'
        elif model._meta.app_label == 'two':
            return 'two_db'

        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'one':
            return 'one_db'
        elif model._meta.app_label == 'two':
            return 'two_db'

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'one':
            return db == 'one_db'
        elif app_label == 'two':
            return db == 'two_db'

        return None

    def allow_relation(self, obj1, obj2, **hints):
        print(obj1._meta.app_label, obj2._meta.app_label)
        if obj1._meta.app_label == 'one' and obj2._meta.app_label == 'one':
                return True
        elif 'one' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        elif obj1._meta.app_label == 'two' and obj2._meta.app_label == 'two':
            return True
        elif 'two' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True

        return False
