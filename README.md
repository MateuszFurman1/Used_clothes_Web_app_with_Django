https://user-images.githubusercontent.com/106817902/219962697-f79621cc-2e38-4c1e-8ea5-d4f9324870ba.mp4


## Key Features

* Make donation
* Confirm if donation was taken
* See and edit profile
* For editing profile - have to set password. Can change password
* Registration/Login/logout


## How to run
* clone repository
* go to Settings-> Project-> Python Interpreter-> add interpreter-> add local interpreter
* terminal: pip install -r requirements.txt
* create connection to database, for exampe PostgreSQL
* open pgadmin and type create database usedClothes
* terminal: python manage.py migrate 
* terminal: python manage.py seed_db- to create dummy data 
* terminal: python manage.py runserver
* go to http://127.0.0.1:8000

## Requirements

* asgiref==3.5.2
* autopep8==2.0.1
* Django==4.1.5
* django-crispy-forms==1.14.0
* factory-boy==3.2.1
* Faker==17.0.0
* psycopg2-binary==2.9.5
* pycodestyle==2.10.0
* python-dateutil==2.8.2
* six==1.16.0
* sqlparse==0.4.3
* tomli==2.0.1
* xdg==5.1.1
