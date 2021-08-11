# Introduction
This is a demo of running two apps, `one` and `two`, each with its own database in a Django project

# Define models in app `one`
```
from django.db import models

# Create your models here.
class OneModel(models.Model):
    name=models.CharField(max_length=10)

    class Meta:
        app_label = 'one'

    def __str__(self):
        return self.name
```

# Define models in app `two`
```
from django.db import models

# Create your models here.
class OneModelId(models.Model):

    class Meta:
        app_label = 'two'

    def __str__(self):
        return f'{self.id}'

class TwoModel(models.Model):
    name = models.CharField(max_length=10)
    one_model = models.ForeignKey(OneModelId, on_delete=models.CASCADE, null=True)

    class Meta:
        app_label = 'two'

    def __str__(self):
        return self.name
```

# Create a database router in *one/router.py*
```
# This class routes the database operations
# Reference: `https://docs.djangoproject.com/en/3.2/topics/db/multi-db/`
class DbRouter:
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
```

# Define the database router in Djangon settings, *settings.py*
```
# Database Router for routing multiple databases
DATABASE_ROUTERS = [
    'one.router.DbRouter', # resides in the one/router.py
]
```

# Define the database engines in Django settings, *settings.py*
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'one_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'one_db',
        'USER': 'admin',
        'PASSWORD': 'secret_password',
        'HOST': 'localhost',
        'PORT': '',
    },
    'two_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'two_db',
        'USER': 'admin',
        'PASSWORD': 'secret_password',
        'HOST': 'localhost',
        'PORT': '',
    },
}
```

# Create two Postgres databases, one_db, and two_db, defined in `django.psql`, using `psql`
```
$ psql -U postgres -f django.psql
```

# Make migrations for the two apps
```
$ python manage.py makemigrations one two
$ python manage.py migrate --database=one_db
$ python manage.py migrate --database=two_db
```

# Make migrations for the rest of the tables (auth, admin, etc.)
$ python manage.py migrate

# Check the content of database, one_db, with psql 
```
$ psql -d one_db -U admin -W
psql (11.10)Type "help" for help.one_db=> \dt                  
List of relations Schema |            Name            | Type  | Owner 
--------+----------------------------+-------+------- 
public | auth_group                 | table | admin 
public | auth_group_permissions     | table | admin 
public | auth_permission            | table | admin 
public | auth_user                  | table | admin 
public | auth_user_groups           | table | admin 
public | auth_user_user_permissions | table | admin 
public | django_admin_log           | table | admin 
public | django_content_type        | table | admin 
public | django_migrations          | table | admin 
public | django_session             | table | admin 
public | one_onemodel               | table | admin
(11 rows)
one_db=>
one_db=> select * from one_onemodel; 
id | name ----+------
(0 rows)
```

# Check the content of database, two_db, with psql 
```
$ psql -d two_db -U admin -W
psql (11.10)Type "help" for help.
two_db=> \dt                  
List of relations Schema |            Name            | Type  | Owner 
--------+----------------------------+-------+------- 
public | auth_group                 | table | admin 
public | auth_group_permissions     | table | admin 
public | auth_permission            | table | admin 
public | auth_user                  | table | admin 
public | auth_user_groups           | table | admin 
public | auth_user_user_permissions | table | admin 
public | django_admin_log           | table | admin 
public | django_content_type        | table | admin 
public | django_migrations          | table | admin 
public | django_session             | table | admin 
public | two_onemodelid             | table | admin 
public | two_twomodel               | table | admin
(12 rows)

two_db=> select * from two_onemodelid;
id ----
(0 rows)
two_db=> select * from two_twomodel; 
id | name | one_model_id 
----+------+--------------
(0 rows)
```

# Create a superuser and access the Django admin
```
$ python manage.py createsuperuser
```
In Django Admin, create instances for OneModel (residing in one_db), OneModelId and TwoModel (both in two_db)

# Query and Create Instances with Django's Model API
```
$ python manage.py shell
Python 3.8.7 (default, Jan  4 2021, 21:17:21) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.24.0 -- An enhanced Interactive Python. Type '?' for help.

# import models from two different apps
In [1]: from one.models import *
In [2]: from two.models import *

# query instances in one_db
In [3]: OneModel.objects.all()
Out[3]: <QuerySet [<OneModel: one.1>]>

# query instances in two_db
In [4]: TwoModel.objects.all()
Out[4]: <QuerySet [<TwoModel: two.1>]>
In [5]: OneModelId.objects.all()
Out[5]: <QuerySet [<OneModelId: 1>]>

# create instance in one_db
In [6]: OneModel.objects.create(name='one.2')  
Out[6]: <OneModel: one.2>

# create instance in two_db referencing instance in one_db
In [7]: OneModelId.objects.create(id=OneModel.objects.last().id) 
Out[7]: <OneModelId: 2> 
```

# Verify content in database, one_db, using psql
```
$ psql -d one_db -U admin -W
Password: psql (11.10)
Type "help" for help.
one_db=> select * from one_onemodel; 
id | name  
----+-------  
1 | one.1  
2 | one.2
(2 rows)
one_db=> \q
```

# Verify content in database, two_db, using psql
```
$ psql -d two_db -U admin -W
Password: 
psql (11.10)
Type "help" for help.
two_db=> select * from two_onemodelid; 
id 
----  
1  
2
(2 rows)
two_db=> select * from two_twomodel; 
id | name  | one_model_id 
----+-------+--------------  
1 | two.1 |            1
(1 row)
two_db=> 
```
