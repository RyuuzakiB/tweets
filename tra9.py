import csv    	                      #para administrar funções de leitura/escrita em arquivos csv
from trie import Trie	              #funções da classe trie, como inserir, procurar a polaridade, etc
from Bmais import BPlusTree           #funções das classes B e B+
from palavra import eh_palavra        #função retorna palavra minúscula; sem pontuação, números, e qualquer coisa que não for alfabeto


if __name__ == '__main__':
    ordem=20
    bt = BPlusTree(ordem)
	
    trie = Trie()
    dic='dicionario.csv'
    arq2 = 'TWfonte.csv'
    extensao_csv=".csv"
    
    
    print("PROGRAMA SENTIMENTAL S2\n")

    copia = open(arq2, 'w')
    dicionario = open(dic, 'w')

    print(">>>> CRIAÇÃO DO DICIONÁRIO")
    r='S'
    while (r == 'S' or r == 's'):#não existe do..while em python :(
        arqF= input("Nome do arq fonte: ")+extensao_csv
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
                palavra=eh_palavra(word)             #função tira pontuação, números, e qualquer coisa que não for alfabeto da palavra; em minúsculo
                if palavra:     					
                    if palavra not in trie:
                        trie.insert(palavra,escore)
                        dicionario.write('%s\n' % (palavra))#arv B++ usa depois
                    else:
                        trie.update(palavra,escore)
            linha = ' '.join(['%s'%campo.strip() for campo in linha.split(';')])+'\n'
            copia.write(linha)
        original.close()
        r= input("Deseja inserir outro arq como fonte [s ou n]: ")+extensao_csv
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
    arq2 = 'RESUL.csv'
    pol=0
    arq= input("Nome do arq para ser avaliado: ")+extensao_csv
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
    print(">>>> FUNÇÃO ADICIONAL: buscar palavras cujo escore de sentimento esteja:\n1-a partir de um valor\n2-até um valor\n3-entre um intervalo")
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
