https://user-images.githubusercontent.com/106817902/220195579-9082a7e4-059c-4f98-b770-145f6bd74d88.mp4


## Key Features

* Add/delete delegation request if login
* Add/delete vacation request if login
* Login/logout
* See group members
* Accept/reject delegation/vacation requests for manager group
* Message system to inform about decision
* Appk is still in development phase

App, which helps in office task. Two groups with different permissions. Employees group can send request for holiday, delegation and medical leave and see employees from his group. Also can see pending, accepted and rejected request. User is informed by message system about his request.  Second group- manager, have permission to accept and reject pending from subordinate members. Also can see which of subordinate member is today on vacation/delegation. Registration and login/logout system are implemented for both groups. Pytest covers all views with fixtures. Project is still continued. Future features planned to add: calendar, delegation calculation, service desk ticket, more accurate delegation model.
Tools & technologies used in project:
python, django framework, postgreSQL, pytest, Bootstrap, HTML, CSS, pycharm


## How to run
* clone repository
* go to Settings-> Project-> Python Interpreter-> add interpreter-> add local interpreter
* terminal: pip install -r requirements.txt
* create connection to database, for exampe PostgreSQL
* open pgadmin and type create database officeTool
* terminal: python manage.py migrate 
* terminal: python manage.py seed_db- to create dummy data
* terminal: python manage.py runserver
* go to http://127.0.0.1:8000

## Requirements

* asgiref==3.5.2
* attrs==22.1.0
* autopep8==2.0.1
* convertdate==2.4.0
* Django==4.1.3
* django-crispy-forms==1.14.0
* exceptiongroup==1.0.4
* factory-boy==3.2.1
* Faker==17.0.0
* hijri-converter==2.2.4
* holidays==0.17.2
* iniconfig==1.1.1
* korean-lunar-calendar==0.3.1
* packaging==22.0
* pluggy==1.0.0
* psycopg2-binary==2.9.5
* pycodestyle==2.10.0
* PyMeeus==0.5.11
* pytest==7.2.0
* pytest-django==4.5.2
* python-dateutil==2.8.2
* six==1.16.0
* sqlparse==0.4.3
* tomli==2.0.1
* vacation==0.4.7
* workdays==1.4
