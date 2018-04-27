import os
import requests

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash



app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print(request.form['cargo'])
        print(request.form['pesquisa'])
        
        if request.form['cargo'] == 'Deputados' :
            dados = getDeputadosPorNome(request.form['pesquisa'])
            return render_template('deputados.html', dados=dados)
        
        elif request.form['cargo'] == 'Partidos' :
            dados = getPartidos(request.form['pesquisa'])
            return render_template('partidos.html', dados=dados)

        elif request.form['cargo'] == 'Estados' :
            dados = getEstados()
            return render_template('estados.html', dados=dados)

    return render_template('index.html')



@app.route('/deputado/<string:deputadoId>')
def deputado(deputadoId):
    dados = getDeputadoPorId(deputadoId)
    return render_template('deputado.html', dados=dados)


@app.route('/partido/<string:partidoId>')
def partido(partidoId):
    dados = getPartidoPorId(partidoId)
    return render_template('partido.html', dados=dados)
    # return '%s' % partidoId




#def detalhesDeputadoSenador ():

# Não sei importar outro arquivo .py 
# Então vamos fingir que isso aqui é outra classe

# ------------------------------------------------------------------------------------


def getDeputadosPorNome (nome):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?nome='+nome+'&ordenarPor=nome').json()
    return r['dados']


def getDeputadoPorId (id):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?id='+id+'&ordenarPor=nome').json()
    return r['dados']


def getPartidos (nome):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/partidos?nome='+nome+'&ordenarPor=sigla').json()
    return r['dados']


def getPartidoPorId (id):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/partidos/'+id).json()
    return r['dados']


def getEstados ():
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/referencias/uf').json()
    return r['dados']