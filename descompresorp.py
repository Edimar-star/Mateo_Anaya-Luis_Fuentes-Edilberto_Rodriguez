from huffman import HuffmanNode
from mpi4py import MPI
import numpy as np
import time
import sys

def decode_text(encoded_text, root):
    decoded_text = ''
    node = root

    for bit in encoded_text:
        node = node.left if bit == '0' else node.right

        if node.char is not None:
            decoded_text += node.char
            node = root

    return decoded_text

def find_error(encoded_text, root):
    value = ''
    node = root

    for bit in encoded_text:
        node = node.left if bit == '0' else node.right

        value += bit
        if node.char is not None:
            value = ''
            node = root

    return value

def huffman_decompress(encoded_array, root):
    decoded_text = decode_text(encoded_array, root)
    return decoded_text

def divide_encode_string(cadena, root):
    if len(cadena) <= 500:
        return find_error(cadena, root)

    mitad = len(cadena) // 2
    result1 = divide_encode_string(cadena[:mitad], root)
    result2 = divide_encode_string(result1 + cadena[mitad:], root)

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
        compressed_filename = sys.argv[1]
        with open(compressed_filename, 'rb') as f:
            compressed = bin(int.from_bytes(np.load(f, allow_pickle=True), byteorder='big'))[2:]
            root = HuffmanNode.from_array(np.load(f, allow_pickle=True))
            file_format, ENCODING = np.load(f, allow_pickle=True).tobytes().decode(), np.load(f, allow_pickle=True).tobytes().decode()

        root = comm.bcast(root, root=0)
        tam_compressed = len(compressed)
        length_packages = 10000
        total = tam_compressed // length_packages
        residue = tam_compressed % length_packages
        packages = divide_string(compressed, total)

        cont = 0
        stack = [i for i in range(1, size)]
        while len(packages) > 0:
            index = stack.pop(0)
            value = divide_encode_string(packages[0], root)
            packages[0] = packages[0][:len(packages[0]) - len(value)]
            if len(packages) > 1:
                packages[1] = value + packages[1]
            comm.send((packages.pop(0), cont), dest=index)
            stack.append(index)
            cont += 1

        decompressed = []
        for i in range(1, size):
            comm.send(None, dest=i)
            decompressed += comm.recv(source=MPI.ANY_SOURCE)

        decompressed = sorted(decompressed, key=lambda x: x[1])
        decompressed = np.array(decompressed)[:, 0]

        decompressed_filename = f"descomprimidop-elmejorprofesor.{file_format}"
        with open(decompressed_filename, 'wb') as f:
            decoded_text = ''.join(decompressed)
            f.write(decoded_text.encode(ENCODING))

        end_time = time.time()
        total_time = end_time - start_time
        print(f"{total_time:.2f}")

    else:
        root = comm.bcast(None, root=0)
        values = []
        while True:
            data = comm.recv(source=0)

            if data is None:
                break

            encoded_array, indice = data
            decoded_text = huffman_decompress(encoded_array, root)
            values.append((decoded_text, indice))

        comm.send(values, dest=0)