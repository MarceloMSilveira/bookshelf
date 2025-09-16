import os
from flask import Flask, request, abort
from flask_cors import CORS, cross_origin
import random
from models import Book
from config_db import db
from flask_migrate import Migrate

BOOKS_PER_SHELF = 8

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there.
#     If you do not update the endpoints, the lab will not work - of no fault of your API code!
#   - Make sure for each route that you're thinking through when to abort and with which kind of error
#   - If you change any of the response body keys, make sure you update the frontend to correspond.


# create and configure the app
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

migrate = Migrate(app,db)

from models import Book

with app.app_context():
    db.create_all()

CORS(app,
     origins=[],
     methods=['GET','POST'],
     supports_credentials=True)

#CASO NECESSÁRIO EM ALGUMA ROTA EM ESPECIAL USAR
#@cross_origin()

@app.route('/')
def home():
    return 'Ok!'

# @TODO: Write a route that retrivies all books, paginated.
#         You can use the constant above to paginate by eight books.
#         If you decide to change the number of books per page,
#         update the frontend to handle additional books in the styling and pagination
#         Response body keys: 'success', 'books' and 'total_books'
# TEST: When completed, the webpage will display books including title, author, and rating shown as stars

# @TODO: Write a route that will update a single book's rating.
#         It should only be able to update the rating, not the entire representation
#         and should follow API design principles regarding method and route.
#         Response body keys: 'success'
# TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh

# @TODO: Write a route that will delete a single book.
#        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
#        Response body keys: 'success', 'books' and 'total_books'

# TEST: When completed, you will be able to delete a single book by clicking on the trashcan.

# @TODO: Write a route that create a new book.
#        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
# TEST: When completed, you will be able to a new book using the form. Try doing so from the last page of books.
#       Your new book should show up immediately after you submit it at the end of the page.

