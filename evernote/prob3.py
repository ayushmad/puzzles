import sys


element_hash = {};
element_list = [];
unique_element = 0;
def add_word(word):
    global element_list, element_hash, unique_element;
    if not element_hash.has_key(word):
        element_hash[word] = unique_element;
        unique_element += 1;
        element_list.append([word, -1]);
    else:
        index = element_hash[word];
        entry = element_list[index];
        element_list[index] = [entry[0], entry[1] - 1];
    return;




inp_stream = sys.stdin
count = int(inp_stream.readline())
while count > 0:
    word = inp_stream.readline().strip();
    add_word(word);
    count -=1;

top_k_elements = int(inp_stream.readline());

# Note:- Don't need to sort but just doing it any way
element_list.sort(key = lambda x: (x[1], x[0]));
print_counter = 0;


while print_counter < top_k_elements:
    print element_list[print_counter][0];
    print_counter += 1;
