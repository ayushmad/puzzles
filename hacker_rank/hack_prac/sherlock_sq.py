import sys
import math


inp_stream = sys.stdin;
test_case_count = int(inp_stream.readline());
while test_case_count > 0:
    (top, bottom) = map(int, inp_stream.readline().strip().split());
    top_boundary = math.ceil(pow(top, 0.5));
    bottom_boundary = math.floor(pow(bottom, 0.5));
    print int(bottom_boundary - top_boundary + 1);
    test_case_count -= 1;
