import sys
import os

if __name__ == "__main__":
    filename = sys.argv[1]
    decompressed_filename = sys.argv[2]

    size1 = os.path.getsize(filename)
    size2 = os.path.getsize(decompressed_filename)
    diff = size2 - size1
    
    with open(filename, "rb") as archivo1, open(decompressed_filename, "rb") as archivo2:
        try:
            archivo1 = archivo1.read().decode("cp1252")
            archivo2 = archivo2.read().decode("cp1252")
        except:
            archivo1 = archivo1.read().decode("utf-8")
            archivo2 = archivo2.read().decode("utf-8")
        for linea1, linea2 in zip(archivo1, archivo2):
            if linea1 != linea2:
                print(diff, "nok")
                break
        else:
            print(diff, "ok")