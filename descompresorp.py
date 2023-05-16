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
    if len(cadena) <= 500:
        return remove_prefixes(cadena, trieRoot)

    mitad = len(cadena) // 2
    result1 = eliminar_repetidos(cadena[:mitad], trieRoot)
    result2 = eliminar_repetidos(result1 + cadena[mitad:], trieRoot)

    return result2

def sendPackage(end_index, start_index, length_packages, residue, compressed, root, packages_sended, dest, trieRoot):
    end_index = start_index + length_packages + residue
    temp_compressed = compressed[start_index:end_index]
    residue = len(eliminar_repetidos(temp_compressed, trieRoot))
    end_index = end_index - residue
    comm.send((root, temp_compressed[:end_index], packages_sended), dest=dest)
    start_index = end_index
    packages_sended += 1

    return end_index, start_index, residue, packages_sended

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

        # Inicializo variables primordiales
        tam_compressed = len(compressed)
        length_packages = 100000
        total = tam_compressed // length_packages
        residue = tam_compressed % length_packages
        start_index = 0
        end_index = 0

        # Envio de paquetes iniciales
        packages_sended = 0
        for i in range(1, size):
            values_rcv = sendPackage(end_index, start_index, length_packages, residue, compressed, root, packages_sended, i, trieRoot)
            end_index, start_index, residue, packages_sended = values_rcv

        # Recibo los resultados de todos los hijos
        decompressed = [0] * total
        tasks_done = 0
        while tasks_done < packages_sended:
            result, indice, dest = comm.recv(source=MPI.ANY_SOURCE)
            decompressed[indice] = result
            tasks_done += 1

            if start_index < tam_compressed:
                values_rcv = sendPackage(end_index, start_index, length_packages, residue, compressed, root, packages_sended, dest, trieRoot)
                end_index, start_index, residue, packages_sended = values_rcv
        
        # Aviso a todos los hijos que ya no voy a enviar mas paquetes
        for i in range(1, size):
            comm.send(None, dest=i)

        # Decompress the text
        decompressed_filename = f"descomprimidop-elmejorprofesor.{file_format}"
        with open(decompressed_filename, 'wb') as f:
            decoded_text = ''.join(decompressed)
            f.write(decoded_text.encode(ENCODING))

        end_time = time.time()
        total_time = end_time - start_time
        print(f"{total_time:.2f}")

    else:
        while True: # Mientras haya paquetes por recibir
            data = comm.recv(source=0)

            # Si no hay paquetes por recibir
            if data is None:
                break

            root, encoded_array, indice = data
            decoded_text = huffman_decompress(encoded_array, root)
            comm.send((decoded_text, indice, rank), dest=0)