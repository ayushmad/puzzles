import sys
from bisect import insort_left
'''
    This is a implementation of Expanding core branch bound method for 
    knapsack problem. The Paper refereed by this code is:-
    D Pisinger, An expanding-core algorithm for the exact 0-1 knapsack problem, European Journal of Operational Research 87 (1995) 

    This approach considers the basic Danzig lower bound for the  knapsack problem as the solution.
    It then recursively decides on adding or removing a element based the resultant solutions
'''


'''
    Implementation Notes:-
    1. We make come basic changes which will be corrected based on the performance requirement and question scenario
       a) We completely sort the list , this is done because the previous implementation of Horowitz-Sahani did not consider it 
          as a bottle neck.
       b) Also another reason for not sorting is the data arrived in a linear fashion and we can want to order it
          so as to make sure that the Quora constraints are regarding solutions are met. For more detail see next point.
    2. Now the quora constraints are added as following:-
        a) Select a knapsack having smaller number of elements
        b) If two knapSack exist then select the on lexical arrival time
       Even though we connot prove we think the constraint 2a) is met because the danig also places a lower bound on number of elements 
       in a set and the algorithm tries to stay as close
       Point 2b) has to be verified using iterations 
'''

ExceptionList_global = [];
current_lowerbound = 0;
capacity = 0;
entry_set = [];
TIME_WINDOW = 0;
prev_result_cache = '';
CACHE_STALE = True;

def det_2(a1, a2, b1, b2):
    return a1*b2 - a2*b1;

def get_bounding_values(element_list):
    global capacity;
    combined_weight = 0;
    combined_price = 0;
    ELEMENT_PRICE = 3;
    ELEMENT_WEIGHT = 4;
    index = 0;
    for index in xrange(0, len(element_list)):
        current_weight = element_list[index][ELEMENT_WEIGHT];
        if current_weight + combined_weight > capacity:
            return (index, combined_price, combined_weight);
        combined_weight += current_weight;
        combined_price += element_list[index][ELEMENT_PRICE];
    return (len(element_list), combined_price, combined_weight);


def get_exception_list(P, W, s, t, element_list, element_count):
    '''
        Input:-
            P - Current best price
            W - Current best weight
            s - current removal consideration
            t - current addition consideration
        Output:- 
            true -  If the function could improve the knapsack
            false - IF the function failed in improving the knapsack
        Assumption :- 
            a) There exists a Global Exception list
            b) There exists a Global current lowerbound variable
            c) The input set is augmented to have two elements having zero and infinite efficiency appended
            d) There is a global capacity variable
    '''
    # Also convert the globals to local specifically exception_list reference and capacity
    global ExceptionList_global, current_lowerbound, capacity;
    capacity_local = capacity;
    # Local weight and price position to be added now
    ELEMENT_PRICE = 3;
    ELEMENT_WEIGHT = 4;
    improved = False;
    if W <= capacity:
        if P > current_lowerbound:
            improved = True;
            current_lowerbound = P;
            ExceptionList_global = [];
        while True:
            if t >= element_count:
                return improved;
            pt = element_list[t][ELEMENT_PRICE];
            wt = element_list[t][ELEMENT_WEIGHT];
            # This is the expansion step since we assume sorted we let it be
            if det_2(P - current_lowerbound - 1, 
                     W - capacity,
                     pt,
                     wt) < 0 :
                return improved;
            if get_exception_list(P + pt, W + wt,
                                  s, t + 1, element_list, element_count):
                improved = True;
                ExceptionList_global.append(t);
            t += 1;
    else:
        while True:
            if s < 0:
                return improved;
            ps = element_list[s][ELEMENT_PRICE];
            ws = element_list[s][ELEMENT_WEIGHT];
            # This is the expansion step since we assume sorted we let it be
            if det_2(P - current_lowerbound - 1, 
                     W - capacity,
                     ps,
                     ws) < 0 :
                return improved;
            if get_exception_list(P - ps, W - ws,
                                  s - 1, t, element_list, element_count):
                improved = True;
                ExceptionList_global.append(s);
            s -= 1;
    return improved;
    
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

def get_best_result(time):
    global TIME_WINDOW, entry_set, ExceptionList_global, current_lowerbound, prev_result_cache;
    # CACHING CHECKING
    if not purge_older_entries(time - TIME_WINDOW) and not CACHE_STALE:
        if prev_result_cache != '':
            return prev_result_cache;
    if len(entry_set) == 0:
        return None;
    (bounding_variable, bounding_price, bounding_weight) = get_bounding_values(entry_set);
    ExceptionList_global = [];
    current_lowerbound = 0;
    entry_count = len(entry_set);
    # Avoiding trivial cases
    if bounding_variable != 0 and bounding_variable != entry_count:
        get_exception_list(bounding_price, 
                           bounding_weight, 
                           bounding_variable - 1, 
                           bounding_variable,
                           entry_set,
                           entry_count);
    # Resulting List by using hash to purify
    reject_hash = {};
    result_list = [];
    total_score = 0;
    selected_entry_count = 0;
    lower_index = 0;
    for element in ExceptionList_global:
        if element < bounding_variable:
            reject_hash[element] = 1;
        if element >= bounding_variable:
            result_list.append(entry_set[element][5]);
            total_score += entry_set[element][3];
            selected_entry_count += 1;
    while lower_index < bounding_variable:
        if not reject_hash.has_key(lower_index):
            result_list.append(entry_set[lower_index][5]);
            total_score += entry_set[lower_index][3];
            selected_entry_count += 1;
        lower_index += 1;
    result_list.sort();
    prev_result_cache = str(total_score) + " " + str(selected_entry_count) + " " + " ".join(map(str, result_list)); 
    return prev_result_cache;





inp_stream = sys.stdin;
story_id = 0;
# Processing input file
(count, TIME_WINDOW, capacity) = map(int, inp_stream.readline().split());
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
        res = get_best_result(int(entry_time));
        if res is not None:
            print res;
    count -= 1;
