from orchy_project.dev_settings import *
import os

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'orchy_community',# Or path to database file if using sqlite3.
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'HOST': os.environ.get('DB_IP'),# Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': os.environ.get('DB_PORT'), # Set to empty string for default 3306.
    }
}
minio_url = os.environ.get('MINIO_URL')
minio_port = os.environ.get('MINIO_PORT')

MINIO = {
    'bucket_name':os.environ.get('MINIO_BUCKET_NAME'),
    'access_key':os.environ.get('MINIO_ACCESS_KEY'),
    'secret_key':os.environ.get('MINIO_SECRET_KEY'),
    'url': '{0}:{1}'.format(minio_url, minio_port)
}
