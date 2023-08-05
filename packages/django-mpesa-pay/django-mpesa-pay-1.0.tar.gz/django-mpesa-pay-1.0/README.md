# django-mpesa

This is a django package that provides access to all safaricom plc mpesa endpoints.
It has all mpesa endpoint that has the latest changes to the mpesa api endpoint in compliance to kenya data protection act.

## Installation

Type the command below to install the package in your environemnt variable

```python
python -m pip install django-mpesa-pay
```

In your django project in your **INSTALLED_APPS** add the following

```python
INSTALLED_APPS = [
    #your apps
    "django-mpesa",
]
```

The go to [safaricom](https://developer.safaricom.co.ke/) and create your account so that you can have access to mpesa sandbox for testing your mpesa credential.

From safaricom you will get the following credentials
passkey= **************

```python
#settings.py 
PASS_KEY = ********* #your passkey from safaricom 
ACCOUNT_REFERENCE = "name of your app"
BUSINESS_SHORT_CODE = #your till number
```

NB: Remember to save your PASS_KEY and ACCESS TOKENS in an environment variables in production.
