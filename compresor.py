from huffman import HuffmanNode 
import numpy as np
import heapq
import time
import math
import sys

def build_frequency_table(text):
    # Construye una tabla de frecuencias a partir del texto dado
    freq_dict = {}
    for char in text:
        if char in freq_dict:
            freq_dict[char] += 1
        else:
            freq_dict[char] = 1
    return freq_dict

def build_huffman_tree(freq_dict):
    # Construye el árbol de Huffman a partir de la tabla de frecuencias dada
    heap = []
    for char, freq in freq_dict.items():
        node = HuffmanNode(freq, char)  # Crea un nodo Huffman para cada carácter y su frecuencia
        heapq.heappush(heap, node)

    while len(heap) > 1:
        # Combina los nodos del heap hasta que quede solo un nodo raíz
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = HuffmanNode(left.freq + right.freq)  # Crea un nodo padre con la suma de las frecuencias de los hijos
        parent.left, parent.right = left, right
        heapq.heappush(heap, parent)

    return heap[0]  # Devuelve el nodo raíz del árbol de Huffman

def build_codeword_table(root):
    # Construye una tabla de códigos a partir del árbol de Huffman dado
    codes = {}
    stack = [(root, "")]
    while stack:
        node, code = stack.pop()
        if node.char is not None:
            codes[node.char] = code  # Asigna el código al carácter en la tabla de códigos
        else:
            stack.append((node.left, code + "0"))  # Agrega el nodo izquierdo al stack con el código actualizado
            stack.append((node.right, code + "1"))  # Agrega el nodo derecho al stack con el código actualizado

    return codes  # Devuelve la tabla de códigos


def huffman_compress(text):
    freq_dict = build_frequency_table(text)
    root = build_huffman_tree(freq_dict)
    codeword_dict = build_codeword_table(root)
    encoded_text = "".join(codeword_dict[byte] for byte in text)
    tam = len(encoded_text) // 8
    try:
        encoded_text_bytes = int(encoded_text, 2).to_bytes(tam, byteorder="big")
    except:
        tam = math.ceil(len(encoded_text) / 8)
        encoded_text_bytes = int(encoded_text, 2).to_bytes(tam, byteorder="big")
    # Convert the encoded text to a NumPy array of integers for efficient storage
    return encoded_text_bytes, root

if __name__ == "__main__":
    start_time = time.time()
    filename = sys.argv[1]
    compressed_filename = "comprimido.elmejorprofesor"

    # Abrimos el archivo de texto
    with open(filename, 'rb') as f:
        text = f.read()
    try:
        ENCODING = 'cp1252'
        text = text.decode(ENCODING)
    except:
        ENCODING = 'utf-8'
        text = text.decode(ENCODING)

    # Comprimir el texto
    compressed, root = huffman_compress(text)

    # Guardar la codificación Huffman y el texto comprimido en archivos separados
    with open(compressed_filename, 'wb') as f:
        np.save(f, compressed)
        np.save(f, root.to_array())
        file_format = filename.split('.')[-1]
        np.save(f, file_format.encode())
        np.save(f, ENCODING.encode())
      

    end_time = time.time()
    total_time = end_time - start_time
    print(f"{total_time:.2f}")