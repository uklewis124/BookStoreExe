import flask
from flask import request

from main import check_book_uri
from scripts.prepare_database import Books, db
from . import api

@api.route('/api/v1/load_books_by_name', methods=['GET'])
def load_books_by_name():
    requested_data = request.get_json()

    query: str | None = requested_data.get('search_query')
    page: int | None = requested_data.get('page')

    if query is None or query.strip() == '':
        return {
            'status': 'error',
            'message': 'No search query provided.'
        }, 400

    if not page or not isinstance(page, int) or page <= 0:
        # FIXME:
        page = 1

        search_result_isbn = Books.query.filter(Books.isbn.ilike(f":query")).params(query=f"%{query}%").all()
        search_result_name = Books.query.filter(Books.name.ilike(f":query")).params(query=f"%{query}%").all()
        search_result_author = Books.query.filter(Books.author.ilike(f":query")).params(query=f"%{query}%").all()
        search_result_category = Books.query.filter(Books.category.ilike(f":query")).params(query=f"%{query}%").all()
        search_result_format = Books.query.filter(Books.format.ilike(f":query")).params(query=f"%{query}%").all()

        search_results = []
        def search_results_append(variable):
            for var in variable:
                for book in var:
                    check_book_uri(book=book)
                    search_results.append(book)
                with flask.current_app.app_context():
                    db.session.commit()

        to_search = [
            search_result_isbn,
            search_result_name,
            search_result_author,
            search_result_category,
            search_result_format
        ]

        search_results_append(to_search)

        def get_page(page):
            PAGE_LENGTH = 10

            # How the equation will work:
            # 1. Identify how many it's sent already
            #    (page * PAGE_LENGTH)
            # 2. Get PAGE_LENGTH books after the book
            #    last previously sent

            start_index = (page - 1) * PAGE_LENGTH
            end_index = start_index + PAGE_LENGTH
            
            #  Check if the end_index is larger than the actual list,
            #  if it is: 
            books = search_results[start_index:end_index]

            return books or []

        return {
            'status': 'success',
            'books': get_page(page)
        }