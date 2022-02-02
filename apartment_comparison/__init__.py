from flask import Flask
from apartment_comparison.db_manager import ApartmentsDBManager

db = ApartmentsDBManager('apartments.db')
db.execute_sql_file('apartment_comparison/static/sql/create_tables.sql')


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    with app.app_context():
        from apartment_comparison import routes
    return app
