from flask import Blueprint, render_template, request, jsonify, current_app, redirect
import stripe

donate_bp = Blueprint('donate', __name__)

@donate_bp.route('/donate/')
def donate_route():
    return render_template('donate.html')

@donate_bp.route('/payment/')
def process_payment():
    amount = 30
    currency = 'gbp'
    automatic_payment_methods = {"enabled": True}
    
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        automatic_payment_methods=automatic_payment_methods
    )
    
    return render_template('checkout.html', client_secret=intent.client_secret)

