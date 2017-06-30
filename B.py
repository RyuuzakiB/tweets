import bisect
import itertools
import operator

class _BNode(object):#Nodo da arvore B

    __slots__ = ["tree", "contents", "children"]

    def __init__(self, tree, contents=None, children=None):
        '''
        Inicializa o nodo da arvore
        '''
        self.tree = tree
        self.contents = contents or []
        self.children = children or []
        if self.children:
            assert len(self.contents) + 1 == len(self.children), \
                    "one more child than data item required"

    def __repr__(self):
        '''
        Retorna informações sobre o nodo
        '''
        name = "Branch" if getattr(self, "children", 0) else "Leaf"
        return "<%s %s>" % (name, ", ".join(map(str, self.contents)))

    def lateral(self, parent, parent_index, dest, dest_index):
        '''
        Utilizado para mover nodos nas operações sobre a arvore
        '''
        if parent_index> dest_index:
            dest.contents.append(parent.contents[dest_index])
            parent.contents[dest_index] = self.contents.pop(0)
            if self.children:
                dest.children.append(self.children.pop(0))
        else:
            dest.contents.insert(0, parent.contents[parent_index])
            parent.contents[parent_index] = self.contents.pop()
            if self.children:
                dest.children.insert(0, self.children.pop())

    def shrink(self, ancestors):
        '''
        Encolhe a arvore, pucha um dado para ocupar o lugar de outro
        '''
        parent = None

        if ancestors:
            parent, parent_index = ancestors.pop()
            # tenta pegar o irmão do vizinho da esquerda
            if parent_index:
                left_sib = parent.children[parent_index - 1]
                if len(left_sib.contents) < self.tree.order:
                    self.lateral(
                            parent, parent_index, left_sib, parent_index - 1)
                    return

            # tenta o vizinho da direita
            if parent_index + 1 < len(parent.children):
                right_sib = parent.children[parent_index + 1]
                if len(right_sib.contents) < self.tree.order:
                    self.lateral(
                            parent, parent_index, right_sib, parent_index + 1)
                    return

        center = len(self.contents) // 2
        sibling, push = self.split()

        if not parent:
            parent, parent_index = self.tree.BRANCH(
                    self.tree, children=[self]), 0
            self.tree._root = parent

        # passa a mediana para o pai
        parent.contents.insert(parent_index, push)
        parent.children.insert(parent_index + 1, sibling)
        if len(parent.contents) > parent.tree.order:
            parent.shrink(ancestors)

    def grow(self, ancestors):
        '''
        Faz a arvore crescer, arruma lugar para novo dado
        '''
        parent, parent_index = ancestors.pop()

        minimum = self.tree.order // 2
        left_sib = right_sib = None

        # tenta emprestar do irmão da direita
        if parent_index + 1 < len(parent.children):
            right_sib = parent.children[parent_index + 1]
            if len(right_sib.contents) > minimum:
                right_sib.lateral(parent, parent_index + 1, self, parent_index)
                return

        # tenta emprestar do irmão da esquerda
        if parent_index:
            left_sib = parent.children[parent_index - 1]
            if len(left_sib.contents) > minimum:
                left_sib.lateral(parent, parent_index - 1, self, parent_index)
                return

        # unificar com um irmão - tenta o da esquerda primeiro
        if left_sib:
            left_sib.contents.append(parent.contents[parent_index - 1])
            left_sib.contents.extend(self.contents)
            if self.children:
                left_sib.children.extend(self.children)
            parent.contents.pop(parent_index - 1)
            parent.children.pop(parent_index)
        else:
            self.contents.append(parent.contents[parent_index])
            self.contents.extend(right_sib.contents)
            if self.children:
                self.children.extend(right_sib.children)
            parent.contents.pop(parent_index)
            parent.children.pop(parent_index + 1)

        if len(parent.contents) < minimum:
            if ancestors:
                # pai é a raiz
                parent.grow(ancestors)
            elif not parent.contents:
                # pai é a raiz e não está vazio
                self.tree._root = left_sib or self

    def split(self):
        '''
        Separa um nodo, a mediana sobe e vira pai
        '''
        center = len(self.contents) // 2
        median = self.contents[center]
        sibling = type(self)(
                self.tree,
                self.contents[center + 1:],
                self.children[center + 1:])
        self.contents = self.contents[:center]
        self.children = self.children[:center + 1]
        return sibling, median

    def insert(self, index, item, ancestors):
        '''
        Insere novo dado
        '''
        self.contents.insert(index, item)
        if len(self.contents) > self.tree.order:
            self.shrink(ancestors)




