import os
import sys
import math
import random
from bisect import insort_left

current_lowerbound = 0;
capacity = 0;
entry_set = [];
TIME_WINDOW = 0;
prev_result_cache = '';
CACHE_STALE = True;
'''
This is a implication of the simulated annealing method for knap-sack problem 
The values of constants are taken from paper :- 
'''
class Annealer:
    K_CONTSTANT = 1;
    
    def __init__(self, start_temp, cooling_factor, rerun_count):
        self.start_temp = start_temp;
        self.cooling_factor = cooling_factor;
        self.rerun_count = rerun_count;
        self.price_index = 3;
        self.weight_index = 4;
        return;
    
    def get_danzig_lowerbound(self, max_capacity):
        cumilative_weight = 0;
        cumilative_value = 0;
        PRICE_INDEX = self.price_index;
        WEIGHT_INDEX = self.weight_index;
        index = 0;
        for entry in self.entries:
            cur_weight = entry[WEIGHT_INDEX];
            if cur_weight + cumilative_weight > max_capacity:
                return (index-1, cumilative_value, cumilative_weight);
            cumilative_weight += cur_weight;
            cumilative_value += entry[PRICE_INDEX];
            index += 1;
        return (index, cumilative_value, cumilative_weight);

    def get_randomized_knapsack(self, entries, price_index, 
                                weight_index, capacity,
                                base_value, base_weight,
                                selection_vector, k_constant,
                                start_temp, cooling_factor):
        cur_temp = start_temp;
        entry_count = len(entries);
        best_val = base_value;
        best_selection = list(selection_vector);
        while cur_temp > 0.1:
            cur_value = base_value;
            cur_weight = base_weight;
            selected_indices = [];
            rejected_indices = [];
            for index in (0, len(selection_vector)):
                if selection_vector[index] == 1:
                    selected_indices.append(index);
                else:
                    rejected_indices.append(index);
            # Selecting a already selected element
            swap_in_index = selected_indices[random.randint(0, len(selected_indices))];
            
            cur_weight += entries[swap_in_index][weight_index];
            cur_value += entries[swap_in_index][price_index];
            swap_out_indices = [];
            while cur_weight > capacity:
                swap_out_index = rejected_indices[random.randint(0, len(selected_indices))];
                if swap_out_index not in swap_out_indices:
                    #print "swaping_out_stuff"
                    swap_out_indices.append(swap_out_index);
                    cur_weight -= entries[swap_out_index][weight_index];
                    cur_value -= entries[swap_out_index][price_index]; 
            e_diff = (cur_value - base_value);
            if base_value < cur_value:
                base_weight = cur_weight;
                base_value = cur_value;
                selection_vector[swap_in_index] = 1;
                for index in swap_out_indices:
                    selection_vector[index] = 0;
                if cur_value > best_val:
                    best_selection = list(selection_vector);
                    best_val = cur_value;
            else:
                factor = math.exp(e_diff/cur_temp)
                if random.random()<factor:
                    base_weight = cur_weight;
                    base_value = cur_value;
                    selection_vector[swap_in_index] = 1;
                    #print swap_out_indices;
                    for index in swap_out_indices:
                        selection_vector[index] = 0;
            cur_temp = cur_temp*cooling_factor;

        return (best_selection, 0, best_val);

    def calculate_best_knapsack(self, data_entries, capacity, entries_sorted = True):
        '''
            data_entries - list of entries in the knap-sack. Note they are assumed to be sorted
        '''
        self.entries = data_entries;
        (bounding_variable, bounding_value, bounding_capacity) = self.get_danzig_lowerbound(capacity);
        if bounding_variable == len(data_entries):
            return  (bounding_value, [1]*bounding_variable);
        elif bounding_variable == 0:
            return (0, [0]*bounding_variable);
        # TODO:- Write case when its all or none of the elements
        selection_vector = [1]*(bounding_variable+1);
        selection_vector.extend([0]*(len(data_entries) - (bounding_variable+1)));
        max_value = bounding_value;
        max_selection = selection_vector;
        for run_count in range(self.rerun_count):
            (result_vector, result_weight, result_value) = self.get_randomized_knapsack(self.entries, self.price_index, self.weight_index, capacity,
                                                                                        bounding_value, bounding_capacity, list(selection_vector),
                                                                                        Annealer.K_CONTSTANT, self.start_temp, self.cooling_factor);
            if max_value < result_value:
                max_selection = result_vector;
                max_value = result_value;
            # In case of equality choose one with smaller size or better lexical order
        return (max_value, max_selection);




def update_entry_set(story_id, time, score, height):
    # Protect against zero height
    global entry_set, CACHE_STALE;
    ratio_of_entry = float(height)/float(score);
    insort_left(entry_set, (ratio_of_entry, (-1*score), (-1*time), score, height, story_id));
    return;

def purge_older_entries(before_time):
    # Entry set has the entries in chronological order
    global entry_set;
    list_len = len(entry_set);
    index = 0;
    TIME = 2;
    purged_entries = False;
    while index < list_len:
        if (entry_set[index][TIME]*-1) < before_time:
            del entry_set[index]
            purged_entries = True;
            list_len -= 1;
        else:
            index += 1;
    return purged_entries;

def get_best_result(time, my_anneling_obj):
    global TIME_WINDOW, entry_set, prev_result_cache, CACHE_STALE, capacity;
    # CACHING CHECKING
    if not purge_older_entries(time - TIME_WINDOW) and not CACHE_STALE:
        if prev_result_cache != '':
            return prev_result_cache;
    if len(entry_set) == 0:
        return None;
    (max_value, max_selection) = my_anneling_obj.calculate_best_knapsack(entry_set, capacity);
    selected_entries = [];
    selected_entry_count = len(entry_set);
    for index in range(0, selected_entry_count):
        if max_selection[index] == 1:
            selected_entries.append(entry_set[index][5]);
    selected_entries.sort(); 
    prev_result_cache = str(max_value) + " " + str(len(selected_entries)) + " " + " ".join(map(str, selected_entries));
    return prev_result_cache;


    
    


#inp_stream = sys.stdin;
inp_stream = open('test.txt', 'r');
story_id = 0;
# Processing input file
(count, TIME_WINDOW, capacity) = map(int, inp_stream.readline().split());
my_anneling_obj = Annealer(1000, 0.5, 5);
while count > 0:
    entry_line = inp_stream.readline();
    # print entry_line;
    (event_type, entries) = entry_line.split(None, 1);
    entries =  entries.split();
    # New story has come
    if event_type == "S":
        story_id += 1;
        (entry_time, score, height) = entries;
        update_entry_set(story_id, int(entry_time), int(score), int(height));
    else:
        (entry_time) = entries[0];
        res = get_best_result(int(entry_time), my_anneling_obj);
        if res is not None:
            print res;
    count -= 1;
