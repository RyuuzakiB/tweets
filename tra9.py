from trie import Trie	              #funções da classe trie, como inserir, procurar a polaridade, etc
from B import BPlusTree           #funções das classes B e B+
from funcoes_main import cria_dicionario, insere_na_B, polaridade_tweet

if __name__ == '__main__':
    ordem=20
    bt = BPlusTree(ordem)
    trie = Trie()   
    
    print("PROGRAMA SENTIMENTAL S2\n")
    
    print(">>>> CRIAÇÃO DO DICIONÁRIO")
    trie = cria_dicionario(trie) 
    bt = insere_na_B(bt,trie)
    
    print("\n>>>> DETERMINAÇÃO DA POLARIDADE") #determinar a polaridade de twtts  
    polaridade_tweet(trie)
    
    print(">>>> FUNÇÃO ADICIONAL")
    print("Buscar palavras cujo escore de sentimento esteja:\n1-a partir de um valor\n2-até um valor\n3-entre um intervalo")
    r=0
    while r!=1 and r!=2 and r!=3 :
        r= int(input("Opção: "))
    if r == 1:
        i = float(input("Valor inicial: "))
        f=1.0
    elif r == 2:
        f = float(input("Valor final: "))
        i=-1.0
    else: #r == 3
        i = float(input("Início do intervalo: "))
        f = float(input("Fim: "))	
    listaNodos=bt.getintervalo( i, f)
    print(listaNodos)
    #f ADICIONAL: buscar palavras cujo escore de sentimento esteja entre um intervalo
    #val<(-1) e val>1 funcionam em todos os casos  
