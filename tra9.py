#coding=UTF-8
import unicodedata
from string import punctuation
def eh_palavra(s):
    s= "".join([x for x in s if x.isalpha()])  #tira pontuação e números das palavras
    if(len(s)>=2):
    	return s.lower()
    else:
    	return None

import csv    	
from trie import Trie	
from Bmais import BPlusTree

if __name__ == '__main__':
    ordem=20
    bt = BPlusTree(ordem)
	
    trie = Trie()
    dic='dicionario.csv'
    arq2 = 'TWfonte.csv'
    #arqF='pt2.csv'
    
    print("PROGRAMA SENTIMENTAL S2\n")

    copia = open(arq2, 'w')
    dicionario = open(dic, 'w')

    print(">>>> CRIAÇÃO DO DICIONÁRIO")
    r='S'
    while (r == 'S' or r == 's'):#não existe do..while em python :(
        arqF= input("Nome do arq fonte com frases e respectiva pol: ")
        lista=[]
        original = open(arqF, 'r')
        for linha in original.readlines():
            for campo in linha.split(';'):
                for coluna in campo.split(','):
                    lista.append(coluna.split())
                    if(len(lista[-1])==1):
                        escore = ''.join(lista[-1])
                        if escore=='1' or escore=='-1' or escore=='0':
                            escore=int(escore)
            for word in linha.split(' '):
                palavra=eh_palavra(word)
                if palavra:     					
                    if palavra not in trie:
                        trie.insert(palavra,escore)
                        dicionario.write('%s\n' % (palavra))#arv B++ usa depois
                    else:
                        trie.update(palavra,escore)
            linha = ' '.join(['%s'%campo.strip() for campo in linha.split(';')])+'\n'
            copia.write(linha)
        original.close()
        r= input("Deseja inserir outro arq como fonte [s ou n]: ")
    copia.close()
    dicionario.close()
  
    #pega todas as palavras da trie em lista na forma "pol:palavra"
    lista=list(trie.getT())
    while len(lista) != 0:
        item=lista.pop()
        for elem in item.split(':'):#separa a ch da palavra
            try:
                ch=float(elem)
            except Exception:
                palavra=elem
        bt.insert(ch,palavra)#insere na arv B++

    #determinar a polaridade de twtts    
    print("\n>>>> DETERMINAÇÃO DA POLARIDADE")
    arq2 = 'RESULav.csv'
    pol=0
    arq= input("Nome do arq para ser avaliado: ")
    lista=[]
    original = open(arq, 'r')
    resul = open(arq2, 'w')
    for linha in original.readlines():
        pol=0
        for word in linha.split(' '):
            palavra=eh_palavra(word)
            if palavra:     					
                if palavra in trie:
                    pol+=trie.getpol(palavra)
                #else:
                #    pol+=0
        linha = ' '.join(['%s'%campo.strip() for campo in linha.split(';')])+(',%0.2f'%pol)+('\n') 
        resul.write(linha)
    original.close()
    resul.close()
    print("Resultado no arq %s\n"%arq2)

    #possivel forma para buscar todas as palavras da trie: https://stackoverflow.com/questions/16932772/implementation-of-a-trie-in-python
    #f ADICIONAL: buscar palavras cujo escore de sentimento esteja entre um intervalo
    #val<(-1) e val>1 funcionam em todos os casos    

    r=4
    print(">>>> FUNÇÃO ADICIONAL: buscar palavras cujo escore de sentimento esteja:\n1-a partir de um valor\t2-até um valor\t3-entre um intervalo")
    while r!=1 and r!=2 and r!=3 :
        r= int(input("Opção: "))

    if r == 1:
        i = float(input("Val inicial: "))
        f=1.0
    elif r == 2:
        f = float(input("Val final: "))
        i=-1.0
    else: #r == 3
        i = float(input("Inicio do intervalo: "))
        f = float(input("Fim: "))	

    listaNodos=bt.getintervalo( i, f)
    print(listaNodos)
'''
c = csv.writer(open(arq3, "wb"))


c.writerow([palavra,total,total1,total2])

'''		
		
