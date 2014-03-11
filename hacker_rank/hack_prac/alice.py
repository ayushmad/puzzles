import sys
inp_stream = sys.stdin;
child_count = inp_stream.readline();
children = map(int, inp_stream.readline().strip().split());
total_candy_count_rev = [];
total_candy_count = [];
prev_rating = float('inf');
prev_candy = 1;
while child in children:
    if child <= prev_rating:
        candy_count = min(prev_candy - 1, 1);
    else:
        candy_count = 1 + prev_candy;
    total_candy_count.append(candy_count);
    prev_candy = candy_count;
    prev_rating = prev_candy
