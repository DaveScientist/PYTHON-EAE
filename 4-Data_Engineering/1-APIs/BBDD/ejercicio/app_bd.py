from flask import Flask, request, jsonify
import sqlite3
import os

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/v1/resources/books/all', methods=['GET'])
def get_all():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    select_books = "SELECT * FROM books"
    result = cursor.execute(select_books).fetchall()
    connection.close()
    return jsonify(result)

# 1.Ruta para obtener el conteo de libros por autor ordenados de forma descendente
@app.route('/api/v1/resources/books/authors', methods=['GET'])
def count_authors():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    query = "SELECT author, count(author) as conteo FROM books GROUP BY 1 ORDER BY 2 DESC"
    result = cursor.execute(query).fetchall()
    connection.close()
    return jsonify(result)

# 2.Ruta para obtener los libros de un autor en la llamada
@app.route('/api/v1/resources/books/author', methods=['GET'])
def filter_author():
    author = request.args['author']
    author = '%' + author + '%'
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    query = '''SELECT * 
            FROM books 
            WHERE author LIKE ?
            '''
    result = cursor.execute(query, (author,)).fetchall()
    connection.close()    
    return jsonify(result)

# 3.Ruta para obtener los libros filtrados por title, publicación y autor
@app.route('/api/v1/resources/books/filters', methods=['GET'])
def filters():

    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    query = '''SELECT * 
            FROM books 
            WHERE
            '''
    to_filter = []
    if 'author' in request.args:
        author = request.args['author']
        author = '%' + author + '%'
        query += ' author LIKE ? AND' 
        to_filter.append(author)

    if 'year' in request.args:
        year = request.args['year']
        query += ' published = ? AND' 
        to_filter.append(year)
    
    if 'title' in request.args:
        title = request.args['title']
        title = '%' + title + '%'
        query += ' title LIKE ? AND'
        to_filter.append(title)
    
    if to_filter == []:
        return "No has seleccionado ningún filtro"

    query = query[:-4]+';'
    result = cursor.execute(query, to_filter).fetchall()
    connection.close()    
    return jsonify(result)

app.run()