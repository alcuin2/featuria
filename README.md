# Featuria
BriteCore Assessment App

[Link to the app](http://lawcham.com) - http://lawcham.com

* Register
* Login
* Click on "Add Feature"

You can also use the "Settings" to create new Product Area, increase Priority Range and other CRUD operations.
To manage clients, click on the "Clients" link.


## Tech stack
This app is running on:
* Ubuntu 18.04
* Flask (Python) 
* and other dependencies list on the requirements.txt file in the project.

## Deployment

The app was deployed using GIT to the server.
It is run using gunicorn as a WSGI and Nginx as a reverse proxy web server.

## Installation guide

* Create a virtualenv: $ virtualenv -p python3 venv
* Activate the environment: $ source venv/bin/activate
* Install dependencies: $ pip install -r requirements.txt
* Run app with gunicorn on [port]: $ gunicorn -b 127.0.0.1:5000 -w 4 run:app --daemon
* Set Nginx as a reverse proxy on the port specified.
