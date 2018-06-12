import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/anibal/Documentos/projects/moviesoft/static/image'
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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

                                        ###Add movie###
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


#                                        ###search movie###
@app.route('/movies/<int:id>', methods=['GET'])
def search(id):
    movie_search = Movie.query.get(id)
    if movie_search:
        return render_template('search.html', movie=movie_search)
    return "pelicula no encontrada"

                                        ####delete movie###
@app.route('/movies/delete/<int:id>',)
def delete(id):
    movie_delete = Movie.query.filter_by(id=id).first()
    db.session.delete(movie_delete)
    db.session.commit()
    return redirect(url_for('movie'))


                                        ###update###
@app.route('/movies/<int:movie_id>', methods=['GET', 'PATCH'])
def update(movie_id):
    movie_update = Movie.query.get(movie_id)
    if request.method == 'GET':
        return render_template('search.html', movie=movie_update)
    if request.method == b'PATCH':

        if movie_update.name != request.form['name']:
            movie_update.name = request.form['name']

        if movie_update.year != request.form['year']:
            movie_update.year = request.form['year']

        if movie_update.category != request.form['category']:
            movie_update.category = request.form['category']

        if movie_update.director != request.form['director']:
            movie_update.director = request.form['director']

        if movie_update.distributed != request.form['distributed']:
            movie_update.distributed = request.form['distributed']

        if movie_update.image != request.file['image']:
            movie.update.image = request.file['image']
        db.session.commit()
        return redirect(url_for('movie'))
    # return jsonify(database)


if __name__=='__main__':
    app.run(debug = True, port = 8080)
