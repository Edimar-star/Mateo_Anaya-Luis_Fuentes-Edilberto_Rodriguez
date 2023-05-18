
# Compressor and descompressor

The Huffman File Compression and Decompression App is a powerful Python application designed to compress and decompress files using the efficient Huffman algorithm. It offers the flexibility of performing these operations in both sequential and parallel modes, allowing users to optimize their workflow based on their specific needs.


## Features

- The app enables users to compress files of various formats, reducing their size while preserving the original data. It achieves this through the Huffman coding technique, which assigns shorter codes to more frequently occurring characters in the file, leading to efficient compression.

- Users can effortlessly decompress previously compressed files, restoring them to their original format and size. The app utilizes the Huffman decoding process to reconstruct the original data from the compressed file.

- In the sequential mode, the app performs compression and decompression tasks using a single thread, making it suitable for small to medium-sized files. It provides a straightforward and reliable approach to processing files one at a time.

- For large files or users seeking to leverage the power of multiple CPU cores, the app offers a parallel mode. It utilizes parallel processing techniques to distribute the workload across multiple threads, significantly reducing the time required for compression and decompression operations.

- The app employs various optimization techniques, such as using data structures like priority queues and binary heaps, to enhance the speed and efficiency of the Huffman compression and decompression processes. It strives to deliver fast and reliable performance for both sequential and parallel operations.

- The app incorporates robust error handling and validation mechanisms to ensure the integrity of the compressed and decompressed files. It performs thorough checks during the process to detect and report any anomalies or errors, providing users with confidence in the results.



## Installation

If you already have a working MPI (either if you installed it from sources or by using a pre-built package from your favourite GNU/Linux distribution) and the mpicc compiler wrapper is on your search path, you can use pip:

```bash
  pip install numpy
```

```bash
  python -m pip install mpi4py
```
## Usage

sequential mode, Compress the file

```bash
  python compresor.py LaBiblia.txt
```
Unzip the file

```bash
  python descompresor.py comprimido.elmejorprofesor
```
Check if both files are the same

```bash
  python verificador.py LaBiblia.txt descomprimido-elmejorprofesor.txt 
```
parallel mode, Compress the file

```bash
  mpiexec -n 4 -oversubscribe --allow-run-as-root compresorp.py LaBiblia.txt
```


Unzip the file

```bash
    mpiexec -n 4 -oversubscribe --allow-run-as-root descompresorp.py comrprimidop.elmejorprofesor
```

Check if both files are the same

```bash
  python verificador.py LaBiblia.txt descomprimidop-elmejorprofesor.txt 
```
## Tech Stack

**App:** Python, numpy, mpi4py

## Authors

- [@Edilberto Rodriguez](https://github.com/Edimar-star)
- [@Luis Fuentes](https://github.com/luisda190519)
- [@Mateo Anaya](https://github.com/MT1120)


## Support

For support, email edilbertof@uninorte.edu.co

