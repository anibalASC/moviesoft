from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/anibal/Documentos/projects/moviesoft/baseMovie.db'
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    category = db.Column(db.String(80), unique=False, nullable=False)
    director = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<id:%r>' % self.id

@app.route('/movies/', methods=['GET', 'POST'])
def movie():
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        category = request.form['category']
        director = request.form['director']
        movie = Movie(name=name, year=year, category=category, director=director)
        db.session.add(movie)
        db.session.commit()
        return 'pelicula creada'
    elif request.method == 'GET':
        print(Movie.query.all())
        return render_template('index.html', movies=Movie.query.all())




@app.route('/movies/<int:id>', methods=['GET'])
def search(id):
    movie_search = Movie.query.filter_by(id=id).first()
    if movie_search:
        return render_template('search.html', movie=movie_search)
    return "pelicula no encontrada"



@app.route('/movies/<int:id>', methods=['DELETE'])
def delete(id):
    movie_delete = Movie.query.filter_by(id=id).first()
    if request.method == 'DELETE':
        db.session.delete(movie_delete)
        db.session.commit()
        return "la pelicula se elimino"

@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update(movie_id):
    if request.method == 'PUT':
        movie_update = list(filter(lambda x: x['id'] == movie_id))
        if request.form['name'] != '':
            movie_update[0]['name'] = request.form['name']
        if request.form['year'] != '':
            movie_update[0]['year'] = request.form['year']
        if request.form['category'] != '':
            movie_update[0]['category'] = request.form['category']
        if request.form['director'] != '':
            movie_update[0]['director'] = request.form['director']
        database.append(movie_update)
    return jsonify(database)







#
    # movie_update = list(filter(lambda x: x['id'] == movie_id, database))
    # database.update(new_database)
    # print(movie_update)
    # return jsonify(new_database)
#modificar el valor


if __name__=='__main__':
    app.run(debug = True, port = 8080)
