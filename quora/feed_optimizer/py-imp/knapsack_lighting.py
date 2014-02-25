import os
import sys

class KnapSackLighting:
    """
        This is a implementation of Horowitx - Sahani algorithm which is supposed to be lightning fast.
    """
    def __init__(self, height, time_window):
        self.__height__ = height;
        self.__time_window__ = time_window;
        self.__entry_set__ = [];
        self.best_sacks = [];
        return;

    def add_entry_to_set(self, story_id, time, score, height):
        self.update_entry_set(story_id, time, score, height);
        return;

    def get_sack(self, time):
        return self.compute_sack_fast(time);


    def get_dominating_sets(self, states, element_price, element_weight, capacity, encoding_basis):
        new_states = [(0,0,0)];
        current_weight = element_weight;
        next_state = 1;
        current_state = 0;
        states.append((float('inf'), 0, [0]))
        while min(states[next_state][0], current_weight) <= capacity:
            if states[next_state][0] <= current_weight:
                current_encoding = states[next_state][2];
                current_price = states[next_state][1];
                if current_weight == states[next_state][0]:
                    if states[current_state][1] + element_price > current_price:
                        current_price = states[current_state][1] + element_price;
                        current_encoding = states[current_state][2] +  encoding_basis;
                    current_state += 1;
                    current_weight = states[current_state][0] + element_weight;
                # Check is the value is not dominated
                if current_price > new_states[-1][1]:
                    new_states.append((states[next_state][0],
                                       current_price, 
                                       current_encoding));
                next_state += 1;
            else:
                # Check is the value is not dominated
                if states[current_state][1] + element_price > new_states[-1][1]:
                    new_states.append((current_weight, 
                                      states[current_state][1] + element_price,  
                                      states[current_state][2] + encoding_basis));
                current_state += 1;
                current_weight = (states[current_state][0] + element_weight);
        return new_states;
    
    
    def get_dominating_knapsack(self, capacity, entry_set):
        entry = entry_set[0];
        new_states = [(0, 0, 0), 
                      (entry[3], entry[2], 1)]
        encoding_basis = 2;
        for entry_index in xrange(1, len(entry_set)):
            entry = entry_set[entry_index];
            new_states = self.get_dominating_sets(new_states,
                                                  entry[2],
                                                  entry[3],
                                                  capacity,
                                                  encoding_basis);
            encoding_basis *= 2;
        return new_states;

    def merge_dominating_sets(self, 
                              dsg1, 
                              dsg2,
                              split_basis,
                              capacity):
        # Note each dominating set is sorted by value inherently
        # Hence we need to find the first pair which satisfies the result
        # TODO : - Merging can be improved
        """
        print "=================================================="
        print dsg1;
        print dsg2;
        print "=================================================="
        """
        new_entry = [];
        (max_weight, max_cost, max_encoding) = dsg1[-1];
        for entry1 in reversed(dsg1):
            # first_entry_accepted = True;
            (w1, c1, en1) = entry1;
            for entry2  in reversed(dsg2):
                (w2, c2, en2) = entry2;
                if c1 + c2 > max_cost:
                    if w1 + w2 <= capacity:
                        max_encoding = (en2*pow(2, split_basis)) + en1;
                        max_weight = w1 + w2;
                        max_cost = c1 + c2;
                        """
                        print "++++++++++++++++++++++++++++++"
                        print entry1
                        print entry2
                        print "++++++++++++++++++++++++++++++"
                    if first_entry_accepted:
                        break;
                if first_entry_accepted:
                    first_entry_accepted = False;
            if first_entry_accepted:
                break;
            """
        return (max_weight, max_cost, max_encoding);

    def horowitz_sahani_knapsack(self):
        entry_set = self.__entry_set__;
        capacity = self.__height__;
        entry_count = len(entry_set);

        if entry_count > 4:
            dominating_sets_group1 = self.get_dominating_knapsack(capacity,
                                                                  entry_set[:entry_count/2]);
            dominating_sets_group2 = self.get_dominating_knapsack(capacity,
                                                                  entry_set[entry_count/2:]);

            return self.merge_dominating_sets(dominating_sets_group1, 
                                              dominating_sets_group2,
                                              entry_count/2,
                                              capacity);
        else:
            result_set = self.get_dominating_knapsack(capacity,
                                                      entry_set);
            return result_set[-1];

                 
    def compute_sack_fast(self, time):
        self.purge_older_entries(time - self.__time_window__);
        if len(self.__entry_set__) == 0:
            return None;
        
        dominated_sack = self.horowitz_sahani_knapsack();
        """
        print dominated_sack;
        print self.__entry_set__;
        print "-----------------------------------------";
        """
        selected_encoding = format(dominated_sack[2], 'b');
        selected_encoding = selected_encoding[::-1]
        final_list = [];
        for term_index in xrange(0, len(selected_encoding)):
            if selected_encoding[term_index] == '1':
                final_list.append(self.__entry_set__[term_index][0]);
        final_list.sort();
        # print final_list;
        return str(dominated_sack[1]) + " " + str(len(final_list)) + " " + " ".join(map(str, final_list));

    def update_entry_set(self, story_id, time, score, height):
        # Protect against zero height
        if height == 0:
            return;
        ratio_of_entry = float(score)/float(height);
        insert_success_flag = False;
        for index in xrange(0, len(self.__entry_set__)):
            entry = self.__entry_set__[index]
            if ratio_of_entry  > float(entry[2])/float(entry[3]):
                insert_success_flag = True;
                self.__entry_set__.insert(index, (story_id, time, score, height));
                break;
        if not insert_success_flag:
            self.__entry_set__.append((story_id, time, score, height));
        return;

    def purge_older_entries(self, before_time):
        # Entry set has the entries in chronological order
        list_len = len(self.__entry_set__);
        index = 0;
        while index < list_len:
            if self.__entry_set__[index][1] < before_time:
                del self.__entry_set__[index]
                list_len -= 1;
            else:
                index += 1;
        return;


# inp_stream = sys.stdin;
# inp_stream = open('test.txt', 'r');
inp_stream = open('test.in', 'r');
story_id = 0;
# Processing input file
(count, time_window, height) = map(int, inp_stream.readline().split());
my_kp = KnapSackLighting(height, time_window);
while count > 0:
    entry_line = inp_stream.readline();
    # print entry_line;
    (event_type, entries) = entry_line.split(None, 1);
    entries =  entries.split();
    # New story has come
    if event_type == "S":
        story_id += 1;
        (entry_time, score, height) = entries;
        my_kp.add_entry_to_set(story_id, int(entry_time), int(score), int(height));
    else:
        (entry_time) = entries[0];
        res = my_kp.get_sack(int(entry_time));
        if res is not None:
            print res;
    count -= 1;
