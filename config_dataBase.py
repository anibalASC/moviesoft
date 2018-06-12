from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/anibal/Documentos/projects/moviesoft/baseMovie.db'
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    year = db.Column(db.DateTime, unique=False, nullable=False)
    category = db.Column(db.String(80), unique=False, nullable=False)
    director = db.Column(db.String(80), unique=False, nullable=False)
    distributed  = db.Column(db.String(80), unique=False, nullable=False)
    image = db.Column(db.String(80), unique=False)

    def __repr__(self):
        return '<id: %r>' % self.id

db.session.commit()
