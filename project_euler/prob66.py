import os
import math
import sys

square_array = [];

for i in range(1, 100000):
    square_array.append((i*i));

def get_min_x(d):
    for y in square_array:
        x =  math.pow((y*d)+1, 0.5)

        if x%1 == 0:
            return x;
    raise "This does not satisfy the limit";


max_x = 0 ;
for i in range(61, 1000):
    # Removing perfect squares
    if i in square_array:
        continue;
    my_x = get_min_x(i);
    if my_x > max_x:
        max_x = my_x;
