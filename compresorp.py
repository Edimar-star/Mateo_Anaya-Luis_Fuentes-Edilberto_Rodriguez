from huffman import HuffmanNode
from mpi4py import MPI
import numpy as np
import time
import sys
import math
import heapq

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

def huffman_compress(text, codeword_dict):
    encoded_text = "".join(codeword_dict[byte] for byte in text)
    return encoded_text

def stringToBytes(encoded_text):
    tam = len(encoded_text) // 8
    try:
      encoded_text_bytes = int(encoded_text, 2).to_bytes(tam, byteorder="big")
    except:
      tam = math.ceil(len(encoded_text) / 8)
      encoded_text_bytes = int(encoded_text, 2).to_bytes(tam, byteorder="big")
    # Convert the encoded text to a NumPy array of integers for efficient storage
    return encoded_text_bytes

def divide_string(string, n):
    length = len(string)
    part_size = length // n
    remainder = length % n

    parts = []
    start = 0
    for i in range(n):
        part_length = part_size + (i < remainder)
        end = start + part_length
        part = string[start:end]
        parts.append(part)
        start = end

    return parts

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    # Divide the text into parts
    if rank == 0:
        start_time = time.time()
        compressed_filename = "comprimidop.elmejorprofesor"
        filename = sys.argv[1]
        n = size  # Number of parts

        # Open the file and read the text
        with open(filename, 'rb') as f:
            text = f.read()
        try:
            ENCODING = 'cp1252'
            text = text.decode(ENCODING)
            #print("hola",text)
        except:
            ENCODING = 'utf-8'
            text = text.decode(ENCODING)
        
        freq_dict = build_frequency_table(text)
        root = build_huffman_tree(freq_dict)
        codeword_dict = build_codeword_table(root)
        send_data = divide_string(text, n)
    else:
        codeword_dict = None
        send_data = None

    codeword_dict = comm.bcast(codeword_dict, root=0)
    received_data = comm.scatter(send_data, root=0)
    compressed = huffman_compress(received_data, codeword_dict)
    compressed_results = comm.gather(compressed, root=0)

    if rank == 0:
        with open(compressed_filename, 'wb') as f:
            np.save(f, stringToBytes(''.join(compressed_results)))
            np.save(f, root.to_array())
            file_format = filename.split('.')[-1]
            np.save(f, file_format.encode())
            np.save(f, ENCODING.encode())

        end_time = time.time()
        print(f"{end_time - start_time:.2f}")