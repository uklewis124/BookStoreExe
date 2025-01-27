import flask
from flask import Flask, session, redirect, render_template, request, url_for
import pandas as pd
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import jinja2
import stripe
import random
from sqlalchemy.sql.expression import func

from scripts.prepare_database import db, load_db_after_server, Books

server = Flask(__name__)


server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(server)
with server.app_context():
    db.drop_all()
    db.create_all()
    load_db_after_server()

stripe.api_key = 'rk_test_51QjgkTC1SMldrHOB4GEGcVMcWPHsCxuZaDurHGU6a7FqDCFRdwQqFhvXFy8SFYKwuOdsP9Jtpx5FwhZFbaYPlq5H00H8mzLpe7'


@server.route('/')
def index():
    quantity:int = Books.query.count()

    def get_image(image_uri):
        print(image_uri)

    def get_5_random_books():
        to_return = []
        COUNT = 5
        for i in range(0, COUNT):
            r1 = quantity - 1
            random_number = random.randint(0, r1)
            book = Books.query.filter_by(index=int(random_number)).first()
            if book:  # Ensure that the book exists before adding to the list
                if not book.image_uri:
                    book.image_uri = url_for('static', filename='{book.image_uri}')
                with flask.current_app.app_context():
                    db.session.commit()

                to_return.append(book)
        return to_return

    recommended_books = get_5_random_books()
    popular_books = get_5_random_books()
    new_books = get_5_random_books()

    print(recommended_books[0])

    return render_template(
        'index.html',
        recommended_books=recommended_books,
        popular_books=popular_books,
        new_books=new_books
    )

@server.route('/register/')
def register():
    return render_template('register.html')

@server.route('/login/')
def login():
    return render_template('login.html')

@server.route('/search/', methods=['GET', 'POST'])
def search(): 
    # check if form is submitted from search bar
    if request.method == "POST":
        if request.form:
            try:
                query = request.form.get('search_query')
                return render_template('search.html', search_query=query, books=temp_books) # Replace books with actual books
            except:
                pass
    return render_template('search.html', search_query="", books=[])

@server.route('/search/<query>/')
def search_query(query):
    return render_template('search.html', query=query)

@server.route('/e/<int:code>/')
def error(code):
    try:
        return render_template(f'error_pages/{code}.html')
    except jinja2.exceptions.TemplateNotFound:
        return render_template('error_pages/unknown.html', code=code)

import routes
server.register_blueprint(routes.routes_bp)

if __name__ == '__main__':
    server.run(debug=True)
    