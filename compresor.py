from mpi4py import MPI
from collections import Counter
from huffman import HuffmanNode
import numpy as np
import time
import sys
import math
import heapq

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

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
    start_time = time.time()

    compressed_filename = "comprimido.elmejorprofesor"
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
        

    # Divide the text into parts


    if rank == 0:
        send_data = divide_string(text, n)
        #print('Data to be scattered:', send_data)
        print("scattered")
    else:
        send_data = None

    received_data = comm.scatter(send_data, root=0)
    #print('\n Rank', rank, 'has data:', received_data)
    print('\n Rank', rank, 'has data:', rank)

    compressed, root2 = huffman_compress(received_data)

    comm.barrier()
    gathered_data = comm.gather(received_data, root=0)
    compressed_results = comm.gather(compressed, root=0)
    #print(compressed_results)

    roots = comm.gather(root2, root=0)

    #print(roots)
    if rank == 0:
        compressed_results_array = []
        roots_array =[]
        #print(compressed_results[0])
        for i in range(size):
            compressed_results_array.append(compressed_results[i])
            a =roots[i].to_array()
            roots_array.append(a)


        with open(compressed_filename, 'wb') as f:

            np.save(f, compressed_results_array)
            np.save(f, roots_array)
            file_format = filename.split('.')[-1]
            np.save(f, file_format.encode())
            np.save(f, ENCODING.encode())
    end_time = time.time()
    print(f"{end_time - start_time:.2f}")