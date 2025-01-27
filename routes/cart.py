import json

from flask import Blueprint, request, jsonify, session

from scripts.prepare_database import Books

cart = Blueprint('cart', __name__)

@cart.route('/api/v1/cart/')
def cart_index():
    if session.get('cart'):
        return jsonify({
            "Status": "Success",
            "Message": "Cart contents retrieved",
            "Cart": session['cart']
        }), 200
    else:
        return jsonify({
            "Status": "Success",
            "Message": "Cart is empty"
        })

@cart.route('/api/v1/cart/add/', methods=['POST'])
def cart_add():
    # 1. check if there is a book.index in response
    # 2. check the index is valid and actually points to a book
    # 3. add item to cart dictionary in flask sessions

    # 1. check if there is a book.index in response
    data = request.get_json()
    book_index = data.get('bookId')
    if book_index is None:
        return jsonify({
            "Status": "Failed",
            "Error": "No book index provided"
        }), 400

    db_book = Books.query.filter_by(index=book_index).first()
    if not db_book:
        return jsonify({
            "Status": "Failed",
            "Error": "Book not found"
        }), 404
    
    def get_book_details(book):
        return {
            "index": book.index,
            "image": book.image,
            "name": book.name,
            "author": book.author,
            "format": book.format,
            "book_depository_stars": book.book_depository_stars,
            "price": book.price,
            "currency": book.currency,
            "old_price": book.old_price,
            "isbn": book.isbn,
            "category": book.category,
            "img_paths": book.img_paths,
        }

    if session.get('cart'):
        old_session = session['cart']


        # 1. Check if book already in cart
        for book in old_session:
            print(book)
            if book['index'] == db_book.index:
                book['quantity'] += 1
                session['cart'] = old_session
                return jsonify({
                    "Status": "Success",
                    "Message": "Book quantity increased",
                    "BookDetails": get_book_details(db_book)
                }), 200

        # No book currently in database -> Add book with quantity as 1
        book_details = get_book_details(db_book)
        book_details['quantity'] = 1
        old_session.append(book_details)
        session['cart'] = old_session
    else:
        book_details = get_book_details(db_book)
        book_details['quantity'] = 1
        session['cart'] = [book_details]
    return jsonify({
        "Status": "Success",
        "Message": "Book added to cart",
        "BookDetails": get_book_details(db_book)
    }), 200

@cart.route('/api/v1/cart/remove/', methods=['POST'])
def cart_remove():
    # 1. Check if they have provided a book index to remove
    # 2. Check if that book is in the cart
    # 3. Delete book from cart if quantity == 1
    # 4. -= quantity if quantity > 1

    try:
        # 1.
        data = request.get_json()
        book_index = data.get('bookId')
        if book_index is None:
            return jsonify({
                "Status": "Failed",
                "Error": "No book index provided"
            }), 400

        # 2.
        book = None
        cart_i: int = None
        old_session = session['cart']
        for i, b in enumerate(old_session):
            if b['index'] == book_index:
                cart_i = i
                book = b
                break

        if not book:
            return jsonify({
                "Status": "Failed",
                "Error": "Book not found in cart"
            }), 404

        # 3.
        if book['quantity'] == 1:
            old_session[cart_i].remove()
            session['cart'] = old_session
            return jsonify({
                "Status": "Success",
                "Message": "Book removed from cart"
            }), 200

        # 4.
        old_session[cart_i]['quantity'] -= 1
        session['cart'] = old_session
        return jsonify({
            "Status": "Success",
            "Message": "Book quantity decreased",
            "BookDetails": book
        })
    except Exception as e:
        return jsonify({
            "Status": "Failed",
            "Message": "An unknown error occurred",
            "Error": str(e)
        })