'''
if __name__ == '__main__':
    ordem=20
    bt = BPlusTree(ordem)
	
    trie = Trie()
    dic='dicionario.csv'
    arq2 = 'TWfonte.csv'
    #arqF='pt2.csv'
    
    print("PROGRAMA SENTIMENTAL S2\n")

    copia = open(arq2, 'w')
    dicionario = open(dic, 'w')

    print(">>>> CRIAÇÃO DO DICIONÁRIO")
    r='S'
    while (r == 'S' or r == 's'):#não existe do..while em python :(
        arqF= input("Nome do arq fonte com frases e respectiva pol: ")
        lista=[]
        original = open(arqF, 'r')
        for linha in original.readlines():
            for campo in linha.split(';'):
                for coluna in campo.split(','):
                    lista.append(coluna.split())
                    if(len(lista[-1])==1):
                        escore = ''.join(lista[-1])
                        if escore=='1' or escore=='-1' or escore=='0':
                            escore=int(escore)
            for word in linha.split(' '):
                palavra=eh_palavra(word)
                if palavra:     					
                    if palavra not in trie:
                        trie.insert(palavra,escore)
                        dicionario.write('%s\n' % (palavra))#arv B++ usa depois
                    else:
                        trie.update(palavra,escore)
            linha = ' '.join(['%s'%campo.strip() for campo in linha.split(';')])+'\n'
            copia.write(linha)
        original.close()
        r= input("Deseja inserir outro arq como fonte [s ou n]: ")
    copia.close()
    dicionario.close()
  
    #determinar a polaridade de twtts
    
    print("\n>>>> DETERMINAÇÃO DA POLARIDADE")
    arq2 = 'RESULav.csv'
    pol=0
    arq= input("Nome do arq para ser avaliado: ")
    lista=[]
    original = open(arq, 'r')
    resul = open(arq2, 'w')
    for linha in original.readlines():
        pol=0
        for word in linha.split(' '):
            palavra=eh_palavra(word)
            if palavra:     					
                if palavra in trie:
                    pol+=trie.getpol(palavra)
                #else:
                #    pol+=0
        linha = ' '.join(['%s'%campo.strip() for campo in linha.split(';')])+(',%0.2f'%pol)+('\n') 
        resul.write(linha)
    original.close()
    resul.close()
    print("Resultado no arq %s\n"%arq2)

    #f ADICIONAL: buscar palavras cujo escore de sentimento esteja entre um intervalo
    #val<(-1) e val>1 funcionam em todos os casos    

    #possivel forma para buscar todas as palavras da trie: https://stackoverflow.com/questions/16932772/implementation-of-a-trie-in-python

    #insere pal do dic na arv com ch=pol
    dicionario = open(dic, 'r+')
    for linha in dicionario.readlines():
        for word in linha.split(' '):
            word=eh_palavra(word)
            if word:
                if word in trie:
                    pola=trie.getpol(word)
                    bt.insert(float(pola),word)#cria arvore
                    
                    total,total1,total2=trie.escore(word)
                    print('palavra:',word,'-->','valor:',total,', acumulado:',total1,', ocorrencias:',total2)
                    #print('palavra:',word,'-->','valor:',total,', acumulado:',total1,', ocorrencias:',total2)
    dicionario.close()

    r=4
    print(">>>> FUNÇÃO ADICIONAL: buscar palavras cujo escore de sentimento esteja:\n1-a partir de um valor\t2-até um valor\t3-entre um intervalo")
    while r!=1 and r!=2 and r!=3 :
        r= int(input("Opção: "))

    if r == 1:
        i = float(input("Val inicial: "))
        f=1.0
    elif r == 2:
        f = float(input("Val final: "))
        i=-1.0
    else: #r == 3
        i = float(input("Inicio do intervalo: "))
        f = float(input("Fim: "))	

    listaNodos=bt.getintervalo( i, f)
    print(listaNodos)
'''
'''
c = csv.writer(open(arq3, "wb"))


c.writerow([palavra,total,total1,total2])

'''

