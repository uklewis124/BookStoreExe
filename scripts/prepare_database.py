from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from sqlalchemy import create_engine
import pandas as pd
import os

db = SQLAlchemy()

class Books(db.Model):
    __tablename__ = "books"

    index = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    image_uri = db.Column(db.String)
    name = db.Column(db.String)
    author = db.Column(db.String)
    format = db.Column(db.String)
    book_depository_stars = db.Column(db.Float)
    price = db.Column(db.String)
    currency = db.Column(db.String)
    old_price = db.Column(db.Float)
    isbn = db.Column(db.Integer, unique=True)
    category = db.Column(db.String)
    img_paths = db.Column(db.String)

def load_books():
    global df

    csv_location = f"{os.getcwd()}\\instance\\main_dataset.csv"
    df = pd.read_csv(csv_location)

    df.to_sql('books', db.engine, if_exists='replace', index=True)

def load_db_after_server():
    ## Runs once DB is setup
    load_books()
