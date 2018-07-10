import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_wtf import Form
from forms import RegistrationForms
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/anibal/Documentos/projects/moviesoft/static'
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])

app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# modus = Modus(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/anibal/Documentos/projects/moviesoft/baseMovie.db'
app.config['SECRET_KEY']='ESTA ES LA LLAVE'
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    category = db.Column(db.String(80), unique=False, nullable=False)
    director = db.Column(db.String(80), unique=False, nullable=False)
    distributed  = db.Column(db.String(80), unique=False, nullable=False)
    sinopsis = db.Column(db.String(200), unique=False, nullable=False)
    image = db.Column(db.String(80), unique=False)

    def __repr__(self):
        return '<id:%r>' % self.id

class formDatos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=False, nullable=False)
    email = db.Column(db.String(35), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)

##############################################Routes User#################################################
##############################################list DB user################################################
@app.route('/listUser', methods=['GET', 'POST'])
def userlist():
    usuarios = formDatos.query.all()
    print(usuarios[0].username)
    email =formDatos.query.all()
    return render_template('vistaUsuario.html', usuarios=usuarios, email=email)

###############################################Add user###################################################
@app.route('/registers/', methods=['GET', 'POST'])
def register():
    form = RegistrationForms(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']      
        user = formDatos(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for Registering')
        return redirect(url_for('register'))
    elif request.method == 'GET':
        print(formDatos.query.all())
        return render_template('register.html', form=form)

################################################delete user#########################################
@app.route('/listUser/delete/<int:id>')
def deluser(id):
    user_delete = formDatos.query.filter_by(id=id).first()
    db.session.delete(user_delete)
    db.session.commit()
    return redirect(url_for('userlist'))

#################################################update user########################################


####################################################################################################
#################################################routes#############################################

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')

@app.route('/newMovie',  methods=['GET', 'POST'])
def newMovie():
    return render_template('newMovie.html')


@app.route('/viewMovies', methods=['GET', 'POST'])
def viewMovie():
    return render_template('viewMovies.html', movies=Movie.query.all())

@app.route('/moviesInfo/<int:id>', methods=['GET'])
def movieInfo(id):
    movie_info = Movie.query.filter_by(id=id).first()
    if movie_info:
        return render_template('movie_Info.html', movies=movie_info)
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
        sinopsis  = request.form['sinopsis']
        image = request.files['image']
        image_name = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
        movie = Movie(name=name, year=year, category=category, director=director, distributed=distributed, sinopsis=sinopsis, image=image_name)
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
    # if request.method == 'POST':
    movie_update.name = request.form['name']
    movie_update.year = request.form['year']
    movie_update.category = request.form['category']
    movie_update.director = request.form['director']
    movie_update.distributed = request.form['distributed']
    movie_update.sinopsis = request.form['sinopsis']
    if not 'image' in request.files:
        return render_template('search.html', movie=movie_update)
    movie_new_image = request.files['image']
    if 'image' in request.files:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], movie_update.image))
        image_name = secure_filename(movie_new_image.filename)
        movie_update.image = image_name
        movie_new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
    db.session.commit()
    return render_template('search.html', movie=movie_update)



if __name__=='__main__':
    app.run(debug = True, port = 8080)

