import os
import math
import sys


def get_primes_till (till, return_table = False):
    """
        This Method implements the eschews Ian sheave
    """
    prime_table = [True] * till;
    primes = [];
    for num in xrange(2, till):
        if (prime_table[num]):
            primes.append(num);
            val = num + num;
            while val < till :
                prime_table[val] = False;
                val += num;
    return (primes, (primes, prime_table))[return_table];


def prob60():
    # Checking till 10000 till now
    MAX = 10000000
    #MAX = 1000000
    (primes, prime_map) = get_primes_till(MAX, True)
    # checking with the already present curve
    #four_group = ['3', '7', '109', '679']
    four_group = ['3', '7', '187', '793']
    for num in range(187, 10000):
    #for num in range(7, 1000):
        passed = True;
        for p1 in four_group:
            print (p1 + str(num))
            if not prime_map[int(p1 + str(num))]:
                passed = False;
                break;
            print (str(num) + p1)
            if not prime_map[int(str(num) + p1)]:
                passed = False;
                break;
        if passed:
            print "Selected number is ";
            print num;
            raw_input();

prob60();
