# tests/test_app.py
import unittest
import json
from app import create_app
from config_db import db
from models import Book

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class BooksApiTestCase(unittest.TestCase):
    def setUp(self):
        # cria app isolado para cada teste
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        # contexto + banco novo a cada teste
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # dados iniciais
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # -------- GET /books (paginação) ----------
    def test_get_books_first_page_ok(self):
        res = self.client.get('/books?page=1')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('books', data)
        self.assertIn('total_books', data)
        # sua constante BOOKS_PER_SHELF = 5
        self.assertEqual(len(data['books']), 5)
        self.assertEqual(data['total_books'], len(self.seed_books))

    def test_get_books_page_out_of_range_404(self):
        # temos 6 livros, 5 por página => page=3 não tem nada
        res = self.client.get('/books?page=3')
        self.assertEqual(res.status_code, 404)
        data = res.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)

    # -------- POST /books ----------
    def test_add_book_success(self):
        payload = {'title': 'Effective Python', 'author': 'Brett Slatkin', 'rating': 5}
        res = self.client.post('/books', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)  # seu endpoint retorna 200; poderia ser 201
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('created', data)
        self.assertEqual(data['total_books'], len(self.seed_books) + 1)

    def test_add_book_validation_422(self):
        payload = {'title': 'Missing author', 'rating': 5}  # faltando author
        res = self.client.post('/books', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 422)
        data = res.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(data['status'], 422)
        self.assertEqual(data['error'], 'Unprocessable Entity')
        self.assertIn('Livro', data['message'])
        res = self.client.post('/books/45', data=json.dumps(payload), content_type='application/json')

    #testar post to endpoint errado post ('/books/45') por exemplo.

    # -------- PATCH /books/<id> ----------
    def test_update_rating_success(self):
        # pega um id existente
        a_book = db.session.execute(db.select(Book).order_by(Book.id)).scalars().first()
        res = self.client.patch(f'/books/{a_book.id}', data=json.dumps({'rating': 3}),
                                content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'], a_book.id)
        # confere no banco
        reloaded = db.session.get(Book, a_book.id)
        self.assertEqual(reloaded.rating, 3)

    def test_update_rating_404_for_unknown_id(self):
        res = self.client.patch('/books/99999', data=json.dumps({'rating': 1}),
                                content_type='application/json')
        self.assertEqual(res.status_code, 404)

    # fazer um teste em que não é passado o data com o rating.

    # -------- DELETE /books/<id> ----------
    def test_delete_book_success(self):
        # cria um livro para deletar
        b = Book(title='Temp', author='X', rating=1)
        b.insert()
        before = db.session.execute(db.select(Book)).scalars().all()
        res = self.client.delete(f'/books/{b.id}')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], b.id)
        after = db.session.execute(db.select(Book)).scalars().all()
        self.assertEqual(len(after), len(before) - 1)

    def test_delete_book_404_when_not_found(self):
        res = self.client.delete('/books/99999')
        self.assertEqual(res.status_code, 404)

if __name__ == '__main__':
    unittest.main()
