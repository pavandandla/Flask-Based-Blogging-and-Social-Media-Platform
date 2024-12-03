from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()

def init_db(app):
    # Set the SQLAlchemy database URI and other configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the database with the app
    db.init_app(app)

    # Use the provided app instance to create the database tables
    with app.app_context():
        db.create_all()
