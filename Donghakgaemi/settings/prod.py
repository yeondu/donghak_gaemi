from .base import *

ALLOWED_HOSTS = ['15.165.31.148']

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'Donghakgaemi',
        'USER': 'donghakgaemi',
        'PASSWORD': 'donghakmysql1',
        'HOST': '15.165.31.148',
        'PORT': '3306',
    }
}