class _BPlusLeaf(_BNode):#Folha da arvore B++ 
    __slots__ = ["tree", "contents", "data", "next"]#next é a diferença estrutural entre folhas e nodos internos

    def __init__(self, tree, contents=None, data=None, next=None):
        '''
        Inicializa a folha da arvore
        '''
        self.tree = tree
        self.contents = contents or []
        self.data = data or []
        self.next = next
        assert len(self.contents) == len(self.data), "one data per key"

    def insert(self, index, key, data, ancestors):
        '''
        Insere a folha na arvore
        '''
        self.contents.insert(index, key)
        self.data.insert(index, data)

        if len(self.contents) > self.tree.order:
            self.shrink(ancestors)

    def lateral(self, parent, parent_index, dest, dest_index):
        '''
        Utilizado para mover nodos nas operações sobre a arvore
        '''
        if parent_index > dest_index:
            dest.contents.append(self.contents.pop(0))
            dest.data.append(self.data.pop(0))
            parent.contents[dest_index] = self.contents[0]
        else:
            dest.contents.insert(0, self.contents.pop())
            dest.data.insert(0, self.data.pop())
            parent.contents[parent_index] = dest.contents[0]

    def split(self):
        '''
        Separa um nodo, a mediana sobe e vira pai
        '''
        center = len(self.contents) // 2
        median = self.contents[center - 1]
        sibling = type(self)(
                self.tree,
                self.contents[center:],
                self.data[center:],
                self.next)
        self.contents = self.contents[:center]
        self.data = self.data[:center]
        self.next = sibling
        return sibling, sibling.contents[0]

    def remove(self, index, ancestors):
        '''
        Retira um dado
        '''
        minimum = self.tree.order // 2
        if index >= len(self.contents):
            self, index = self.next, 0

        key = self.contents[index]

        # OTM: se alguma folha não esta totalmente ocupada, ou seja, não tem o numero maximo de filhos
        # ela aceita a key, assim não precisa balancear
        current = self
        while current is not None and current.contents[0] == key:
            if len(current.contents) > minimum:
                if current.contents[0] == key:
                    index = 0
                else:
                    index = bisect.bisect_left(current.contents, key)
                current.contents.pop(index)
                current.data.pop(index)
                return
            current = current.next

        self.grow(ancestors)
        

    def grow(self, ancestors):
        '''
        Faz a arvore crescer, arruma lugar para novo dado
        '''
        minimum = self.tree.order // 2
        parent, parent_index = ancestors.pop()
        left_sib = right_sib = None

        # Tenta emprestar do vizinho - tenta da direita
        if parent_index + 1 < len(parent.children):
            right_sib = parent.children[parent_index + 1]
            if len(right_sib.contents) > minimum:
                right_sib.lateral(parent, parent_index + 1, self, parent_index)
                return

        # volta para esquerda
        if parent_index:
            left_sib = parent.children[parent_index - 1]
            if len(left_sib.contents) > minimum:
                left_sib.lateral(parent, parent_index - 1, self, parent_index)
                return

        # juntar ao vizinho - tenta da esquerda
        if left_sib:
            left_sib.contents.extend(self.contents)
            left_sib.data.extend(self.data)
            parent.remove(parent_index - 1, ancestors)
            return

        # volta para esquerda
        self.contents.extend(right_sib.contents)
        self.data.extend(right_sib.data)
        parent.remove(parent_index, ancestors)


