# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 01:01:36 2021

@author: Cristiano
"""
from docplex.mp.model import Model

opt_mod = Model(name = 'Linear Program')

data_file = open('dados.txt', 'r')

linhas = data_file.readlines()

ingredientes = []
elementos = []
demanda = 1000
custo = []
porcentagemMN = []
valores = []
minimo = []
maximo = []
limitante = []
limitanteMaxInf = []
limitanteMaxSup = []

#Ler cada linha do arquivo
for linha in linhas:
    linha = linha.split(' = ') # divido a linha entre nome do tipo de dado e os dados em si
    
    if linha[0] == 'Ingredientes':
        aux = linha[1]
        aux = aux.split('[')
        aux = aux[1]
        aux = aux.split(']')
        aux = aux[0]
        ing_lista = aux.split(', ')
        for ingrediente in ing_lista:
            ingredientes.append(str(ingrediente))
            
    if linha[0] == 'Elementos':
        aux = linha[1]
        aux = aux.split('[')
        aux = aux[1]
        aux = aux.split(']')
        aux = aux[0]
        el_lista = aux.split(', ')
        for elemento in el_lista:
            elementos.append(str(elemento))
    
    if linha[0] == 'Demanda':
        demanda = int(linha[1])
        
    if linha[0] == 'Custo':
        aux = linha[1]
        aux = aux.split('[')
        aux = aux[1]
        aux = aux.split(']')
        aux = aux[0]
        c_lista = aux.split(', ')
        for c in c_lista:
            custo.append(float(c))
            
    if linha[0] == 'PorcentagemMateriaNatural':
        aux = linha[1]
        aux = aux.split('[')
        aux = aux[1]
        aux = aux.split(']')
        aux = aux[0]
        porcent_lista = aux.split(', ')
        for p in porcent_lista:
            porcentagemMN.append(float(p))
            
    if linha[0] == 'Valores':
        aux = linha[1]
        aux = aux.split('[[')
        aux = aux[1]
        aux = aux.split(']]')
        aux = aux[0]
        valores_matriz = aux.split('], [')
        for item_lista in valores_matriz:
            lista_aux = []
            lista_val = item_lista.split(', ')
            for val in lista_val:
                lista_aux.append(float(val))
            valores.append(lista_aux)
    
    if linha[0] == 'Minimo':
        aux = linha[1]
        aux = aux.split('[')
        aux = aux[1]
        aux = aux.split(']')
        aux = aux[0]
        min_lista = aux.split(', ')
        for min_item in min_lista:
            minimo.append(float(min_item))
    
    if linha[0] == 'Maximo':
        aux = linha[1]
        aux = aux.split('[')
        aux = aux[1]
        aux = aux.split(']')
        aux = aux[0]
        max_lista = aux.split(', ')
        for max_item in max_lista:
            maximo.append(float(max_item))
            
    if linha[0] == 'Limitante':
        aux = linha[1]
        aux = aux.split('[')
        aux = aux[1]
        aux = aux.split(']')
        aux = aux[0]
        lim_lista = aux.split(', ')
        for lim in lim_lista:
            limitante.append(float(lim))
            
    if linha[0] == 'LimitanteMaximoInferior':
        aux = linha[1]
        aux = aux.split('[')
        aux = aux[1]
        aux = aux.split(']')
        aux = aux[0]
        limInf_lista = aux.split(', ')
        for limInf in limInf_lista:
            limitanteMaxInf.append(float(limInf))
    
    if linha[0] == 'LimitanteMaximoSuperior':
        aux = linha[1]
        aux = aux.split('[')
        aux = aux[1]
        aux = aux.split(']')
        aux = aux[0]
        limSup_lista = aux.split(', ')
        for limSup in limSup_lista:
            limitanteMaxSup.append(float(limSup))
            
'''
print('Ingredientes: ', ingredientes)
print('Elementos: ', elementos)
print('Demanda: ', demanda)
print('Custo: ', custo)
print('Porcentagens: ', porcentagemMN)
print('Valores: ', valores)
print('Minimo: ', minimo)
print('Maximo: ', maximo)
print('Limitante: ', limitante)
print('Limitante Inferior: ', limitanteMaxInf)
print('Limitante Superior: ', limitanteMaxSup)
'''
#Define as 19 variaveis de decisao
q = opt_mod.continuous_var_list(19)
#Cria a expressão da funcao objetivo
obj = opt_mod.sum((custo[i] * (q[i]/(porcentagemMN[i]/100))) for i in range(len(ingredientes)))

#Define as restricoes
left_c1 = opt_mod.sum(q[i] for i in range(len(ingredientes)))
right_c1 = demanda
c1 = opt_mod.add_constraint(left_c1 = right_c1, ctname='c1')

#Define a funcao objetivo
opt_mod.set_objective('min', obj)

