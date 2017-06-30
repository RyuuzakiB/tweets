import csv    	                      #para administrar funções de leitura/escrita em arquivos csv
from trie import Trie	              #funções da classe trie, como inserir, procurar a polaridade, etc
from B import BPlusTree           #funções das classes B e B+
from palavra import eh_palavra        #função retorna palavra minúscula; sem pontuação, números, e qualquer coisa que não for alfabeto



def cria_dicionario(trie): 
    arq2 = 'Copia_fonte.csv' 
    copia = open(arq2, 'w')
    r='S'
    lista=[]
    while r.lower()=='s':
        arqF= input("Nome do arq fonte: ")+'.csv'
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
                    else:
                        trie.update(palavra,escore)
            linha = ' '.join(['%s'%campo.strip() for campo in linha.split(';')])+'\n'
            copia.write(linha)
        original.close()
        r= input("Deseja inserir outro arq como fonte [s ou n]: ")
    copia.close()
    return trie
    
    
    
    
def insere_na_B(bt,trie):
    #pega todas as palavras da trie em lista na forma "pol:palavra"
    lista=[]
    lista=list(trie.getT())
    while len(lista) != 0:
        item=lista.pop()
        for elem in item.split(':'):#separa a ch da palavra
            try:
                ch=float(elem)
            except Exception:
                palavra=elem
        bt.insert(ch,palavra)#insere na arv B++
    return bt



def polaridade_tweet(trie):  
    arq2 = 'RESULTADO.csv'
    pol=0
    arq= input("Nome do arq para ser avaliado: ")+'.csv'
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
        linha = ' '.join(['%s'%campo.strip() for campo in linha.split(';')])+(',%0.2f'%pol)+('\n') 
        resul.write(linha)
    original.close()
    resul.close()
    print("Resultado no arquivo %s\n"%arq2)