class BTree(object):#estrutura da arvore B
    BRANCH = LEAF = _BNode

    def __init__(self, order):
        '''
        Inicializa a arvore
        '''
        self.order = order
        self._root = self._bottom = self.LEAF(self)

    def _path_to(self, item):
        '''
        retorna o caminho para um nodo
        '''
        current = self._root
        ancestry = []

        while getattr(current, "children", None):
            index = bisect.bisect_left(current.contents, item)
            ancestry.append((current, index))
            if index < len(current.contents) \
                    and current.contents[index] == item:
                return ancestry
            current = current.children[index]

        index = bisect.bisect_left(current.contents, item)
        ancestry.append((current, index))
        present = index < len(current.contents)
        present = present and current.contents[index] == item

        return ancestry

    def _present(self, item, ancestors):
        '''
        Retorna se está na arvore
        '''
        last, index = ancestors[-1]
        return index < len(last.contents) and last.contents[index] == item

    def insert(self, item):
        '''
        Insere nodo
        '''
        current = self._root
        ancestors = self._path_to(item)
        node, index = ancestors[-1]
        while getattr(node, "children", None):
            node = node.children[index]
            index = bisect.bisect_left(node.contents, item)
            ancestors.append((node, index))
        node, index = ancestors.pop()
        node.insert(index, item, ancestors)


    def __contains__(self, item):
        '''
        se está na arvore
        '''
        return self._present(item, self._path_to(item))




class BPlusTree(BTree):#estrutura da arvore B++
    LEAF = _BPlusLeaf

    def _get(self, key):
        '''
        Retorna dados com a chave informada
        '''
        node, index = self._path_to(key)[-1]

        if index == len(node.contents):
            if node.next:
                node, index = node.next, 0
            else:
                return

        while node.contents[index] == key:
            yield node.data[index]
            index += 1
            if index == len(node.contents):
                if node.next:
                    node, index = node.next, 0
                else:
                    return
    def _getINT(self, i, f):
        '''
        Retorna dados com a chave entre o intervalo informado
        '''
        node, index = self._path_to(i)[-1]

        if index == len(node.contents):
            if node.next:
                node, index = node.next, 0
            else:
                return
        while (node.contents[index] >= i  and  node.contents[index] <=f):
            yield node.data[index]
            index += 1
            if index == len(node.contents):
                if node.next:
                    node, index = node.next, 0
                else:
                    return		
		
    def _path_to(self, item):
        '''
        Retorna uma lista com caminho até o item
        '''
        path = super(BPlusTree, self)._path_to(item)
        node, index = path[-1]
        while hasattr(node, "children"):
            node = node.children[index]
            index = bisect.bisect_left(node.contents, item)
            path.append((node, index))
        return path

    def get(self, key, default=None):
        '''
        Organiza o retorno do _get
        '''
        try:
            return self._get(key).next()
        except StopIteration:
            return default

    def getlist(self, key):
        '''
        Organiza o retorno do _get em lista
        '''
        return list(self._get(key))
		
    def getintervalo(self, i, f):
        '''
        Organiza o retorno do _getINT em lista
        '''
        return list(self._getINT(i,f))

    def insert(self, key, data):
        '''
        Insere novo dado
        '''
        path = self._path_to(key)
        node, index = path.pop()
        node.insert(index, key, data, path)


    __getitem__ = get
    __setitem__ = insert

    def __contains__(self, key):
        '''
        Testa se está na arvore
        '''
        for item in self._get(key):
            return True
        return False
###################

#Class B e B++: https://gist.github.com/teepark/572734/36b26f29102007cb4c259c903119ff2ac0795377#file-btree-py
