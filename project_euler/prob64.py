import os
import math
import sys

# This is can be later changed to a library


# Takes a number at removes all the square terms
def square_term(num):
    terms = range(2, int(math.ceil(math.pow(num, 2))));
    terms.reverse();
    for i in terms:
        if  num%(i*i) == 0:
            num = num/(i*i);
    return num;



def get_period(num):
    mprev = 0;
    dprev = 1;
    aprev = int(math.floor(math.pow(num, 0.5)));
    a0 = aprev;
    period = 0;
    while True:
        period += 1;
        mnext = dprev*aprev - mprev;
        dnext = (num - (mnext*mnext))/dprev
        anext =  int(math.floor((a0 + mnext)/dnext))
        if anext == 2*a0:
            return period;
        (mprev, dprev, aprev) = (mnext, dnext, anext);


odd_period = 0;
for i in range(2, 10000):
    if math.pow(i, 0.5)%1 == 0:
        continue;
    if not get_period(i)%2 == 0:    
        odd_period += 1;

print odd_period
