#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

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
            print (dados[0])
            return render_template('deputados.html', dados=dados)
        
        elif request.form['cargo'] == 'Partidos' :
            dados = getPartidos(request.form['pesquisa'])
            return render_template('partidos.html', dados=dados)

        elif request.form['cargo'] == 'Estados' :
            dados = getEstados()
            return render_template('estados.html', dados=dados)

    return render_template('deputados.html')



@app.route('/deputado/<string:deputadoId>')
def deputado(deputadoId):
    dados = getDeputadoPorId(deputadoId)
    idPartido = dados[0]['uriPartido'][51:]
    return render_template('deputado.html', dado=dados[0], idPartido=idPartido)



@app.route('/partido/<string:partidoId>')
def partido(partidoId):
    dados = getPartidoPorId(partidoId)
    membrosPartido = getDeputadoPorPartido(dados['sigla'])
    return render_template('partido.html', dados=dados, membrosPartido=membrosPartido) 



@app.route('/estado/<string:siglaEstado>')
def estado(siglaEstado):
    dados = getDeputadoPorEstado(siglaEstado)
    return render_template('estado.html', membrosPartido=dados) 


#Caso queri pegar o nome do estado a siglado você pode 
#criar um rest full privado no firebase e dar get nele


# Não sei importar outro arquivo .py 
# Então vamos fingir que isso aqui é outra classe

# ------------------------------------------------------------------------------------


def getDeputadosPorNome (nome):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?nome='+nome+'&itens=30&ordenarPor=nome').json()
    return r['dados']


def getDeputadoPorId (id):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?id='+id+'&ordenarPor=nome').json()
    return r['dados']


def getDeputadoPorPartido (sigla):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?legislatura='+'55'+'&siglaPartido='+sigla).json()
    return r['dados']


def getDeputadoPorEstado (sigla):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?legislatura='+'55'+'&siglaUf='+sigla).json()
    return r['dados']


def getPartidos (nome):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/partidos?itens=40&ordenarPor=sigla').json()
    return r['dados']


def getPartidoPorId (id):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/partidos/'+id).json()
    return r['dados']


def getEstados ():
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/referencias/uf').json()
    return r['dados']






