import os
import math

def find_change_count(first_string, second_string):
    hash_first_string = {};
    unmatched_char = 0;
    for char in first_string:
        if not hash_first_string.has_key(char):
            hash_first_string[char] = 0;
        hash_first_string[char] += 1;

    for char in second_string:
        if hash_first_string.has_key(char):
            hash_first_string[char] -= 1
            if hash_first_string[char] == 0:
                del hash_first_string[char];
        else:
            unmatched_char += 1;
    
    return unmatched_char;


if __name__ == "__main__":
    inp_stream = open('test.txt', 'r');
    test_case_count = int(inp_stream.readline());
    while test_case_count > 0:
        added_string = inp_stream.readline().strip();
        if len(added_string) % 2 == 1:
            print -1;
        else:
            print find_change_count(added_string[:(len(added_string)/2)], added_string[(len(added_string)/2):]);
        test_case_count -= 1;
