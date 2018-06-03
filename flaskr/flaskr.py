#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import pygal

from controllerFolder.controller import *
from flask import Flask, request, g, redirect, url_for, abort, \
     render_template, flash, jsonify



app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py.



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
            return render_template('principal.html', dados=dados)
        dados = getPartidosPorSigla(request.form['pesquisa'])
        return render_template('principal.html', dados=dados)

    return render_template('principal.html')



@app.route('/deputado/<string:deputadoId>')
def deputado(deputadoId):
    dados = getDeputadoPorId(deputadoId)
    return render_template('deputado.html', dado=dados)



@app.route('/partido/<string:partidoId>', methods=['GET'])
def partido(partidoId):
    if request.method == 'GET' and request.args:
        dados = getPagina(request.args.get('paginador'))
        return jsonify(dados)
    dados = getPartidoPorId(partidoId)
    membrosPartido = getDeputadoPorPartido(dados['sigla'])
    return render_template('partido.html', dados=dados, membrosPartido=membrosPartido) 



@app.route('/estado/<string:siglaEstado>', methods=['GET'])
def estado(siglaEstado):
    if request.method == 'GET' and request.args:
        dados = getPagina(request.args.get('paginador'))
        return jsonify(dados)
    dados = getDeputadoPorEstado(siglaEstado)
    return render_template('estado.html', membrosPartido=dados) 



@app.route('/proposicoesAutor/<string:idAutor>')
def proposicoesAutor (idAutor):
    dados = getProposicaoAutor(idAutor)
    return render_template('proposicaoAutor.html', dados=dados) 



@app.route('/proposicao/<string:idProposicao>')
def proposicao (idProposicao):
    dados = getProposicaoPorId(idProposicao)
    return render_template('proposicao.html', dados=dados) 



@app.errorhandler(404)
def notFound(error):
    return render_template('error.html'), 404


## -- Graph


@app.route('/graph/deputado', methods=['GET'])
def graph():
    if request.method == 'GET' and request.args:
        custom_style = pygal.style.Style(
            background='#202020',
            plot_background='#252525',
            foreground='#FFFFFF',
            foreground_strong='#FFFFFF',
            foreground_subtle='#000000',
            legend_font_size=22,
            label_font_size=18,
            major_label_font_size=16.5,
            title_font_size=25,
            opacity='.7',
            opacity_hover='.99',
            colors=('#FFFFAA', '#FF0000', '#FFFF00'))

        valores = getDeputadoGastosDoisUltimosMeses(request.args['deputado'])
        bar_chart = pygal.Bar(style=custom_style)
        bar_chart.title = 'Valores em Reais(R$)' 
        bar_chart.add(valores.get('mes1'), [ valores.get('valoresMes1')])
        bar_chart.add(valores.get('mes2'), [ valores.get('valoresMes2')])
        bar_chart.add('Total', [ valores.get('valoresMes1') + valores.get('valoresMes2')])

        return bar_chart.render()

