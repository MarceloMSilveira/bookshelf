import os

SECRET_KEY = os.urandom(32)
#Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

database_name = "bookshelf"
user_name = "marcelopostgresuser"
password = '73$Rps'
host = "localhost:5432"

database_path = f"postgresql://{user_name}:{password}@{host}/{database_name}"

SQLALCHEMY_DATABASE_URI = database_path


