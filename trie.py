class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

def insert_prefixes(prefixes):
    root = TrieNode()
    for prefix in prefixes:
        node = root
        for char in prefix:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    return root

def remove_prefixes(cadena, root):
    resultado = []
    while cadena:
        node = root
        prefix_found = False
        for i, char in enumerate(cadena):
            if char not in node.children:
                resultado.append(cadena)
                prefix_found = False
                break
            node = node.children[char]
            if node.is_end_of_word:
                resultado.append(cadena[i+1:])
                prefix_found = True
                break
        if not prefix_found:
            break
        cadena = resultado[-1]
    return resultado[-1]