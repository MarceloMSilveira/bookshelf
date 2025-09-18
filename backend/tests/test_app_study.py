#imports
import unittest
from app import create_app
from config_db import db
from models import Book
import json

#config class

class Basic_Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    #SQLALCHEMY_TRACK_MODIFICATIONS = False # será que preciso disso? Não precisei nos meus testes

class BookApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(Basic_Config)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.seed_books = [
            Book(title='Clean Code', author='Robert C. Martin', rating=5),
            Book(title='The Pragmatic Programmer', author='Andy & Dave', rating=5),
            Book(title='Refactoring', author='Martin Fowler', rating=4),
            Book(title='Test-Driven Development', author='Kent Beck', rating=5),
            Book(title='Fluent Python', author='Luciano Ramalho', rating=5),
            Book(title='Design Patterns', author='GoF', rating=5),
            Book(title='Clean Code2', author='Robert C. Martin2', rating=5),
            Book(title='The Pragmatic Programmer2', author='Andy & Dave2', rating=5),
            Book(title='Refactoring2', author='Martin Fowler2', rating=4),
            Book(title='Test-Driven Development2', author='Kent Beck2', rating=5),
            Book(title='Fluent Python2', author='Luciano Ramalho2', rating=5),
            Book(title='Design Patterns2', author='GoF2', rating=5)
        ]
        for b in self.seed_books:
            b.insert()

        return super().setUp()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        return super().tearDown()

#get rota '/' => 302 (found)    
    def test_home_access_ok(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 302)

# get /books (todos os livros com/sem paginação)
    #sucesso:
    def test_get_books_success_cases(self):
        res = self.client.get('/books')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertIn("books", data)
        self.assertIn("success", data)
        self.assertTrue(data["success"])
        self.assertIn("total_books", data)
        total_books = data.get("total_books")
        self.assertEqual(total_books, 12)
        books_in_page = len(data['books'])
        self.assertEqual(books_in_page,5)
        res2 = self.client.get('/books?page=3')
        data = res2.get_json()
        self.assertEqual(len(data["books"]),2)

    #falhas:
    def test_get_books_fail_cases(self):
        res = self.client.get('/books?page=10')
        self.assertEqual(res.status_code, 404)
        data = res.get_json()
        self.assertFalse(data['success'])


# post /books
    #success:
    def test_post_books_success_cases(self):
        payload = {'title': 'Effective Python', 'author': 'Brett Slatkin', 'rating': 5}
        res = self.client.post('/books', data=json.dumps(payload), content_type='application/json')
        data = res.get_json()
        self.assertIn(res.status_code,[200,201])
        self.assertTrue(data['success'])
        self.assertIn('created',data)
        self.assertEqual(data['total_books'],len(self.seed_books)+1)
    
    #fails
    def test_post_books_fail_cases(self):
        payload = {'title': '', 'author': 'Brett Slatkin', 'rating': 5}
        res = self.client.post('/books', data=json.dumps(payload), content_type='application/json')
        data = res.get_json()
        self.assertEqual(res.status_code,422) 
        self.assertFalse(data['success'])

    #fails wrong endpoint
    def test_post_books_wrong_endpoint(self):
        payload = {'title': '', 'author': 'Brett Slatkin', 'rating': 5}
        res = self.client.post('/books/45', data=json.dumps(payload), content_type='application/json')
        data = res.get_json()
        self.assertEqual(res.status_code,405) 
        self.assertFalse(data['success'])


# PATCH /books/id
    #success
    def test_patch_books_success_cases(self):
        # pega um id existente
        a_book = db.session.execute(db.select(Book).order_by(Book.id)).scalars().first()
        print(f"ID EXISTENTE NO MEU BD: {a_book.id}")
        self.assertEqual(a_book.rating,5)
        res = self.client.patch(f'/books/{a_book.id}', data=json.dumps({'rating': 3}),
                                content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(a_book.rating,3)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('updated',data)

    #fail1 id não existente:
    def test_update_rating_404_for_unknown_id(self):
        res = self.client.patch('/books/99999', data=json.dumps({'rating': 1}),
                                content_type='application/json')
        self.assertEqual(res.status_code, 404)
    #fail2 faltou o dado {'rating':x}
    def test_update_missing_body_fail_case(self):
        res = self.client.patch('/books/1', content_type='application/json')
        self.assertEqual(res.status_code,415)


# delete /books/id
    #success
    def test_delete_books_success_cases(self):
         # cria um livro para deletar
        b = Book(title='Temp', author='X', rating=1)
        b.insert()
        #before = db.session.execute(db.select(Book)).scalars().all()
        res = self.client.delete(f'/books/{b.id}')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], b.id)
        rows = db.session.execute(db.select(Book)).scalars().all()
        all_books_len = len([r.title for r in rows])
        b2 = db.session.execute(db.select(Book).where(Book.title=='Refactoring')).scalars().first()
        res = self.client.delete(f'/books/{b2.id}')
        data = res.get_json()
        self.assertIn('deleted',data)
        rows = db.session.execute(db.select(Book)).scalars().all()
        all_books_len_after_delete = len([r.title for r in rows])
        self.assertEqual(all_books_len-1,all_books_len_after_delete)
    
    
    #fail
    def test_delete_books_fail_cases(self):
        res = self.client.delete('books/1000')
        data = res.get_json()
        self.assertEqual(res.status_code,404)
        self.assertFalse(data['success'])

if __name__ == '__main__':
    unittest.main()