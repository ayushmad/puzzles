import sys
import math

def power_set(numbers, numb_count):
    mask = 0;
    added_sum = 0;
    num_rev = list(numbers);
    num_rev.reverse();
    while mask < pow(2, numb_count):
        mask_bin = bin(mask)[2:][::-1];
        current_xor = 0;
        index = 0;
        for mask_val in mask_bin:
            current_xor ^=  num_rev[index]*int(mask_val);
            index += 1;
        added_sum += current_xor;
        mask += 1;
    return added_sum;



inp_stream = sys.stdin;
test_case_count = int(inp_stream.readline().strip());
while test_case_count > 0:
    number_count = int(inp_stream.readline());
    numbers = map(int, inp_stream.readline().strip().split());
    print power_set(numbers, number_count);
    test_case_count -= 1;
