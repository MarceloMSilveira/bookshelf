#imports:
import unittest
from models import Book
from config_db import db
from app import create_app

# @TODO: Write at least two tests for each endpoint - one each for success and error behavior.
#        You can feel free to write additional tests for nuanced functionality,
#        Such as adding a book without a rating, etc.
#        Since there are four routes currently, you should have at least eight tests.
#        Optional: Update the book information in setUp to make the test database your own!


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
        self.app = create_app(TextConfig)        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # dados iniciais no db para teste :
        self.seed_books = [
            Book(title='Clean Code', author='Robert C. Martin', rating=5),
            Book(title='The Pragmatic Programmer', author='Andy & Dave', rating=5),
            Book(title='Refactoring', author='Martin Fowler', rating=4),
            Book(title='Test-Driven Development', author='Kent Beck', rating=5),
            Book(title='Fluent Python', author='Luciano Ramalho', rating=5),
            Book(title='Design Patterns', author='GoF', rating=5),
        ]
        for b in self.seed_books:
            b.insert()
        return super().setUp()
    
    #ações após cada teste:
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        return super().tearDown()
    
    # GET / paginação

    def test_get_books_first_page_ok(self):
        res = self.client.get('books?page=1')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('books', data)
        self.assertIn('total_books', data)
        self.assertEqual(len(data['books']), 5)
        self.assertEqual(len(data['total_books'],len(self.seed_books)))