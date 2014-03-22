import sys
from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction
from collections import defaultdict

def nCk(n,k): 
  return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1))

def neighbours_of_dest_in(cur_grid, dest, node_count):
    global col, row;
    node_row = node_count/col;
    node_col = node_count%col;
    neighbours = [];
    if node_row > 0:
        res = (node_row-1)*col+node_col
        if ((cur_grid& 1 << res) > 0):
            neighbours.append(res);
    if node_col > 0:
        res = (node_row)*col+(node_col-1)
        if ((cur_grid& 1 << res) > 0):
            neighbours.append(res);
    if node_row < (row-1):
        res = (node_row+1)*col + node_col
        if (cur_grid& 1 << res) > 0:
            neighbours.append(res);
    if node_col < col-1:
        res = (node_row)*col + node_col + 1
        if (cur_grid& 1 << res) > 0:
            neighbours.append(res);
    return neighbours;





inp_stream = sys.stdin;

##################### Reading_row and column quantities
(row, col) = map(int, inp_stream.readline().split());
edges = {};
### Populating_edge table:
cur_row = 0;
while cur_row < row:
    row_val = map(int, inp_stream.readline().strip().split());
    cur_col = 0;
    while cur_col < col-1:
        node_index = cur_row*col+cur_col
        if not edges.has_key(node_index):
            edges[node_index] = {};
        if not edges[node_index].has_key(node_index+1):
            edges[node_index][node_index+1] = {};
        edges[node_index][node_index+1] = row_val[cur_col];
        if not edges.has_key(node_index+1):
            edges[node_index+1] = {};
        if not edges[node_index+1].has_key(node_index):
            edges[node_index+1][node_index] = {};
        edges[node_index+1][node_index] = row_val[cur_col];
        cur_col += 1
    cur_row += 1
cur_row = 0;
while cur_row < row-1:
    row_val = map(int, inp_stream.readline().strip().split());
    cur_col = 0;
    while cur_col < col:
        node_index = cur_row*col+cur_col
        next_index = (cur_row+1)*col + cur_col;
        if not edges.has_key(node_index):
            edges[node_index] = {};
        if not edges[node_index].has_key(next_index):
            edges[node_index][next_index] = {};
        edges[node_index][next_index] = row_val[cur_col];
        if not edges.has_key(next_index):
            edges[next_index] = {};
        if not edges[next_index].has_key(node_index):
            edges[next_index][node_index] = {};
        edges[next_index][node_index] = row_val[cur_col];
        cur_col += 1
    cur_row += 1

################################ Now All That is left is initialization ########################


cell_count = row*col
dp_table = {};
dp_table[1] = [float('inf')]*cell_count;
dp_table[1][0] = 0;

dp_table = defaultdict(lambda: [float('inf')]*(cell_count), dp_table);

for l in range(2, cell_count+1):
    l_count = 0;
    max_l_count = nCk(cell_count-1, l-1);
    cur_grid = (int(pow(2, l-1)-1) << 1) + 1;
    while l_count < max_l_count:
        cur_grid_bin = bin(cur_grid)[2:][::-1][1:];
        dest = 2;
        node_count = 1;
        for b in cur_grid_bin:
            if b == '1':
                source_grid = cur_grid & ~(dest);
                neighbours = neighbours_of_dest_in(source_grid, dest, node_count);
                min_val = float('inf');
                for neighbour in neighbours:
                    min_val = min(dp_table[source_grid][neighbour] + edges[node_count][neighbour], 
                                  min_val);
                dp_table[cur_grid][node_count] = min_val;
            dest = dest << 1;
            node_count += 1;
        l_count += 1;
        cur_num = cur_grid >> 1;
        temp_u = cur_num &(-cur_num);
        temp_v = cur_num + temp_u;
        cur_grid = ((temp_v + (((temp_v^cur_num)/temp_u) >> 2)) << 1) + 1;
cover_all = int(pow(2, cell_count))-1;
neighbours = neighbours_of_dest_in(cover_all&~(1), 1, 0);
min_val = float('inf');
for neighbour in neighbours:
    min_val = min(min_val, dp_table[cover_all][neighbour] + edges[neighbour][0]);
if min_val < float('inf'):
    print min_val;
else:
    print 0;
