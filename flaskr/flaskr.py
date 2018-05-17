#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import requests
from flask import Flask, request, g, redirect, url_for, abort, \
     render_template, flash, jsonify

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'GET' and request.args:
        if 'deputados' in request.args :
            dados = getDeputadosPorNome(request.args['deputados'])
            return jsonify(dados)
        if 'partidos' in request.args:
            dados = getPartidosPorSigla(request.args['partidos'])
            return jsonify(dados)
    
    if request.method == 'POST' :
        if request.form['cargo'] == 'Deputados':
            dados = getDeputadosPorNome(request.form['pesquisa'])
            return render_template('principal.html', dados=dados)
        dados = getPartidosPorSigla(request.form['pesquisa'])
        return render_template('principal.html', dados=dados)
    return render_template('principal.html')


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

@app.route('/mostrar/<string:size>')
def mostrarMais (size = '10'):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?itens='+size+'&ordenarPor=nome').json()
    return str(r['dados'])
   

#Caso queri pegar o nome do estado a siglado você pode 
#criar um rest full privado no firebase e dar get nele


# Não sei importar outro arquivo .py 
# Então vamos fingir que isso aqui é outra classe

# ------------------------------------------------------------------------------------


def getDeputadosPorNome (nome, size = '3'):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?nome='+nome+'&itens='+size+'&ordenarPor=nome').json()
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


def getPartidosPorSigla (sigla):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/partidos?sigla='+sigla+'&itens=40&ordenarPor=sigla').json()
    return r['dados']


def getPartidoPorId (id):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/partidos/'+id).json()
    return r['dados']


def getEstados ():
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/referencias/uf').json()
    return r['dados']