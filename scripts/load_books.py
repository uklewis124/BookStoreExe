import os
import pandas as pd
from sqlalchemy import text
from scripts.prepare_database import db, Books  # Replace with the actual package containing `db`
from flask import current_app


def load_books():
    """
    Load books into the 'books' table by replacing rows but keeping existing columns.
    """
    global df

    # Load CSV file
    csv_location = f"{os.getcwd()}\\instance\\main_dataset.csv"
    df = pd.read_csv(csv_location)

    # Establish Flask application context
    app = current_app
    with app.app_context():
        # Remove all existing rows, but keep columns
        Books.query.delete()  # will this delete all rows?
        db.session.commit()

        # Append new rows to the table
        df.to_sql('books', db.engine, if_exists='append', index=True)