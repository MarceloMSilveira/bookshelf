from flask import Flask, request, abort, redirect, url_for
from flask_cors import CORS, cross_origin
from models import Book
from config_db import db
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException


BOOKS_PER_SHELF = 5

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there.
#     If you do not update the endpoints, the lab will not work - of no fault of your API code!
#   - Make sure for each route that you're thinking through when to abort and with which kind of error
#   - If you change any of the response body keys, make sure you update the frontend to correspond.


# create and configure the app

migrate = Migrate()

def create_app(config_object='config'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)

    migrate.init_app(app,db)

    with app.app_context():
        db.create_all()

    CORS(app,
        origins=["http://localhost:5173","http://127.0.0.1:5173/"],
        #origins=['*'],
        methods=['GET','POST'],
        supports_credentials=True)

    #CASO NECESSÁRIO EM ALGUMA ROTA EM ESPECIAL USAR
    #@cross_origin()

    @app.route('/')
    def home():
        return redirect(url_for('all_books'))
        #return 'test'

    # done!
    # @TODO: Write a route that retrivies all books, paginated.
    #         You can use the constant above to paginate by eight books.
    #         If you decide to change the number of books per page,
    #         update the frontend to handle additional books in the styling and pagination
    #         Response body keys: 'success', 'books' and 'total_books'
    # TEST: When completed, the webpage will display books including title, author, and rating shown as stars

    @app.route('/books')
    def all_books():
        page = request.args.get("page",1,type=int)
        stmt = db.select(Book).order_by(Book.id)
        try:
            books = db.session.execute(stmt).scalars().all()
            start = (page-1)*BOOKS_PER_SHELF
            end = page*BOOKS_PER_SHELF
            formatted_books = [book.format() for book in books]
            if (len(formatted_books[start:end])==0):
                abort(404)
            return {
                "success":True,
                "books": formatted_books[start:end],
                "total_books": len(formatted_books)
            }
        
        except Exception as e:
            print(str(e))
            abort(404)
        
    #done!
    # @TODO: Write a route that will update a single book's rating.
    #         It should only be able to update the rating, not the entire representation
    #         and should follow API design principles regarding method and route.
    #         Response body keys: 'success'
    # TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh
    @app.route('/books/<int:book_id>',methods=['PATCH'])
    @cross_origin()
    def update_rating(book_id):
        try:
            data = request.get_json()
        except:
            abort(415,description='Verifique os dados enviados para atualizar o rating')

        if (data['rating']==''):
            abort(400,description='missing rating field in your request')
        try:
            book = db.get_or_404(Book,book_id)
            book.rating = data['rating']
            book.update()
            return {
                "success":True,
                "updated":book.id
            }
        except:
            db.session.rollback()
            abort(404)

    #done
    # @TODO: Write a route that will delete a single book.
    #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
    #        Response body keys: 'success', 'books' and 'total_books'

    # TEST: When completed, you will be able to delete a single book by clicking on the trashcan.
    @app.route('/books/<int:book_id>', methods=['DELETE'])
    @cross_origin()
    def delete_book(book_id):
        try:
            book = db.session.get(Book,book_id)
            if not book:
                abort(404)
            book.delete()
            results = db.session.execute(db.select(Book).order_by(Book.id)).scalars().all()
            books = [{'id':r.id, 'title':r.title, 'rating':r.rating, 'author':r.author} for r in results]
            

            return {
                'success':True,
                'deleted':book_id,
                'books': books,
                'total_books': len(books)
            }
        except:
            abort(404)



    # @TODO: Write a route that create a new book.
    #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
    # TEST: When completed, you will be able to create a new book using the form. Try doing so from the last page of books.
    #       Your new book should show up immediately after you submit it at the end of the page.
    @app.route('/books', methods=['POST'])
    def add_book():
        data = request.get_json()
        if (not(data.get('title')) or not(data.get('author')) or not(data.get('rating'))):
                abort(422, description = 'Parece que está faltando uma informação sobre o Livro')
        try:
            new_book = Book (
                title=data.get('title',None),
                author=data.get('author',None),
                rating=data.get('rating',None)
            )
            
            new_book.insert()
            results = db.session.execute(db.select(Book).order_by(Book.id)).scalars().all()
            books = [{'id':r.id, 'title':r.title, 'rating':r.rating, 'author':r.author} for r in results]
            print(new_book.id)
            return {
                'success':True,
                'created':new_book.id,
                'books':books,
                'total_books':len(books)
            }
        except HTTPException as e:
            raise e
        except Exception:
            db.session.rollback()
            abort(422, description='Não foi possível processar a solicitação de inclusão desse livro no servidor.')
    
    
    @app.errorhandler(400)
    def bad_request(error):
        return{
            "status": 400,
            "success":False,
            "error": 'bad request',
            "message":getattr(error, 'description','')
        }, 400

    @app.errorhandler(404)
    def not_found(error):
        return {
            "success":False,
            "error": 404,
            "message":"Resource not found"
        }, 404

    @app.errorhandler(415)
    def unsupported_type(error):
        return{
            "status": 415,
            "success":False,
            "error": 'unsupported type',
            "message":getattr(error, 'description','')
        }, 415

    @app.errorhandler(422)
    def unprocessable(error):
        return {
            "status": 422,
            "success":False,
            "error": 'Unprocessable Entity',
            "message":getattr(error, 'description','')
        }, 422


    @app.errorhandler(405)
    def method_not_allowed(error):
        return {
            "status": 405,
            "success":False,
            "error": 'Method not allowed',
            "message":getattr(error, 'description','')
        }, 405

    return app

# Para rodar local:
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)