from flask import Flask, request, render_template, jsonify
from elasticsearch import Elasticsearch
from time import sleep, time
import json
import os
import requests

es = Elasticsearch(hosts='localhost:9200')
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/users1/<name>')
def print(name):
    return 'This is ' + name


@app.route('/users')
def get_name_suername():
    # http://localhost:5000/users?name=lenin&surname=falconi
    name = request.args.get('name')  # substitute parenthesis by [] to force to input a data
    surname = request.args.get('surname')
    return 'This is {} {}'.format(name, surname)


@app.route('/indexar_demo/', methods=['GET', 'POST'])
def create_demo_index():
    index_name = request.form.get('index_name')
    doc_type = request.form.get('doc_type')
    if index_name and doc_type is not None:
        r = requests.get('http://localhost:9200')
        i = 1
        while r.status_code == 200:
            if i != 17:  # problema con elemento 17 de la base
                r = requests.get('http://swapi.co/api/people/' + str(i))
                resp = es.index(index=index_name, doc_type=doc_type, id=i, body=json.loads(r.content))
            i = i + 1
        return render_template('indexing_demo.html', dato=i, response=resp)

    print('indice {} creado'.format(index_name))
    return render_template('indexing_demo.html')


@app.route('/read', methods=['GET', 'POST'])
def read_data():
    id_number = request.form.get('id_number')  # substitute with args to work with postman as in: request.args.get
    doc_type = request.form.get('doc_type')
    index_name = request.form.get('index_name')
    try:
        resp = es.get(index=index_name, doc_type=doc_type, id=id_number)

    except:
        resp = {'_source': {'texto': 'Esto se jodio'}}
    return render_template('read_demo.html', resultado=resp)


@app.route('/insert', methods=['GET', 'POST'])
def insert_data():
    doc1 = {'name': request.form.get("name"),
            'height': request.form.get("height"),
            'mass': request.form.get("mass"),
            'hair_color': request.form.get("hair_color"),
            'skin_color': request.form.get("skin_color"),
            'eye_color': request.form.get("eye_color"),
            'birth_year': request.form.get("birth_year"),
            # 'gender': request.form.get("gender"),
            # 'homeworld': request.form.get("homeworld"),
            # 'vehicles': request.form.get("vehicles")
            }
    id_number = request.form.get('id_number')  # substitute with args to work with postman as in: request.args.get
    doc_type = request.form.get('doc_type')
    index_name = request.form.get('index_name')

    try:
        resp = es.index(index=index_name, doc_type=doc_type, body=doc1, id=id_number)
    except:
        resp = {'estado': 'dato no agregado'}

    return render_template('insert_demo.html', response=resp)


@app.route('/update', methods=['GET', 'POST'])
def update():
    id_number = request.form.get('id_number')  # substitute with args to work with postman as in: request.args.get
    doc_type = request.form.get('doc_type')
    index_name = request.form.get('index_name')

    timestamp = int(time())
    source_to_update = {

        "doc": {
            "year": 2014,
            "grade": "Grade 3",
            "timestamp": timestamp  # integer of epoch time
        }
    }

    doc1 = {"doc": {
                    request.form.get("field_name"): request.form.get("field_value"),
                    "timestamp": timestamp
                  }
    }
    try:
        resp = es.update(index=index_name, doc_type=doc_type, body=doc1, id=id_number)
    except:
        resp = {'estado': 'dato no actualizado'}
    return render_template('update_demo.html', response=resp)


@app.route('/search', methods=['GET', 'POST'])
def search():
    index_name = request.form.get('index_name')
    search_string = request.form.get('search_string')

    try:
        resp = es.search(index=index_name,
                         # body={"query": {"query_string": {"query": search_string, "default_field": "name"}}}
                         body={"query":{"match":{"name":search_string}}}
                         )

    except:
        resp = {'hits': {'total': {'value': 0}, 'hits': {'_id': '404', '_source': {'name': 'NOBODY'}}}}
    return render_template('search_demo.html', resultado=resp)


@app.route('/delete_document', methods=['GET', 'POST'])
def delete_document():
    id_number = request.form.get('id_number')
    index_name = request.form.get('index_name')
    try:
        if es.exists(index=index_name, id=id_number):
            resp = es.delete(index=index_name, id=id_number)

        else:
            resp = {'Status': 'document not found.'}
    except:
        resp = {'Status': 'document not found.'}
    return render_template('delete_document.html', response=resp)


@app.route('/delete_index', methods=['GET', 'POST'])
def delete_index():
    index_name = request.form.get('index_name')
    try:
        resp = es.indices.delete(index=index_name)

    except:
        resp = {'Status': 'Type an index name please'}
    return render_template('delete_index.html', response=resp)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
