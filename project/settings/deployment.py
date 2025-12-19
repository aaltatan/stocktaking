from .base import *

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=str).split(";")