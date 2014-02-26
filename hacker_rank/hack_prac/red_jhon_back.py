import sys


def get_primes(till_number):
    if till_number <= 1:
        return 0;
    sieve = [False, False];
    sieve.extend([True]*(till_number-1))
    for index in range(2, till_number+1):
        if sieve[index]:
            cur_index = index + index;
            while cur_index <= till_number:
                sieve[cur_index] = False;
                cur_index += index;
    return sum([ 1 for ele in sieve if ele ]);



def get_possible_combinations(number):
    number -= 1; 
    if number < 3:
        return get_primes(1);
    dp_table = [1,1,1,2];
    pos = 4
    while pos <= number:
        flat_combn = dp_table[pos-4];
        standing_comb = dp_table[pos-1];
        dp_table.append(flat_combn+standing_comb);
        pos += 1;
    #return dp_table[-1];
    return get_primes(dp_table[-1]);


#inp_stream = sys.stdin;
inp_stream = open('test.txt', 'r');
#test_case_count = int(raw_input());
test_case_count = int(inp_stream.readline());
while test_case_count > 0:
    number = int(inp_stream.readline());
    print get_possible_combinations(number);
    test_case_count -= 1;
