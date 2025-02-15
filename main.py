import queue
from subprocess import check_output

letter_frequencies = {}

class TreeVertex:
    def __init__(self, c, weight, left_child, right_child):
        self.c = c
        self.weight = weight
        self.left_child = left_child
        self.right_child = right_child

def count_frequencies():
    file = open("book.txt",'r')
    lines = file.readlines()
    for line in lines:
        for char in line:
            if(char != "\ufeff"):
                try:
                    letter_frequencies[char] = letter_frequencies[char] + 1
                except KeyError:
                    letter_frequencies[char] = 1

    file.close()
    pass

def build_tree(freqs):
    while freqs.qsize() > 1:
        left_weight, left_char, left_tree = freqs.get()
        right_weight, right_char, right_tree = freqs.get()

        merged_weight = left_weight + right_weight
        merged_tree = TreeVertex(left_char + right_char, merged_weight, left_tree, right_tree)

        freqs.put((merged_weight, left_char + right_char, merged_tree))

    return freqs.get()[2]

def create_code_map(root, prefix):
    dict = {}
    if(root.left_child == None):
        dict[root.c] = prefix
        return {root.c, prefix}
    else:
        left_map = create_code_map(root.left_child, prefix + "0")
        right_map = create_code_map(root.right_child, prefix + "1")

        left_map.update(right_map)

        return left_map

count_frequencies()

q = queue.PriorityQueue()

for item in letter_frequencies.items():
    q.put((item[1], item[0], TreeVertex(item[0], item[1], None, None)))


root_vertex = build_tree(q)
code_map = create_code_map(root_vertex,"")
print(code_map)
