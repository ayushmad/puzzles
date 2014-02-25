import os
import sys

'''
I  think we can solve this problem with a DP solution of complexity n^3 but lets ee how it goes.
'''

#inp_stream = sys.stdin;
inp_stream = open('test.txt', 'r');
(flower_count, student_count) = map(int, inp_stream.readline().split());
flowers_cost = map(int, inp_stream.readline().split());
flowers_cost.sort(reverse=True);

result = 0;
for index in range(0, (flower_count/student_count)):
    result += sum(flowers_cost[index*student_count : (index+1)*student_count])*(index+1);

index += 1
result += sum(flowers_cost[student_count * index:])*(index+1)
print result;
