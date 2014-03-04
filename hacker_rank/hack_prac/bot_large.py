class Mark_Zoid:
    def __init__ (self):
        self.state = "SEARCH_TASK";
        return;

    def update_board(self, board, bot_pos):
        self.table = board;
        self.bot = bot_pos;
        return;

    def distance_between_blocks(self, source, dest):
        return pow(source[0]-dest[0], 2) + pow(source[1]-dest[1], 2);
    
    def isclean(self,target_pos):
        dirty_marker = "d";
        if self.table[target_pos[0]][target_pos[1]] == dirty_marker:
            return False;
        return True;

    def find_nearest_dirty_block(self):
        index = 0;
        min_dist = float('inf');
        min_point = (-1, -1);
        for row in range(0, len(self.table)):
            for col in range(0, len(self.table[row])):
                if not self.isclean((row, col)):
                    selected_dist = self.distance_between_blocks(self.bot, (row, col));
                    if min_dist > selected_dist:
                        min_point = (row, col);
                        min_dist = selected_dist;
        return min_point;


    def move_for_target(self):
        cur_pos = self.bot;
        move = "NOP";
        min_distance = float('inf');
        if cur_pos[0] != 0:
            # Can go up
            next_pos = (cur_pos[0]-1, cur_pos[1])
            selected_dist = self.distance_between_blocks(next_pos, self.target_block);
            if min_distance > selected_dist:
                move = "UP";
                min_distance = selected_dist;
        if cur_pos[1] != 0:
            # Can go left
            next_pos = (cur_pos[0], cur_pos[1]-1)
            selected_dist = self.distance_between_blocks(next_pos, self.target_block);
            if min_distance > selected_dist:
                move = "LEFT";
                min_distance = selected_dist;
        if cur_pos[0] != len(self.table)-1:
            # Can go down
            next_pos = (cur_pos[0]+1, cur_pos[1])
            selected_dist = self.distance_between_blocks(next_pos, self.target_block);
            if min_distance > selected_dist:
                move = "DOWN";
                min_distance = selected_dist;
        if cur_pos[1] != len(self.table[cur_pos[0]])-1:
            # Can go right
            next_pos = (cur_pos[0], cur_pos[1]+1)
            selected_dist = self.distance_between_blocks(next_pos, self.target_block);
            if min_distance > selected_dist:
                move = "RIGHT";
                min_distance = selected_dist;
        return move;
    


    def next_task(self):
        if self.state == "SEARCH_TASK":
            ### identify the next block to clean
            self.target_block = self.find_nearest_dirty_block();
            if self.target_block != (-1, -1):
                self.state = "REACH_BLOCK";
                return self.next_task();
            else:
                return "NOP";
        elif self.state == "REACH_BLOCK":
            if self.target_block == self.bot:
                self.state = "ON_BLOCK";
                return self.next_task();
            else:
                return self.move_for_target();
        elif self.state == "ON_BLOCK":
            if self.isclean(self.target_block):
                self.state = "SEARCH_TASK";
                return self.next_task();
            else:
                return "CLEAN";


mk = Mark_Zoid();

"""
inp_stream = open('test.txt', 'r');
# Tail starts here
if __name__ == "__main__":
    pos = [int(i) for i in inp_stream.readline().strip().split()]
    board = [[j for j in inp_stream.readline().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)
"""

# Head ends here
def next_move(posr, posc, dimh, dimw, board):
    mk.update_board(board, (posr, posc));
    print mk.next_task();

# Tail starts here
if __name__ == "__main__":
    pos = [int(i) for i in raw_input().strip().split()]
    dim = [int(i) for i in raw_input().strip().split()]
    board = [[j for j in raw_input().strip()] for i in range(dim[0])]
    next_move(pos[0], pos[1], dim[0], dim[1], board)
