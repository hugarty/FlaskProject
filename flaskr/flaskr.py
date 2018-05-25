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
        if 'paginador' in request.args:
            dados = getPagina(request.args.get('paginador'))
            return jsonify(dados)
        if 'partidos' in request.args:
            dados = getPartidosPorSigla(request.args['partidos'])
            return jsonify(dados)
    
    if request.method == 'POST' :
        if request.form['cargo'] == 'Deputados':
            dados = getDeputadosPorNome(request.form['pesquisa'])
            print(dados)
            return render_template('principal.html', dados=dados)
        dados = getPartidosPorSigla(request.form['pesquisa'])
        return render_template('principal.html', dados=dados)

    return render_template('principal.html')



@app.route('/deputado/<string:deputadoId>')
def deputado(deputadoId):
    dados = getDeputadoPorId(deputadoId)
    if(temElementoEm(dados)):
        idPartido = dados[0]['uriPartido'][51:]
        return render_template('deputado.html', dado=dados[0], idPartido=idPartido)
    return redirect(url_for('naoEncontrado'))



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
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?itens='+size+'&ordenarPor=nome')
    return str(r['dados'])



@app.route('/naoEncontrado')
def naoEncontrado():
    return render_template('error.html', dado='SemDeputado')



@app.errorhandler(404)
def notFound(error):
    return render_template('error.html'), 404


#Caso queira pegar o nome do estado a siglado você pode 
#criar um rest full privado no firebase e dar get nele


# Não sei importar outro arquivo .py 
# Então vamos fingir que isso aqui é outra classe

# ------------------------------------------------------------------------------------


def getPagina (pagina):
    r = requests.get(pagina)
    dados = paginacao(r)
    return dados


def getDeputadosPorNome (nome, size = '30'):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?nome='+nome+'&itens='+size+'&ordenarPor=nome')
    dados = paginacao(r)
    return dados


def getDeputadoPorId (id):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?id='+id+'&idLegislatura=55&idLegislatura=54&idLegislatura=53&idLegislatura=52&idLegislatura=51&idLegislatura=50&ordem=ASC&ordenarPor=nome')
    return r.json()['dados']


def getDeputadoPorPartido (sigla):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?legislatura='+'55'+'&siglaPartido='+sigla)
    return r.json()['dados']


def getDeputadoPorEstado (sigla):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?legislatura='+'55'+'&siglaUf='+sigla)
    return r.json()['dados']


def getPartidosPorSigla (sigla):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/partidos?sigla='+sigla+'&itens=40&ordenarPor=sigla')
    return r.json()['dados']


def getPartidoPorId (id):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/partidos/'+id)
    return r.json()['dados']


def getEstados ():
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/referencias/uf')
    return r.json()['dados']


def temElementoEm (lista):
    if len(lista) > 0 :
        return True

def paginacao (r):
    dictPagina = dict()
    print('relações dessa página')
    for i in r.json()['links']:
        dictPagina[i['rel']] = i['href']
        print(i['rel'])

    dados = r.json()['dados']
    
    if temElementoEm(dados):
        if 'next' in dictPagina:
            dados[0]['linkNextPage'] = dictPagina['next']

        if 'previous' in dictPagina:
            dados[0]['linkPreviousPage'] = dictPagina['previous']

        if 'first' in dictPagina:
            dados[0]['linkFirstPage'] = dictPagina['first']

        if 'last' in dictPagina:
            dados[0]['linkLastPage'] = dictPagina['last']
    return dados