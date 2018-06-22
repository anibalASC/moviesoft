import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
# from flask_modus import Modus
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/anibal/Documentos/projects/moviesoft/static'
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])

app = Flask(__name__)
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# modus = Modus(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/anibal/Documentos/projects/moviesoft/baseMovie.db'
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    category = db.Column(db.String(80), unique=False, nullable=False)
    director = db.Column(db.String(80), unique=False, nullable=False)
    distributed  = db.Column(db.String(80), unique=False, nullable=False)
    image = db.Column(db.String(80), unique=False)

    def __repr__(self):
        return '<id:%r>' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')

@app.route('/newMovie',  methods=['GET', 'POST'])
def newMovie():
    return render_template('newMovie.html')

@app.route('/viewMovies', methods=['GET', 'POST'])
def viewMovie():
    return render_template('viewMovies.html', movies=Movie.query.all())

@app.route('/moviesInfo/<int:id>', methods=['GET', 'POST'])
def movieInfo():
    movie_info = Movie.query.filter_by(id=id).first()
    if movie_info:
        return render_template('movie_Info.html', movies=Movie.query.all())
    return "pelicula no encontrada"

###############################################Add movie###############################################
@app.route('/movies/', methods=['GET', 'POST'])
def movie():
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        category = request.form['category']
        director = request.form['director']
        distributed = request.form['distributed']
        image = request.files['image']
        image_name = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
        movie = Movie(name=name, year=year, category=category, director=director, distributed=distributed, image=image_name)
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('movie'))
    elif request.method == 'GET':
        print(Movie.query.all())
        return render_template('index.html', movies=Movie.query.all())


###############################################search movie###############################################
@app.route('/movies/<int:id>', methods=['GET'])
def search(id):
    movie_search = Movie.query.filter_by(id=id).first()
    # movie_search = Movie.query.get(id)
    if movie_search:
        return render_template('search.html', movie=movie_search)
    return "pelicula no encontrada"


###############################################delete movie###############################################
@app.route('/movies/delete/<int:id>',)
def delete(id):
    movie_delete = Movie.query.filter_by(id=id).first()
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], movie_delete.image))
    db.session.delete(movie_delete)
    db.session.commit()
    return redirect(url_for('movie'))


###############################################update movie###############################################

@app.route('/moviesSearch/<int:movie_id>', methods=['GET', 'POST'])
def update(movie_id):
    movie_update = Movie.query.filter_by(id=movie_id).first()
    if request.method == 'GET':
        return render_template('search.html', movie=movie_update)
    if request.method == 'POST':
        movie_update.name = request.form['name']
        movie_update.year = request.form['year']
        movie_update.category = request.form['category']
        movie_update.director = request.form['director']
        movie_update.distributed = request.form['distributed']
        print(request.files['image'])
        if 'image' in request.files:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], movie_update.image))
            image = request.files['image']
            print('image')
            image_name = secure_filename(image.filename)
            print('image_name')
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
        db.session.commit()
        return render_template('search.html', movie=movie_update)



if __name__=='__main__':
    app.run(debug = True, port = 8080)


























# @app.route('/movies/<int:movie_id>', methods=['GET', 'POST'])
# def update(movie_id):
#     movie_update = Movie.query.filter_by(id=id).first()
#     if request.method == 'GET':
#         return render_template('search.html', movie=movie_update)
#     movie_update.name = request.form['name']
#     movie_update.year = request.form['year']
#     movie_update.category = request.form['category']
#     movie_update.director = request.form['director']
#     movie_update.distributed = request.form['distributed']
#     print(request.files['image'])
#     if 'image' in request.files:
#         os.remove(os.path.join(app.config['UPLOAD_FOLDER'], movie_update.image))
#         image = request.files['image']
#         print('image')
#         image_name = secure_filename(image.filename)
#         print('image_name')
#         image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
#     db.session.commit()
#     return render_template('search.html', movie=movie_update)
        # return redirect(url_for('movie'))
    # return jsonify(database)


