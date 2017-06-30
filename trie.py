import collections
class Trie:
    def __init__(self):
        """
        É criada tipo uma struct na classe Trie, com o que queremos buscar nela 
        """
        self.child = collections.defaultdict(Trie) #função que retorna sempre a estrutura definida (.child, .por, .ac e .f), caso contrário, None(Null)
        self.pol=0 #polaridade
        self.ac=0 #escore acumulado
        self.f=0 #frequencia

    def insert(self, string,escore):
        """
        Dada uma string, é acrescentada na trie "no mesmo lugar", sendo essa uma característica de árvore trie
        Exemplo: inserindo "Olá" e "Oi", 'O' é escrito uma vez só, sendo conectado tanto com "lá" com "i"
        """
        node = self
        for char in string:
            node = node.child[char]
        node.pol = escore
        node.ac = escore
        node.f = 1

    def getpol(self, palavra): 
        """
        Entrada: palavra de arquivo em que queremos saber a polaridade das frases
        Saída: polaridade da palavra
        """
        node = self
        for char in palavra:
            node = node.child[char]
        return node.pol
        
    def update(self, word, escore):
        """
        Entrada = palavra e o seu escore em uma frase (ambos pegos do arquivo dado com frases e suas polaridades)
        Função: Atualiza o valor acumulado, total de ocorrências e polaridade da palavra
        """
        node = self
        for char in word:
            node = node.child[char]
        node.ac += escore
        node.f += 1
        node.pol = float(node.ac/node.f)
        
    def escore(self, word):
        """
        Função que, dada uma palavra, retorna a polaridade dela, o valor acumulado e o número de ocorrências
        """
        node=self        
        for char in word:
            node = node.child[char]
        return float(node.pol),int(node.ac),int(node.f)
            
            
    def getT(self, prefix=""):#retorna todos os elementos da trie
        """
        Função criada para percorrer a trie inteira; as letras vão se acumulando e quando acha os valores, retorna naquele formato
        """
        if self.pol is not None:#se o nodo existe
            if self.f != 0:#se a frequencia é diferente de 0, ou seja, se chegou em algum nodo com pol, acc e f associadas
                yield "{}:{}".format(self.pol, prefix)#retorna "pol:prefix", sem sair da função
        for letter, child in self.child.items():#para cada letra filha
            yield from child.getT(prefix + letter)#chama a função de novo passando o prefixo + letra filha


    def __contains__(self, word):
        '''
        Para ver se palavra existe na trie
        '''
        trie = self
        for char in word:
            if char in trie.child:
                trie = trie.child[char]
            else:
                return False
        return True

    def __str__(self, depth = 0):
        """
        Apresenta uma trie bonitinha, não ordenada
        """
        for i in self.child:
            s.append( '{}{}-> {}-{}-{} {}'.format(' ' * depth, i or '#', self.pol, self.acc, self.f, '\n' + self.child[i].__str__(depth + 1)))

        
