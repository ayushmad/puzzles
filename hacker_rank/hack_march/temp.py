import sys
import random
res = [];
l = open('test.txt','w');
row = random.randint(1, 11);
col = random.randint(1, 11);
l.write("%d %d\n"%(row, col)); 
cur_row = 0;
while cur_row < row:
    cur_col = 0;
    res = "";
    while cur_col < col -1:
        res = res + " " + str(random.randint(1, 900));
        cur_col += 1;
    res = res.strip();
    l.write("%s\n"%(res));
    cur_row += 1;
cur_row = 0;
while cur_row < row - 1:
    cur_col = 0;
    res = "";
    while cur_col < col:
        res = res + " " + str(random.randint(1, 900));
        cur_col += 1;
    res = res.strip();
    l.write("%s\n"%(res));
    cur_row += 1;
l.close();
