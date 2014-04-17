line_count = int(raw_input().strip());
min_x = float('inf');
min_y = float('inf');
while line_count > 0:
     (cur_x , cur_y) = map(int, line.strip().split());
     min_x = (min_x, cur_x)[cur_x < min_x];
     min_y = (min_y, cur_y)[cur_y < min_y];
     line_count -= 1;
print min_x * min_y
