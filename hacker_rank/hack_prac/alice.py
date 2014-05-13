import sys
inp_stream = sys.stdin;
child_count = inp_stream.readline();
data = inp_stream.read().split('\n');
print data
children = map(int, data);
print children;
