import random

MOVE_LEFT = 1 << 1;
MOVE_RIGHT = 1 << 2;
MOVE_TOP = 1 << 3;
MOVE_BOTTOM = 1 << 4;

class Board:
    """
        Class is used to create a board and create board movement logic
        Methods :-
        generate_next_tile - Creates a new tile at one of the new places
        shift_<move> - collapse tiles in the move direction
        possible_<move> - returns the board after collapsing in move direction
        get_current_board - returns the current board
        get_possible_next_boards - returns the list of boards with all possible tile combination and positions
    """
    def __init__(self, board_size, board = None):
        self.board_size = board_size;
        self.save_hash = {};
        self.save_unique_id= 0;
        self.board = board;
        if (board == None):
            self.board = self.__generate_blank_board();
        return;

    def __generate_blank_board(self):
        return [[0]*self.board_size for i in range(0, self.board_size)];
    
    def __get_random_entry(self, entry_list):
        return random.choice(entry_list);

    def __get_possible_tiles(self):
        return [2,4];

    def __get_random_tile(self):
        tile_list = self.__get_possible_tiles();
        return self.__get_random_entry(tile_list);
    
    def __get_possible_spots(self):
        spots = [];
        for row in xrange(0, self.board_size):
            for col in xrange(0, self.board_size):
                if self.board[row][col] == 0:
                   spots.append((row, col));
        return spots;

    class __BoardEnumerator:
        """
            Given Board it iterates over the board in the movement direction as defined
            it returns the list for row cols in each movement
        """
        
        def __init__(self, board_size, move_direction):
            self.board_size = board_size;
            self.move_direction = move_direction;
            self.base = 0;
        
        def __iter__(self):
            return self;

        def next(self):
            if self.base >= self.board_size:
                raise StopIteration;
            if self.move_direction == MOVE_LEFT:
                enumerated_list =  [(self.base, col) for col in xrange(0, self.board_size)];
            elif self.move_direction == MOVE_RIGHT:
                enumerated_list =  [(self.base, (self.board_size - (col + 1))) for col in xrange(0, self.board_size)];
            elif self.move_direction == MOVE_TOP:
                enumerated_list =  [(row, self.base) for row in xrange(0, self.board_size)];
            else:
                enumerated_list =  [((self.board_size - (row + 1)), self.base) for row in xrange(0, self.board_size)];
            self.base += 1;
            return enumerated_list;

    def __collapse_tiles(self, move):
        """
            Collapse Tiles is based on a idea of enumerating the board in different ways
            and joining them again.
            We enumerate the board based on direction first into list of (row, col) pairs:
        """
        enum_obj = Board.__BoardEnumerator(self.board_size, move);
        for enum_entry in enum_obj:
            entries = [];
            for row, col in enum_entry:
                if (self.board[row][col] != 0):
                    entries.append(self.board[row][col]);
            # Now we join consecutive entries
            collapsed_entries = [];
            index = 0;
            while index < len(entries):
                if index != (len(entries) - 1) and entries[index] == entries[index+1]:
                    collapsed_entries.append(entries[index]*2);
                    index += 2;
                else:
                    collapsed_entries.append(entries[index]);
                    index += 1;
            index = 0;
            for row, col in enum_entry:
                if index < len(collapsed_entries):
                    self.board[row][col] = collapsed_entries[index];
                else:
                    self.board[row][col] = 0;
                index += 1;
        return;

    def __get_random_tile_spot(self):
        spots = self.__get_possible_spots();
        return self.__get_random_entry(spots);

    def update_tile_in_position(self, position, tile):
        self.board[position[0]][position[1]] = tile;
        

    def generate_next_tile(self):
        random_position = self.__get_random_tile_spot();
        random_tile = self.__get_random_tile();
        self.update_tile_in_position(random_position, random_tile);

    def shift_direction(self, move):
        self.__collapse_tiles(move);
    
    def get_current_board(self):
        """
            taking care of list reference
        """
        returnable_board = [[entry for entry in row] for row in self.board];
        return returnable_board;
        

    def get_possible_next_boards(self):
        next_board_list = [];
        possible_position = self.__get_possible_spots();
        possible_tiles = self.__get_possible_tiles();
        for position in possible_position:
            for tile in possible_tiles:
                save_board = self.get_current_board();
                self.update_tile_in_position(position, tile);
                next_board_list.append(self.get_current_board());
                self.board = save_board;
        return next_board_list;

    def update_board(self, board):
        self.board = board;
    
    def __sum_values_on_board(self):
        cost = 0;
        for row in self.board:
            for entry in row:
                cost += entry;
        return cost;

    
    def get_board_value(self):
        return self.__sum_values_on_board();

    def save_board(self):
        u_id = self.u_id;
        self.save_hash[u_id] = self.board;
        self.u_id += 1;
        return u_id;

    def restore_board(self, uid):
        self.board = self.save_hash[uid];
        del self.save_hash[uid];
        return;

    def is_game_over(self):
        for row in self.board:
            for entry in row:
                if entry == 0:
                    return False;
        return True;


                


