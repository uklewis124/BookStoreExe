import flask
from flask import request

from main import check_book_uri
from scripts.prepare_database import Books
from . import api

@api.route('/api/v1/load_books_by_name', methods=['GET'])
def load_books_by_name():
    requested_data = request.get_json()

    query: str | None = requested_data['search_query']
    page: int | None = requested_data['page']

    if not query:
        return {
            'status': 'error',
            'message': 'No search query provided.'
        }

    if not page:
        # FIXME:
        page = 1

        search_result_isbn = Books.query.filter(Books.isbn.ilike(f'%{query}%')).all()
        search_result_name = Books.query.filter(Books.name.ilike(f'%{query}%')).all()
        search_result_author = Books.query.filter(Books.author.ilike(f'%{query}%')).all()
        search_result_category = Books.query.filter(Books.category.ilike(f'%{query}%')).all()
        search_result_format = Books.query.filter(Books.format.ilike(f'%{query}%')).all()

        search_results = []
        def search_results_append(variable):
            for book in variable:
                check_book_uri()
                search_results.append(book)
            with flask.current_app.app_context():
                db.session.commit()

        search_results_append(search_result_isbn)
        search_results_append(search_result_name)
        search_results_append(search_result_author)
        search_results_append(search_result_category)
        search_results_append(search_result_format)

        def get_page(page):
            PAGE_LENGTH = 10

            # How the equation will work:
            # 1. Identify how many it's sent already
            #    (page * PAGE_LENGTH)
            # 2. Get PAGE_LENGTH books after the book
            #    last previously sent

            start_index = (page - 1) * PAGE_LENGTH

            books = search_results[start_index:start_index + PAGE_LENGTH]

            return books

        return {
            'status': 'success',
            'books': get_page(page)
        }