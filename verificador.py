import sys
import os

if __name__ == "__main__":
    # Se obtienen los nombres de archivo de los argumentos de línea de comandos
    filename = sys.argv[1]
    decompressed_filename = sys.argv[2]

    # Se obtiene el tamaño en bytes de los archivos
    size1 = os.path.getsize(filename)
    size2 = os.path.getsize(decompressed_filename)
    diff = size2 - size1
    
    # Se abren los archivos en modo lectura binaria y se leen los contenidos
    with open(filename, "rb") as archivo1, open(decompressed_filename, "rb") as archivo2:
        try:
            # Se intenta decodificar los contenidos de los archivos utilizando "cp1252"
            archivo1 = archivo1.read().decode("cp1252")
            archivo2 = archivo2.read().decode("cp1252")
        except:
            # Si falla la decodificación con "cp1252", se intenta con "utf-8"
            archivo1 = archivo1.read().decode("utf-8")
            archivo2 = archivo2.read().decode("utf-8")
        
        # Se comparan las líneas de los archivos uno a uno
        for linea1, linea2 in zip(archivo1, archivo2):
            # Si se encuentra una diferencia entre las líneas, se imprime el resultado y se sale del bucle
            if linea1 != linea2:
                print(diff, "nok")
                break
        else:
            # Si no se encontraron diferencias entre las líneas de los archivos, se imprime el resultado
            print(diff, "ok")
