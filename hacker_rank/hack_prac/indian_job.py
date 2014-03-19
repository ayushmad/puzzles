import sys


#################################################
############ Trivial Cases ######################

def is_viable(added_time, total_time):
    return (added_time <= total_time*2);

def check_single_viability(added_time, total_time):
    return added_time <=  total_time;


############################################
######### Small Case #######################

def can_be_mixed(numbers, pipe_line, pos, max_time):
    if pos == len(numbers):
        if pipe_line[0] <= max_time and pipe_line[1] <= max_time:
            return True;
    else:
        return can_be_mixed(numbers, 
                            (pipe_line[0]+numbers[pos],  pipe_line[1]), 
                            pos + 1, 
                            max_time) or can_be_mixed(numbers, 
                            (pipe_line[0], numbers[pos] + pipe_line[1]), 
                            pos + 1, 
                            max_time);
                



#########################################################################
## Since the nearest possible solution seems to be pseudo polynomial ####
## Applying toth algorithm#################

ExceptionList_global = 0;
current_lowerbound = 0;

def det_2(a1, a2, b1, b2):
    return a1*b2 - a2*b1;

def get_bounding_values(element_list, capacity):
    combined_weight = 0;
    index = 0;
    for index in xrange(0, len(element_list)):
        current_weight = element_list[index];
        if current_weight + combined_weight > capacity:
            return (index, combined_weight, combined_weight);
        combined_weight += current_weight;
    return (0, 0, 0);


def get_exception_list(P, W, s, t, element_list, element_count, capacity):
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
    global ExceptionList_global, current_lowerbound;
    capacity_local = capacity;
    # Local weight and price position to be added now
    improved = False;
    if W <= capacity:
        if P > current_lowerbound:
            improved = True;
            current_lowerbound = P;
            ExceptionList_global = [];
        while True:
            if t >= element_count:
                return improved;
            pt = element_list[t];
            wt = element_list[t];
            # This is the expansion step since we assume sorted we let it be
            if det_2(P - current_lowerbound - 1, 
                     W - capacity,
                     pt,
                     wt) < 0 :
                return improved;
            if get_exception_list(P + pt, W + wt,
                                  s, t + 1, element_list, element_count, capacity):
                improved = True;
                ExceptionList_global.append(t);
            t += 1;
    else:
        while True:
            if s < 0:
                return improved;
            ps = element_list[s];
            ws = element_list[s];
            # This is the expansion step since we assume sorted we let it be
            if det_2(P - current_lowerbound - 1, 
                     W - capacity,
                     ps,
                     ws) < 0 :
                return improved;
            if get_exception_list(P - ps, W - ws,
                                  s - 1, t, element_list, element_count, capacity):
                improved = True;
                ExceptionList_global.append(s);
            s -= 1;
    return improved;



def can_be_mixed_larger(element_list, capacity):
    global ExceptionList_global, current_lowerbound;
    current_lowerbound = 0;
    ExceptionList_global = [];
    element_list.sort();
    ## Checking if first element enters
    if element_list[0] > capacity:
        return False

    (last_pos, count, size) = get_bounding_values(element_list, capacity);
    print get_bounding_values(element_list, capacity);
    get_exception_list(count,
                       size,
                       last_pos - 1,
                       last_pos,
                       element_list,
                       len(element_list),
                       capacity);
    ExceptionList_global.sort();
    print ExceptionList_global;
    rest_sum = sum(element_list[last_pos-1:]);
    for index in ExceptionList_global:
        if index < last_pos:
            rest_sum += element_list[index];
        else:
            rest_sum -= element_list[index];
    return rest_sum <= capacity;



############### Running test cases #################
inp_stream = sys.stdin;
test_case_count = int(inp_stream.readline());
while test_case_count > 0:
    (number_count, time_allowed) = map(int, inp_stream.readline().split());
    numbers = map(int, inp_stream.readline().split());
    added_time = sum(numbers);
    if not is_viable(added_time, time_allowed):
        print "NO";
    elif check_single_viability(added_time, time_allowed):
        print "YES";
    elif len(numbers) < 5: 
        if can_be_mixed(numbers, (0, 0), 0, time_allowed):
            print "YES";
        else:
            print "NO"; 
    else:
        if can_be_mixed_larger(numbers, time_allowed):
            print "YES";
        else:
            print "NO"
    test_case_count -= 1;

