class TrieNode:
    def __init__(self):
        # Inicializa un nodo Trie
        self.children = {}  # Diccionario para almacenar los hijos del nodo
        self.is_end_of_word = False  # Bandera para indicar si es el final de una palabra

def insert_prefixes(prefixes):
    # Inserta los prefijos en un Trie y devuelve la raíz del Trie
    root = TrieNode()  # Crea un nodo raíz vacío del Trie
    for prefix in prefixes:
        node = root  # Comienza desde la raíz para cada prefijo
        for char in prefix:
            if char not in node.children:
                node.children[char] = TrieNode()  # Crea un nuevo nodo si el carácter no está presente en los hijos del nodo actual
            node = node.children[char]  # Avanza al siguiente nodo hijo
        node.is_end_of_word = True  # Marca el último nodo como el final de una palabra

    return root

def remove_prefixes(cadena, root):
    # Remueve los prefijos de una cadena utilizando el Trie y devuelve el resultado
    resultado = []
    while cadena:
        node = root  # Comienza desde la raíz para cada cadena
        prefix_found = False  # Bandera para indicar si se encontró un prefijo
        for i, char in enumerate(cadena):
            if char not in node.children:
                resultado.append(cadena)  # Agrega la cadena completa si no se encuentra el carácter en los hijos del nodo actual
                prefix_found = False
                break
            node = node.children[char]  # Avanza al siguiente nodo hijo
            if node.is_end_of_word:
                resultado.append(cadena[i+1:])  # Agrega la subcadena restante si se encuentra un prefijo
                prefix_found = True
                break
        if not prefix_found:
            break
        cadena = resultado[-1]  # Actualiza la cadena con la última subcadena agregada
    return resultado[-1]  # Devuelve la última subcadena resultante

