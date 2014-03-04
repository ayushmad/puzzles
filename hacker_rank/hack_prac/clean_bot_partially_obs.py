class Mark_Zoid:
    def __init__ (self):
        self.state = "SEARCH_TASK";
        self.state_file = "ghost_mark_zoid.txt";
        self.observe_count = 0;
        # Hard coded as the board size is fixed any be populated alter programmatic
        self.observation_points = [(1, 1), (1, 3), (3, 1), (3, 3)];
        return;

    def update_board(self, board):
        self.table = board;
        return;

    def partialy_update_board(self, new_board):
        index = 0;
        for row in self.table:
            for col_no in range(self.table):
                if row[col_no] == 'o' and self.new_board[index][col_no] != 'o':
                    row[col_no] = self.new_board[index][col_no];
            index += 1;
    
    def update_bot(self, bot_pos):
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
    
    def load_state(self, board):
        try:
            state_fh = open(self.state_file, 'r');
            # First line is the current state
            self.state = state_fh.readline().strip();
            self.observe_count = int(state_fh.readline().strip());
            (t_x, t_y) = map(int, state_fh.readline().strip().split());
            self.target_block = (t_x, t_y);
            self.table = [];
            for line in state_fh:
                self.table.append(list(line.strip()));
            state_fh.close();
            self.partialy_update_board(board);
        except IOError:
            # No state here update board buddy;
            self.update_board(board);

        

    def save_state(self):
        out_fh = open(self.state_file, 'w');
        # First line is the current state
        out_fh.write("%s\n"%(self.state));
        out_fh.write("%d\n"%(self.observe_count));
        out_fh.write("%d\t%d\n"%(self.target_block[0], self.target_block[1]));
        for row in self.table:
            out_fh.write("%s\n"%("".join(row)));
        out_fh.close();


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
            # Moving Bot hence changing board
            self.table[self.bot[0]][self.bot[1]] = '-';
        return move;
    


    def next_task(self):
        if self.state == "SEARCH_TASK":
            ### identify the next block to clean
            self.target_block = self.find_nearest_dirty_block();
            if self.target_block != (-1, -1):
                self.state = "REACH_BLOCK";
                return self.next_task();
            else:
                # Moving to observation state
                self.state = "OBSERVE";
                return self.next_task();
        elif self.state == "REACH_BLOCK":
            # Is good to partially update the board when I am moving
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
                # Cleaning hence changing
                self.table[self.bot[0]][self.bot[1]] = '-';
                return "CLEAN";
        elif self.state == "OBSERVE":
            if self.observe_count > 3:
                self.observe_count += 1;
                return "NOP";
            else:
                target_pos = self.observation_points[self.observe_count];
                if self.bot == target_pos:
                    self.observe_count += 1;
                    self.state = "SEARCH_TASK";
                    return self.next_task();
                else:
                    self.target_block = target_pos;
                    return self.move_for_target();


    def run(self, board, bot_pos):
        self.load_state(board);
        self.update_bot(bot_pos);
        next_step = self.next_task();
        self.save_state();
        return next_step;


mk = Mark_Zoid();

def next_move(posr, posc, board):
    print mk.run(board, (posr, posc));

"""
inp_stream = open('test.txt', 'r');
# Tail starts here
if __name__ == "__main__":
    pos = [int(i) for i in inp_stream.readline().strip().split()]
    board = [[j for j in inp_stream.readline().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)
"""
if __name__ == "__main__":
    pos = [int(i) for i in raw_input().strip().split()]
    board = [[j for j in raw_input().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)
