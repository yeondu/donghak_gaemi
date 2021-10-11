from .base import *
ALLOWED_HOSTS = ['*']

# 오류나면 mysql-connector-python 8.0.26 설치
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

