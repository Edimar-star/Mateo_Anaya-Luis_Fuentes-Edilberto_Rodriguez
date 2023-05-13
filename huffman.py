import numpy as np

class HuffmanNode:
    def __init__(self, freq, char=None):
        self.freq = freq
        self.char = char
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def to_array(self):
        return np.array([self.freq, self.char, self.left, self.right])

    @staticmethod
    def from_array(arr):
        nodo = HuffmanNode(arr[0], arr[1])
        nodo.left = arr[2]
        nodo.right = arr[3]

        return nodo
