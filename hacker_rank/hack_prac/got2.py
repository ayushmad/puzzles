import sys
import math



def calculate_resulting_anagrams(result_hash):
    anagram_count = 0;
    odd_count = 0;
    divide_val = 1;
    for (char, count) in char_hash.items():
        if count % 2 == 1:
            odd_count += 1;
            if odd_count > 1:
                return 0;
        if count > 1:
            anagram_count += count/2;
            divide_val *= math.factorial(count/2);
    return math.factorial(anagram_count)/divide_val;



inp_stream = open('test.txt', 'r');
char_stream = inp_stream.readline().strip();
char_hash = {};
for char in char_stream:
    if not char_hash.has_key(char):
        char_hash[char] = 0;
    char_hash[char] += 1;
print int(calculate_resulting_anagrams(char_hash) % 1000000007);
