import os
import sqlite3
import requests

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py


@app.route('/', methods=['POST', 'GET'])
def index():
    
    if request.method == 'POST':
        if request.form['pesquisa'] != '':
            r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?nome='+request.form['pesquisa']+'&ordenarPor=nome').json()
            print(r['dados'][0])
#            print(r['dados'].length)
#            print('https://dadosabertos.camara.leg.br/api/v2/deputados?nome=Rogerio&ordenarPor=nome')
        else:
            print('Não tem nome')

        # print(request.form['infoDeputadosSenadores'])
        # print(request.form['infoPartidos'])
        # print(request.form['cargo'])
    
    return render_template('index.html')
