import sys
class PathFinder:
    def __init__(self, table, start_pos, end_pos, block_markers = []):
        self.table = table;
        self.start_pos = start_pos;
        self.target_pos = end_pos;
        self.parent_table = [[(-1, -1) for i in table[j]] for j in range(len(table))];
        self.block_markers = block_markers;

    
    def accept_move(self, move, traversed):
        if move in traversed:
            return False;
        for block_marker in self.block_markers:
            if self.table[move[0]][move[1]] == block_marker:
                return False;
        return True;

    def order_a_star(self, moves):
        target_pos = self.target_pos;
        moves.sort(key=lambda x: abs(target_pos[0]-x[0]) + abs(target_pos[1]-x[1]));
        return;
    
    def order_moves(self, moves):
        self.order_a_star(moves);
        return;

    def next_moves(self, cur_pos, traversed):
        next_moves = [];
        if cur_pos[0] != 0:
            # Can go up
            if self.accept_move((cur_pos[0]-1, cur_pos[1]), traversed):
                next_moves.append((cur_pos[0]-1, cur_pos[1]));
        if cur_pos[1] != 0:
            # Can go left
            if self.accept_move((cur_pos[0], cur_pos[1]-1), traversed):
                next_moves.append((cur_pos[0], cur_pos[1]-1));
        if cur_pos[0] != len(self.table)-1:
            # Can go down
            if self.accept_move((cur_pos[0]+1, cur_pos[1]), traversed):
                next_moves.append((cur_pos[0]+1, cur_pos[1]));
        if cur_pos[1] != len(self.table[cur_pos[0]])-1:
            # Can go right
            if self.accept_move((cur_pos[0], cur_pos[1]+1), traversed):
                next_moves.append((cur_pos[0], cur_pos[1]+1));
        self.order_moves(next_moves);
        return next_moves;

    def do_dfs(self):
        prev_move = (-1, -1);
        cur_move = self.start_pos;
        traversed = [cur_move]
        branching_stack = [];
        while cur_move != self.target_pos:
            next_move_list = self.next_moves(cur_move, traversed);
            """
            print cur_move
            print self.target_pos
            print next_move_list;
            print traversed;
            print branching_stack;
            pprint(self.table);
            pprint(self.parent_table);
            raw_input();
            """
            if len(next_move_list) == 0:
                (x, y) = branching_stack.pop();
                while (x, y) in traversed:
                    if len(branching_stack) == 0:
                        raise Exception("No Path to Target");
                    (x, y) = braching_stack.pop();
                prev_move = cur_move;
                cur_move = (x, y);
            else:
                prev_move = cur_move;
                cur_move = next_move_list[0];
            self.parent_table[cur_move[0]][cur_move[1]] = prev_move;
            traversed.append(cur_move);
            for mov in next_move_list[1:]:
                branching_stack.append((mov[0], mov[1]));
        # Exiting the while loop means acquiring target
        path = [];
        parent_node = self.target_pos;
        while parent_node != self.start_pos:
            path.append(parent_node);
            parent_node = self.parent_table[parent_node[0]][parent_node[1]];
        path.append(parent_node);
        # Path pushed in reverse order
        return path;
 
 
def find_point(marker, table):
    index = 0; 
    for row in table:
        try:
            pos = row.index(marker);
            return (index, pos);
        except ValueError:
            pass;
        index += 1;
def print_path(path_stack):
    move = "";
    cur_pos = path_stack.pop();
    while len(path_stack) > 0:
        next_pos = path_stack.pop();
        if cur_pos[0] < next_pos[0]:
            move +="DOWN\n";
        elif cur_pos[0] > next_pos[0]:
            move += "UP\n";
        elif cur_pos[1] > next_pos[1]:
            move += "LEFT\n";
        else:
            move += "RIGHT\n";
        cur_pos = next_pos;
    return move.strip();

def displayPathtoPrincess(n,grid):
    path_find = PathFinder(grid,
                    find_point("m", grid),
                    find_point("p", grid));
    
    print print_path(path_find.do_dfs());
    return;
    
"""
if __name__ == "__main__" :
    inp_stream = open('test.txt', 'r'); 
    grid_size = int(inp_stream.readline());
    grid = [list(inp_stream.readline().strip()) for j in range(grid_size)];
    displayPathtoPrincess(grid_size, grid);    
""" 

#print all the moves here
# Tail starts here
m = input()

grid = []
for i in xrange(0, m):
    grid.append(list(raw_input().strip()))

displayPathtoPrincess(m,grid)

