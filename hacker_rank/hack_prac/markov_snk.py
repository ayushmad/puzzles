import random

class Die:
    """
        Die class represents a die being inti lazied.
        It takes the die configuration in its constructor and 
        provides the following A.P.I's:-
        roll :- generates a number in the range given the probabilites
        get_configuration :- returns the configuration of the die
        previous_roll :-  returns the previous roll of the die.
        faces :- returns the number of faces in the die
    """
    def __init__(self, die_configuration):
        """
        Input:- Die configuration
        """
        self.side_count = len(die_configuration);
        # Storing probabilities as a sum count
        self.limiting_configuration = [];
        base_sum = 0.0;
        for entry in die_configuration:
            base_sum += entry;
            self.limiting_configuration.append(base_sum);

        print self.limiting_configuration;
            
        self.previous_roll = None;

    def roll(self):
        """
        Simulates a random roll returns the value for the face 
        Note :-  Rolls are on a 1 based index 
        """
        res = random.random();
        for index, val in enumerate(self.limiting_configuration):
            if val >= res:
                return index+1;
        return self.side_count;

    def faces(self):
        """
            returns the count of faces in die
        """
        return self.side_count;

    def get_configuration(self):
        """
            Returns the maximum probability with which a value is returned
        """
        return [(index+1, value) for index, val in enumerate(self.limiting_configuration)];




class Board:
    def __init__(self, snakes, ladders, board_size = 100):
        self.board_size = 100;
        self.current_position = 0;
        self.end_postion = board_size;
        self.ladders = {mouth: tail for [mouth, tail] in ladders};
        self.snakes = {mouth: tail for [mouth, tail] in snakes};
    
    def has_won(self, pos):
        if pos == self.board_size:
            return True;
        return False;

    def has_over_short(self, pos):
        if pos > self.board_size:
            return True;
        return False;
    
    def snake_bite(self, position):
        if self.snakes.has_key(position):
            return self.snakes[position];
        return position;
    
    def ladder_ride(self, position):
        if self.ladders.has_key(position):
            return self.ladders[position];
        return position;

    def move_board(self, count):
        self.current_position += count;
        if self.has_won(self.current_position):
            return True;
        elif self.has_over_short(self.current_position):
            self.current_position -= count;
        else:
            # Going through snakes and ladders till position does not become static
            prev_position = None;
            step = 0;
            while prev_position != self.current_position:
                prev_position = self.current_position;
                self.current_position = self.snake_bite(prev_position);
                prev_position = self.current_position;
                self.current_position = self.ladder_ride(prev_position);
                if step > 100:
                    raise Exception("Exception troublesome board");
                step += 1;
        return False;

    def get_postion(self):
        return self.current_position;

    def reset_board(self):
        self.current_position = 0;
        self.prev_position = 0;
        
class Game:
    def __init__(self, die, board, step_limit):
        self.die = die;
        self.board = board;
        self.roll_count = 0;
        self.step_limit = 1000;

    def step_game(self):
        move_val = self.die.roll();
        return self.board.move_board(move_val);

    def simulate_game(self):
        step = 1;
        while step <= self.step_limit:
            res = self.step_game();
            if res:
                return step;
            step += 1;
        raise Exception('No result reached');

    def get_result_over_k_simulation(self, k):
        result = 0;
        count  = 0;
        while count < k:
            try:
                result += self.simulate_game();
            except:
                pass;
            self.board.reset_board();
            count += 1;
        return int(float(result)/float(k));



if __name__ == "__main__":
    test_case_count = int(raw_input());
    while test_case_count > 0:
        die_probabilites = map(float, raw_input().strip().split(','));
        ladder_count, snake_count = raw_input().strip().split(',');
        ladders = map(lambda x: map(int, x.split(',')), raw_input().split());
        snakes = map(lambda x: map(int, x.split(',')), raw_input().split());
        simuation_count = 5000;
        my_die = Die(die_probabilites);
        my_board = Board(snakes, ladders);
        my_game = Game(my_die, my_board, 1000);
        print my_game.get_result_over_k_simulation(5000);
        test_case_count -= 1;
