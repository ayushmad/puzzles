import sys

table = [];

def start_point():
    herm_marker = "M";
    index = 0;
    for row in table:
        try:
            pos = row.index('M');
            return (index, pos);
        except ValueError:
            pass;
        index += 1;



def target_point():
    exit_marker = "*";
    index = 0; 
    for row in table:
        try:
            pos = row.index('*');
            return (index, pos);
        except ValueError:
            pass;
        index += 1;

def next_moves(cur_pos, prev_pos, traversed):
    next_moves = [];
    if cur_pos[0] != 0:
        # Can go up
        if table[cur_pos[0]-1][cur_pos[1]] != "X":
            next_moves.append((cur_pos[0]-1, cur_pos[1]));
    if cur_pos[1] != 0:
        # Can go left
        if table[cur_pos[0]][cur_pos[1]-1] != "X":
            next_moves.append((cur_pos[0], cur_pos[1]-1));
    if cur_pos[0] != len(table)-1:
        # Can go down
        if table[cur_pos[0]+1][cur_pos[1]] != "X":
            next_moves.append((cur_pos[0]+1, cur_pos[1]));
    if cur_pos[1] != len(table[0])-1:
        # Can go right
        if table[cur_pos[0]][cur_pos[1]+1] != "X":
            next_moves.append((cur_pos[0], cur_pos[1]+1));
    accepted_next_moves = []
    for move in next_moves:
        if move != prev_pos and move not in traversed:
            accepted_next_moves.append(move);
    return accepted_next_moves;

def do_dfs():
    start_pos = start_point();
    target_pos = target_point();
    braching_stack = [];
    prev_move = (-1, -1);
    cur_move = start_pos;
    traversed = [start_pos]
    branch = 0;
    while cur_move != target_pos:
        next_move_list = next_moves(cur_move, prev_move, traversed);
        """
        print cur_move
        print target_pos
        print next_move_list;
        print traversed;
        print braching_stack;
        print len(table);
        print len(table[0]);
        raw_input();
        """
        if len(next_move_list) == 0:
            (x, y, branch) = braching_stack.pop();
            prev_move = cur_move;
            cur_move = (x, y);
        else:
            prev_move = cur_move;
            cur_move = next_move_list[0];
        traversed.append(cur_move);
        if len(next_move_list) > 1:
            branch += 1;
        for mov in next_move_list[1:]:
            braching_stack.append((mov[0], mov[1], branch));
    return branch;




        

inp_stream = sys.stdin;
#inp_stream = open('test.txt', 'r');
test_case_count = int(inp_stream.readline());
while test_case_count > 0:
    (rows, cols) = map(int, inp_stream.readline().split());
    table = [list(inp_stream.readline().strip()) for i in range(rows)];
    wands = do_dfs(); 
    if wands == int(inp_stream.readline()):
        print "Impressed";
    else:
        print "Oops!";
    test_case_count -= 1;
