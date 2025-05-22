import heapq
from collections import defaultdict

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_tree(text):
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1

    heap = [Node(char, freq[char]) for char in freq]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]


def build_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}
    if node is not None:
        if node.char is not None:
            code_map[node.char] = prefix
        build_codes(node.left, prefix + "0", code_map)
        build_codes(node.right, prefix + "1", code_map)
    return code_map


def compress(text):
    root = build_tree(text)
    codes = build_codes(root)
    encoded_text = ''.join(codes[char] for char in text)

    # Save tree as string
    tree_structure = []
    tree_values = []

    def serialize(node):
        if node is None:
            return
        if node.char is not None:
            tree_structure.append('1')
            tree_values.append(node.char)
        else:
            tree_structure.append('0')
            serialize(node.left)
            serialize(node.right)

    serialize(root)

    header = ''.join(tree_structure) + '|' + ''.join(tree_values)
    return header + '|' + encoded_text


def deserialize(header_bits, header_chars):
    def helper():
        nonlocal i, j
        if i >= len(header_bits):
            return None
        if header_bits[i] == '1':
            node = Node(header_chars[j], 0)
            i += 1
            j += 1
            return node
        else:
            i += 1
            left = helper()
            right = helper()
            node = Node(None, 0)
            node.left = left
            node.right = right
            return node

    i = j = 0
    return helper()


def decompress(data):
    try:
        header_bits, header_chars, encoded_text = data.split('|')
        root = deserialize(header_bits, header_chars)

        result = []
        node = root
        for bit in encoded_text:
            node = node.left if bit == '0' else node.right
            if node.char is not None:
                result.append(node.char)
                node = root

        return ''.join(result)
    except Exception as e:
        raise ValueError("Invalid compressed file format") from e
