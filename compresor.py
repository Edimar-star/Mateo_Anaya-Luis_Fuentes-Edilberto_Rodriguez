from collections import Counter
from huffman import HuffmanNode
import numpy as np
import time
import sys
import math
import heapq

def build_frequency_table(text):
	freq_dict = Counter(text)
	return freq_dict

def build_huffman_tree(freq_dict):
    heap = []
    for char, freq in freq_dict.items():
        node = HuffmanNode(freq, char)
        heapq.heappush(heap, node)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = HuffmanNode(left.freq + right.freq)
        parent.left, parent.right = left, right
        heapq.heappush(heap, parent)

    return heap[0]

def build_codeword_table(root):
    codes = {}
    stack = [(root, "")]
    while stack:
        node, code = stack.pop()
        if node.char is not None:
            codes[node.char] = code
        else:
            stack.append((node.left, code + "0"))
            stack.append((node.right, code + "1"))

    return codes

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
    print(f"{end_time - start_time:.2f}")
