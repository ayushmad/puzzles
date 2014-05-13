import os
import math
import random
import sys

inp_stream = open("test.txt", "w");


total_bytes = 100000
no_of_bytes = total_bytes
latency = 100
download_rate = 150
chunk_count  = 2000
inp_stream.write("%s\n" % (total_bytes))
inp_stream.write("%s\n" % (latency))
inp_stream.write("%s\n" % (download_rate))
inp_stream.write("%s\n" % (chunk_count))


def output_proper_channel():
    global inp_stream
    global no_of_bytes
    pieces = 1000
    last_pos = 0
    start_val = 0
    stop_val = 0
    while start_val != no_of_bytes:
        start = start_val
        end = random.randint(start_val + no_of_bytes/pieces,
                             no_of_bytes)
        inp_stream.write("%d,%d\n"%(start, end))
        start_val = start_val + no_of_bytes/pieces;
        yield

def output_random_crap():
    global inp_stream
    global no_of_bytes
    count_time = 1000
    while count_time > 0:
        start = random.randint(0, no_of_bytes)
        end = random.randint(start, no_of_bytes)
        inp_stream.write("%d,%d\n"%(start, end))
        count_time -= 1
        yield

state_flag = True
proper_channel = output_proper_channel()
random_crap = output_random_crap()
while chunk_count > 0:
    if state_flag:
        next(proper_channel)
        state_flag = False
    else:
        next(random_crap)
        state_flag = True
    chunk_count -= 1

