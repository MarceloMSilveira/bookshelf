#imports:
import unittest
from models import Book
from config_db import db
from app import create_app

#definição das configurações que serão passadas para o nosso flask-app (TESTING e SQLALCHEMY_DATABASE_URI)
#principalmente para sobrescrever o db que será acessado.
class TextConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# definir a classe de teste
class BookShelfApiTestCase(unittest.TestCase):
    #ações antes de cada teste:
    def setUp(self):
        

        return super().setUp()
    
    #ações após cada teste:
    def tearDown(self):
        return super().tearDown()
    
