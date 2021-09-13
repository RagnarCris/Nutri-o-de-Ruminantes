# -*- coding: utf-8 -*-
"""
@author: Cristiano e Matheus
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

#Define as 19 variaveis de decisao
q = opt_mod.continuous_var_list(len(ingredientes), lb=0.0)
#Cria a expressão da funcao objetivo
obj = sum((custo[i] * (q[i]/(porcentagemMN[i]/100))) for i in range(len(ingredientes)))

#Define as restricoes
left_c1 = sum(q[i] for i in range(len(ingredientes)))
right_c1 = demanda
opt_mod.add_constraint(left_c1 == right_c1, ctname='c1')

#Restricoes dos ingredientes
opt_mod.add_constraints(q[i] >= (minimo[i]/100)*demanda for i in range(len(ingredientes)))

opt_mod.add_constraints(q[i] <= (maximo[i]/100)*demanda for i in range(len(ingredientes)))

#Restricoes dos elementos
left_c2 = sum((valores[i][elementos.index('PB')]/100)*q[i] for i in range(len(ingredientes)))
right_c2 = ((limitante[elementos.index('PB')]/100)*demanda - ((limitanteMaxInf[elementos.index('PB')]/100)*(limitante[elementos.index('PB')]/100)*demanda))
opt_mod.add_constraint(left_c2 >= right_c2, ctname='c2')

left_c3 = sum((valores[i][elementos.index('PB')]/100)*q[i] for i in range(len(ingredientes)))
right_c3 = ((limitante[elementos.index('PB')]/100)*demanda + ((limitanteMaxSup[elementos.index('PB')]/100)*(limitante[elementos.index('PB')]/100)*demanda))
opt_mod.add_constraint(left_c3 <= right_c3, ctname='c3')

left_c4 = sum((valores[i][elementos.index('NDT')]/100)*q[i] for i in range(len(ingredientes)))
right_c4 = ((limitante[elementos.index('NDT')]/100)*demanda - ((limitanteMaxInf[elementos.index('NDT')]/100)*(limitante[elementos.index('NDT')]/100)*demanda))
opt_mod.add_constraint(left_c4 >= right_c4, ctname='c4')

left_c5 = sum((valores[i][elementos.index('NDT')]/100)*q[i] for i in range(len(ingredientes)))
right_c5 =  ((limitante[elementos.index('NDT')]/100)*demanda + ((limitanteMaxSup[elementos.index('NDT')]/100)*(limitante[elementos.index('NDT')]/100)*demanda))
opt_mod.add_constraint(left_c5 <= right_c5, ctname='c5')

left_c6 = sum((valores[i][elementos.index('PDR')]/100)*q[i] for i in range(len(ingredientes)))
right_c6 =  ((limitante[elementos.index('PDR')]/100)*demanda - ((limitanteMaxInf[elementos.index('PDR')]/100)*(limitante[elementos.index('PDR')]/100)*demanda))
opt_mod.add_constraint(left_c6 >= right_c6, ctname='c6')

left_c7 = sum((valores[i][elementos.index('PDR')]/100)*q[i] for i in range(len(ingredientes)))
right_c7 =  ((limitante[elementos.index('PDR')]/100)*demanda + ((limitanteMaxSup[elementos.index('PDR')]/100)*(limitante[elementos.index('PDR')]/100)*demanda))
opt_mod.add_constraint(left_c7 <= right_c7, ctname='c7')

left_c8 = sum((valores[i][elementos.index('PNDR')]/100)*q[i] for i in range(len(ingredientes)))
right_c8 =  ((limitante[elementos.index('PNDR')]/100)*demanda - ((limitanteMaxInf[elementos.index('PNDR')]/100)*(limitante[elementos.index('PNDR')]/100)*demanda))
opt_mod.add_constraint(left_c8 >= right_c8, ctname='c8')

left_c9 = sum((valores[i][elementos.index('PNDR')]/100)*q[i] for i in range(len(ingredientes)))
right_c9 =  ((limitante[elementos.index('PNDR')]/100)*demanda + ((limitanteMaxSup[elementos.index('PNDR')]/100)*(limitante[elementos.index('PNDR')]/100)*demanda))
opt_mod.add_constraint(left_c9 <= right_c9, ctname='c9')

left_c10 = sum((valores[i][elementos.index('FDN')]/100)*q[i] for i in range(len(ingredientes)))
right_c10 =  ((limitante[elementos.index('FDN')]/100)*demanda - ((limitanteMaxInf[elementos.index('FDN')]/100)*(limitante[elementos.index('FDN')]/100)*demanda))
opt_mod.add_constraint(left_c10 >= right_c10, ctname='c10')

left_c11 = sum((valores[i][elementos.index('FDN')]/100)*q[i] for i in range(len(ingredientes)))
right_c11 =  ((limitante[elementos.index('FDN')]/100)*demanda + ((limitanteMaxSup[elementos.index('FDN')]/100)*(limitante[elementos.index('FDN')]/100)*demanda))
opt_mod.add_constraint(left_c11 <= right_c11, ctname='c11')

left_c12 = sum((valores[i][elementos.index('EE')]/100)*q[i] for i in range(len(ingredientes)))
right_c12 =  ((limitante[elementos.index('EE')]/100)*demanda - ((limitanteMaxInf[elementos.index('EE')]/100)*(limitante[elementos.index('EE')]/100)*demanda))
opt_mod.add_constraint(left_c12 >= right_c12, ctname='c12')

left_c13 = sum((valores[i][elementos.index('EE')]/100)*q[i] for i in range(len(ingredientes)))
right_c13 =  ((limitante[elementos.index('EE')]/100)*demanda + ((limitanteMaxSup[elementos.index('EE')]/100)*(limitante[elementos.index('EE')]/100)*demanda))
opt_mod.add_constraint(left_c13 <= right_c13, ctname='c13')

left_c14 = sum((valores[i][elementos.index('Ca')]/100)*q[i] for i in range(len(ingredientes)))
right_c14 =  ((limitante[elementos.index('Ca')]/100)*demanda - ((limitanteMaxInf[elementos.index('Ca')]/100)*(limitante[elementos.index('Ca')]/100)*demanda))
opt_mod.add_constraint(left_c14 >= right_c14, ctname='c14')

left_c15 = sum((valores[i][elementos.index('Ca')]/100)*q[i] for i in range(len(ingredientes)))
right_c15 =  ((limitante[elementos.index('Ca')]/100)*demanda + ((limitanteMaxSup[elementos.index('Ca')]/100)*(limitante[elementos.index('Ca')]/100)*demanda))
opt_mod.add_constraint(left_c15 <= right_c15, ctname='c15')

left_c16 = sum((valores[i][elementos.index('P')]/100)*q[i] for i in range(len(ingredientes)))
right_c16 =  ((limitante[elementos.index('P')]/100)*demanda - ((limitanteMaxInf[elementos.index('P')]/100)*(limitante[elementos.index('P')]/100)*demanda))
opt_mod.add_constraint(left_c16 >= right_c16, ctname='c16')

left_c17 = sum((valores[i][elementos.index('P')]/100)*q[i] for i in range(len(ingredientes)))
right_c17 =  ((limitante[elementos.index('P')]/100)*demanda + ((limitanteMaxSup[elementos.index('P')]/100)*(limitante[elementos.index('P')]/100)*demanda))
opt_mod.add_constraint(left_c17 <= right_c17, ctname='c17')

left_c18 = sum((valores[i][elementos.index('Na')]/100)*q[i] for i in range(len(ingredientes)))
right_c18 =  ((limitante[elementos.index('Na')]/100)*demanda - ((limitanteMaxInf[elementos.index('Na')]/100)*(limitante[elementos.index('Na')]/100)*demanda))
opt_mod.add_constraint(left_c18 >= right_c18, ctname='c18')

left_c19 = sum((valores[i][elementos.index('Na')]/100)*q[i] for i in range(len(ingredientes)))
right_c19 =  ((limitante[elementos.index('Na')]/100)*demanda + ((limitanteMaxSup[elementos.index('Na')]/100)*(limitante[elementos.index('Na')]/100)*demanda))
opt_mod.add_constraint(left_c19 <= right_c19, ctname='c19')

left_c20 = sum((valores[i][elementos.index('K')]/100)*q[i] for i in range(len(ingredientes)))
right_c20 =  ((limitante[elementos.index('K')]/100)*demanda - ((limitanteMaxInf[elementos.index('K')]/100)*(limitante[elementos.index('K')]/100)*demanda))
opt_mod.add_constraint(left_c20 >= right_c20, ctname='c20')

left_c21 = sum((valores[i][elementos.index('K')]/100)*q[i] for i in range(len(ingredientes)))
right_c21 =  ((limitante[elementos.index('K')]/100)*demanda + ((limitanteMaxSup[elementos.index('K')]/100)*(limitante[elementos.index('K')]/100)*demanda))
opt_mod.add_constraint(left_c21 <= right_c21, ctname='c21')

left_c22 = sum((valores[i][elementos.index('Mg')]/100)*q[i] for i in range(len(ingredientes)))
right_c22 =  ((limitante[elementos.index('Mg')]/100)*demanda - ((limitanteMaxInf[elementos.index('Mg')]/100)*(limitante[elementos.index('Mg')]/100)*demanda))
opt_mod.add_constraint(left_c22 >= right_c22, ctname='c22')

left_c23 = sum((valores[i][elementos.index('Mg')]/100)*q[i] for i in range(len(ingredientes)))
right_c23 =  ((limitante[elementos.index('Mg')]/100)*demanda + ((limitanteMaxSup[elementos.index('Mg')]/100)*(limitante[elementos.index('Mg')]/100)*demanda))
opt_mod.add_constraint(left_c23 <= right_c23, ctname='c23')

left_c24 = sum((valores[i][elementos.index('S')]/100)*q[i] for i in range(len(ingredientes)))
right_c24 =  ((limitante[elementos.index('S')]/100)*demanda - ((limitanteMaxInf[elementos.index('S')]/100)*(limitante[elementos.index('S')]/100)*demanda))
opt_mod.add_constraint(left_c24 >= right_c24, ctname='c24')

left_c25 = sum((valores[i][elementos.index('S')]/100)*q[i] for i in range(len(ingredientes)))
right_c25 =  ((limitante[elementos.index('S')]/100)*demanda + ((limitanteMaxSup[elementos.index('S')]/100)*(limitante[elementos.index('S')]/100)*demanda))
opt_mod.add_constraint(left_c25 <= right_c25, ctname='c25')

left_c26 = sum((valores[i][elementos.index('Co')])*q[i] for i in range(len(ingredientes)))
right_c26 =  ((limitante[elementos.index('Co')])*demanda - ((limitanteMaxInf[elementos.index('Co')]/100)*(limitante[elementos.index('Co')])*demanda))
opt_mod.add_constraint(left_c26 >= right_c26, ctname='c26')

left_c27 = sum((valores[i][elementos.index('Co')])*q[i] for i in range(len(ingredientes)))
right_c27 =  ((limitante[elementos.index('Co')])*demanda + ((limitanteMaxSup[elementos.index('Co')]/100)*(limitante[elementos.index('Co')])*demanda))
opt_mod.add_constraint(left_c27 <= right_c27, ctname='c27')

left_c28 = sum((valores[i][elementos.index('Se')])*q[i] for i in range(len(ingredientes)))
right_c28 =  ((limitante[elementos.index('Se')])*demanda - ((limitanteMaxInf[elementos.index('Se')]/100)*(limitante[elementos.index('Se')])*demanda))
opt_mod.add_constraint(left_c28 >= right_c28, ctname='c28')

left_c29 = sum((valores[i][elementos.index('Se')])*q[i] for i in range(len(ingredientes)))
right_c29 =  ((limitante[elementos.index('Se')])*demanda + ((limitanteMaxSup[elementos.index('Se')]/100)*(limitante[elementos.index('Se')])*demanda))
opt_mod.add_constraint(left_c29 <= right_c29, ctname='c29')

left_c30 = sum((valores[i][elementos.index('Zn')])*q[i] for i in range(len(ingredientes)))
right_c30 =  ((limitante[elementos.index('Zn')])*demanda - ((limitanteMaxInf[elementos.index('Zn')]/100)*(limitante[elementos.index('Zn')])*demanda))
opt_mod.add_constraint(left_c30 >= right_c30, ctname='c30')

left_c31 = sum((valores[i][elementos.index('Zn')])*q[i] for i in range(len(ingredientes)))
right_c31 =  ((limitante[elementos.index('Zn')])*demanda + ((limitanteMaxSup[elementos.index('Zn')]/100)*(limitante[elementos.index('Zn')])*demanda))
opt_mod.add_constraint(left_c31 <= right_c31, ctname='c31')

#Define a funcao objetivo
opt_mod.set_objective('min', obj)

opt_mod.print_information()

opt_mod.solve()

opt_mod.print_solution()