class Player:
    """
    get_next_move - player returns a next move from the board based on his choice
    """
    def __init__(self, algorithm):
        self.algorithm = algorithm;
        return;

    def __select_next_move(self, moves):
        return moves[0];

    def play_move(self, board):
        move = self.algorithm.get_best_move(board);
        board.shift_direction(move);
        return move;


## We are dividing the code into main boards
## game. It provides the class which actually runs a game and by generating all its entities
## It needs to a algorithm object which its provides to player object to get the next move


class Game:
    def __init__(self, algorithm):
        self.player = Player(algorithm);
        self.board = None;

    def simulate_game(self):
        self.board = Board(4)
        while True:
            self.player.play_move(self.board);
            if self.board.is_game_over():
                break;
            self.board.generate_next_tile();
        return self.board.get_board_value();

    def mean_k_simulation(self, k):
        result = 0;
        best = float('-inf');
        worst = float('inf');

        for no in xrange(0, k):
            value = self.simulate_game();
            ## Check if value is acceptable;
            if value > best:
                best = value;
            elif value < worst:
                worst = value;
            result += value;
        return (best, float(result)/float(k), worst);


### This should be in a new file
class Algorithm:
    """"
    This is the base class we will be implementing versions of this tree which will be min-max based.
    We will be calling the structure a user-move, chance move
    The tree is generated using DFS we might even want to clean up table.
    This class extended should provide only the method evaluate_board which will be the main heuristic function
    """
    def __init__(self, depth):
        self.name = "Base Algorithm"
        self.depth = depth;
    
    def __expected_move(self, board_obj, depth):
        base_board = board_obj.get_current_board();
        board_list = board_obj.get_possible_next_boards();
        total_value = 0;
        count = len(board_list);
        for current_board in board_list:
            board_obj.update_board(current_board)
            (move, value) = self.__user_move(board_obj, depth);
            total_value += value;
        board_obj.update_board(base_board);
        if count == 0:
            return float('-inf');
        return float(total_value)/float(count);

    def __user_move(self, board_obj, depth):
        if depth <= 0:
            return (None, self.evalute_board(board_obj));
        base_board = board_obj.get_current_board();
        maximixing_value = float('-inf');
        maximizing_move = MOVE_LEFT;
        # moving left first
        move_list = [MOVE_LEFT,
                     MOVE_RIGHT,
                     
                     
                     MOVE_TOP,
                     MOVE_BOTTOM];
        for move_direction in move_list:
            board_obj.shift_direction(move_direction);
            value = self.__expected_move(board_obj, depth-1);
            if value > maximixing_value:
                maximizing_move = move_direction;
                maximixing_value = value;
            board_obj.update_board(base_board);
            base_board = board_obj.get_current_board();
        return (maximizing_move, maximixing_value);
        

    def get_best_move(self, board_obj, depth = 1):
        # Get best move is called when user has a chance to move so we are going to be calling user - chance
        current_board_grid = board_obj.get_current_board();
        # Making a decision board to play around with it
        new_board_obj = Board(len(current_board_grid), current_board_grid);
        (move, value) = self.__user_move(new_board_obj, depth);
        return move;




class MaxValue(Algorithm):
    def __init__(self, depth):
        Algorithm.__init__(self, depth);
        return;
    
    def evalute_board(self, board_obj):
        return board_obj.get_board_value();

class MaxEmptyCells(Algorithm):
    def __init__(self, depth):
        Algorithm.__init__(self, depth);
        return;
    
    def evalute_board(self, board_obj):
        board = board_obj.get_current_board();
        value = 0;
        for row in board:
            for entry in row:
                if entry == 0:
                    value += 1;
        return value;


if __name__ == "__main__":
    algo = MaxEmptyCells(2);
    my_game = Game(algo);
    for count in range(0, 1):
        (best, median, worst) = my_game.mean_k_simulation(5000)
        print "Iteration %d Best value %f Average Value %f, Worst Value %f"%(count, 
                                                                             best,
                                                                             median,
                                                                             worst);
