from flask import Flask, request, jsonify

database = []

app = Flask(__name__)


@app.route('/movies', methods=['GET', 'POST'])
def movie():
    if request.method == 'POST':
        id = len(database) + 1
        name = request.form['name']
        year = request.form['year']
        category = request.form['category']
        director = request.form['director']
        movie = {"id":id,"name":name,"year":year,"category":category,"director":director}
        database.append(movie)
        print(movie)

        return jsonify(movie)
    return jsonify(database)

@app.route('/movies/<int:movie_id>', methods=['GET'])
def search(movie_id):
    movie_filter = list(filter(lambda x: x['id'] == movie_id, database))
    print(movie_filter)
    return jsonify(movie_filter)



@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete(movie_id):
    movie_remove = list(filter(lambda x: x['id'] == movie_id, database))
    database.remove(movie_remove[0])
    print(movie_remove)
    return jsonify(database)

@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update(movie_id):
    if request.method == 'POST':
        movie_update = list(filter(lambda x: x['id'] == movie_id, database))
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







# garaje = []
# coche1 = {'marca': 'Renault', 'color': 'rojo', 'combustible': 'gasoil'}
# coche2 = {'marca': 'Renault', 'color': 'verde', 'combustible': 'gasolina'}
# coche3 = {'marca': 'Mercedes', 'color': 'gris metalizado', 'combustible': 'gasolina'}
# garaje.append(coche1)
# garaje.append(coche2)
# garaje.append(coche3)
# for i in garaje:
#     print(i['marca'], i['color'], i['combustible'])
    # movie_update = list(filter(lambda x: x['id'] == movie_id, database))
    # database.update(new_database)
    # print(movie_update)
    # return jsonify(new_database)
#modificar el valor




app.run(debug = True, port = 8080)
