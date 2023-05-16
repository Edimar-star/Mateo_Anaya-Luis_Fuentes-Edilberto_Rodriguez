from trie import insert_prefixes, remove_prefixes
from huffman import HuffmanNode
from mpi4py import MPI
import numpy as np
import time
import sys

# Función para decodificar el texto utilizando el árbol de Huffman
def decode_text(encoded_text, root):
    decoded_text = ''
    node = root

    for bit in encoded_text:
        if bit == '0':
            node = node.left
        else:
            node = node.right

        if node.char is not None:
            decoded_text += node.char
            node = root

    return decoded_text

def huffman_decompress(encoded_array, root):
    decoded_text = decode_text(encoded_array, root)
    return decoded_text

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

def eliminar_repetidos(cadena, trieRoot):
    if len(cadena) <= 1000:
        return remove_prefixes(cadena, trieRoot)

    mitad = len(cadena) // 2
    result1 = eliminar_repetidos(cadena[:mitad], trieRoot)
    result2 = eliminar_repetidos(result1 + cadena[mitad:], trieRoot)

    return result2

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
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        start_time = time.time()
        # Load Huffman encoding and compressed text from file
        compressed_filename = sys.argv[1]
        with open(compressed_filename, 'rb') as f:
            compressed = bin(int.from_bytes(np.load(f, allow_pickle=True), byteorder='big'))[2:]
            root = HuffmanNode.from_array(np.load(f, allow_pickle=True))
            file_format = np.load(f, allow_pickle=True).tobytes().decode()
            ENCODING = np.load(f, allow_pickle=True).tobytes().decode()

        # Creo el diccionario
        codeword_dict = build_codeword_table(root)
        values = sorted(codeword_dict.values(), key=len)
        trieRoot = insert_prefixes(values)

        # Dividimos las partes
        parts = divide_string(compressed, size)

        # Corregimos las partes
        ttime = time.time()
        for i in range(size):
            part = parts[i]
            residue = len(eliminar_repetidos(part, trieRoot))
            if residue > 0 and i < size - 1:
                parts[i + 1] = part[len(part) - residue:] + parts[i + 1]
                parts[i] = part[:len(part) - residue]
    
    else:
        parts = None
        root = None

    root = comm.bcast(root, root=0)
    encoded_text = comm.scatter(parts, root=0)
    decoded_text = decode_text(encoded_text, root)
    decompressed = comm.gather(decoded_text, root=0)

    if rank == 0:
        decompressed_filename = f"descomprimidop-elmejorprofesor.{file_format}"
        with open(decompressed_filename, 'wb') as f:
            decoded_text = ''.join(decompressed)
            f.write(decoded_text.encode(ENCODING))

        end_time = time.time()
        total_time = end_time - start_time
        print(f"{total_time:.2f}")