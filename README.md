## Authentication System
An app that verifies an individual's identity using their login details. 

Click on [Django Auth System](https://django-auth-system.onrender.com) to interact with the deployed app.



### Tech Stack
- Python 3.12
- Django 5.0
- Django Rest Framework 3.15
- PostgreSQL 16



### Launch Project
Clone and install the project to your local machine.

```
$ cd ~
$ mkdir django-auth-project
$ cd django-auth-project
$ pipenv shell
$ pipenv install
$ git clone https://github.com/adara-code/auth-system
$ cd authentication 
$ pip install -r requirements.txt
```

Navigate to pgAdmin and create a new database
Return to the project and go to settings.py to connect your database to the app. Comment out database['default] line.

```
*settings.py*
DATABASES = {
    ‘default’: {
        ‘ENGINE’: ‘django.db.backends.postgresql_psycopg2’,
        ‘NAME’: env(‘DB_NAME’),
        ‘USER’: env(‘DB_USER’),
        ‘PASSWORD’: env(‘DB_PASSWORD’),
        'HOST': env('DB_HOST),
        'PORT': env('DB_PORT')
    }
}
```

Open terminal

```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```









