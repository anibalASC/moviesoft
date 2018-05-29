from flask import Flask, request, jsonify
app = Flask(__name__)

database = []


@app.route('/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'POST':
        name = (request.form['name'])
        year = (request.form['year'])
        category = (request.form['category'])
        director = (request.form['director'])
        movie = {"name":name, "year":year, "category":category, "director":director}
        database.append(movie)
        print(movie)
        return jsonify(movie)
        # return "Metodo POST"
    elif request.method == 'GET':
        return jsonify(database)

# def delete_movies():
#     if




app.run(debug = True, port = 8080)
