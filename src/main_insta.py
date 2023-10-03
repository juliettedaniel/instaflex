import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import app, db


# Get the current directory
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'insta.flex.db')

# Create the Flask application instance
# app = Flask(__name__)

# Load the configuration from the config.py file
app.config.from_pyfile('config.py')

# Set the SQLite database file path
#'sqlite:///instaflex.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instaflex.db')

# Set up the database connection
db.init_app(app)
with app.app_context():
    db.create_all()

# Define a basic route
@app.route('/')
def hello():
    return 'Hello, Flask!'

# Print the value of SQLALCHEMY_DATABASE_URI
print(app.config['SQLALCHEMY_DATABASE_URI'])

# Run the Flask app
if __name__ == '__main__':
    app.run()