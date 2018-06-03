#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import requests, datetime


# Paginador
def getPagina (pagina):
    r = requests.get(pagina)
    dados = paginacao(r)
    return dados


def getDeputadosPorNome (nome, size = '30'):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?nome='+nome+'&itens='+size+'&ordenarPor=nome')
    dados = paginacao(r)
    return dados


def getDeputadoPorId (id):
    dados = infoDeputado(id)
    return dados


def getDeputadoPorEstado (sigla, size = '30'):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?legislatura='+'55'+'&siglaUf='+sigla+'&itens='+size)
    dados = paginacao(r)
    dados = getIdPartidoDeCadaDeputado(dados)
    return dados

    
def getDeputadoPorPartido (sigla, size = '30'):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?legislatura='+'55'+'&siglaPartido='+sigla+'&itens='+size)
    dados = paginacao(r)
    return dados


def getPartidosPorSigla (sigla):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/partidos?sigla='+sigla+'&itens=40&ordenarPor=sigla')
    return checkSiglaPartido(r)


def getPartidoPorId (id):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/partidos/'+id)
    return r.json()['dados']


def getProposicaoAutor(id):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/proposicoes?idAutor='+id+'&ordem=ASC&ordenarPor=id&itens=50')
    return r.json()['dados']


def getProposicaoPorId(id):
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/proposicoes/'+id)
    return r.json()['dados']


def getEstados ():
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/referencias/uf')
    return r.json()['dados']


# ------


def checkSiglaPartido (r):
    if len(r.json()['dados']) > 0:
        return r.json()['dados']
    return [{'semDados': 'semDados'}]


def infoDeputado(id):
    dados = dict()
    partidos  = []
    
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?id='+id+'&idLegislatura=56&idLegislatura=55&idLegislatura=54&idLegislatura=53&idLegislatura=52&idLegislatura=51&idLegislatura=50&ordem=ASC&ordenarPor=idLegislatura')
    r2 = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados/'+id)

    if r2.status_code == 200:
        for i in r.json()['dados']:
            partidos.append(i['siglaPartido'])
        dados['qtLegislatura'] = len(r.json()['dados'])
        dados['anosLegislando'] = dados['qtLegislatura'] * 4
        dados['partidos'] = partidos
        dados['geral'] = r2.json()['dados']
        dados['idPartido'] = r2.json()['dados']['ultimoStatus']['uriPartido'][51:]
    return dados



def paginacao (r):
    dictPagina = dict()
    for i in r.json()['links']:
        dictPagina[i['rel']] = i['href']

    dados = r.json()['dados']
    
    if len(dados) > 0:
        if 'next' in dictPagina:
            dados[0]['linkNextPage'] = dictPagina['next']

        if 'previous' in dictPagina:
            dados[0]['linkPreviousPage'] = dictPagina['previous']

        if 'first' in dictPagina:
            dados[0]['linkFirstPage'] = dictPagina['first']

        if 'last' in dictPagina:
            dados[0]['linkLastPage'] = dictPagina['last']
    return dados


def getIdPartidoDeCadaDeputado(r):
    if len(r) > 0:
        dados = r
        for x in dados:
            x['uriPartido'] =  x['uriPartido'][51:]
    return dados






# -- Pygal Graficos

def getDeputadoGastosDoisUltimosMeses( idDeputado):
    valores = dict()
    mes1 = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
    mes2 = datetime.date.today().replace(day=1, month=mes1.month) - datetime.timedelta(days=1)
    r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados/'+idDeputado+'/despesas?ano='+str(mes1.year)+'&ano='+str(mes2.year)+'&mes='+str(mes1.month)+'&mes='+str(mes2.month)+'&itens=100&ordem=DESC&ordenarPor=mes')
    somaMes1 = 0
    somaMes2 = 0
    
    for i in r.json()['dados']:
        if str(i['mes']) == str(mes1.month):
            somaMes1 = somaMes1 + i['valorLiquido']
        else:
            somaMes2 = somaMes2 + i['valorLiquido']

    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 
        'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    valores.update({'mes1':meses[mes1.month - 1]})  
    valores.update({'mes2':meses[mes2.month - 1]})
    valores.update({'valoresMes1':somaMes1})
    valores.update({'valoresMes2':somaMes2})
    return valores
