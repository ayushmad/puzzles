import sys

inp_stream = sys.stdin;
data = list(inp_stream.readline());
char_hash = {};
for char in data:
    if not char_hash.has_key(char):
        char_hash[char] = 0;
    char_hash[char] += 1;

merged_list = [(char, char_hash[char]) for char in char_hash.keys()];
merged_list.sort(key = lambda x: x[0]);
result_str = "";
for entry in merged_list:
    result_str += entry[0]*(entry[1]/2);
print result_str;
