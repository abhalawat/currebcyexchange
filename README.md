<h1 align="center">CurrencyXchange</h1>
This is a API System built on Django rest framework.
API is secured using token Authentication.

## Features

#### User Authentication API - https://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html
* User SignUp - New user has a default profile picture set and wallet balance 0.
* User Login
* User Logout & more.
#### User update profile picture API

#### User wallet API
* View wallet balance.
* Deposit to wallet balance.
* Withdraw from wallet balance.
#### Currency exchange API
Convert amount to destination currency.

## Getting Started
Create & Start your python virtual environment. - Optional

Run the following commands:
``` bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Make API call using POSTMAN(https://www.getpostman.com/) App.
All API endpoints/URL's are available inside the postman export folder.

### Thanks