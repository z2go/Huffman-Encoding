"""
Huffman: 10451396 bits (~1.30MB)
UTF-7: 16229843 bits (~2.03MB)
UTF-8: 18548392 bits (~2.31MB)

UTF-8, which is default encoding, means 8 bits per character,
but since there are just 105 different characters, I really only need 7 bits per character

Huffman encoding saves 5778447 bits (~0.72MB) or ~35.6% from UTF-7
Huffman encoding saves 8096996 bits (~1.01MB) or ~43.7% from UTF-8

Obviously my output file is much bigger (8 times bigger!) because it uses UTF-8 and not actual binary
"""
import math
import queue

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
            if(char != "\ufeff"): #Ignores this problematic char
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

def create_code_map(root, prefix): #Had to add the second param for recursion

    dict = {}
    if(root.left_child == None):
        dict[root.c] = prefix
        return dict
    else:
        left_map = create_code_map(root.left_child, prefix + "0")
        right_map = create_code_map(root.right_child, prefix + "1")

        left_map.update(right_map)

        return left_map

def get_encode_bits(map):
    file_read = open("book.txt", 'r')
    file_write = open("encoded_book.txt",'w') #Decided to write it to a file even though it isn't necessary


    regular_length_per_letter = math.ceil(math.log2(len(letter_frequencies.items())))
    #This line gets the amount of bits for each character

    huffman_char_num = 0
    regular_char_num = 0

    lines = file_read.readlines()
    file_read.close()
    for line in lines:
        for char in line:
            if (char != "\ufeff"):
                binary_representation = map[char]
                file_write.write(binary_representation)

                huffman_char_num += len(binary_representation)
                regular_char_num += regular_length_per_letter

    file_write.close()

    print("Huffman Encoded Length: " + str(huffman_char_num))
    print("Regular Encoded Length: " + str(regular_char_num))
    print("Pct Saved: "+str(100*(1-huffman_char_num/regular_char_num)))


count_frequencies()

q = queue.PriorityQueue()

for item in letter_frequencies.items():

    q.put((item[1], item[0], TreeVertex(item[0], item[1], None, None)))
    #NOTE: The second element is purely for sorting:
    # if it isn't included then the tree will try and sort two TreeVertex classes
    # Since the only important thing to sort off of is the frequency, the second element is purely cosmetic
    # This is an easier way to sort them that doesn't use a comparator
    # When


root_vertex = build_tree(q)
code_map = create_code_map(root_vertex,"")
get_encode_bits(code_map)