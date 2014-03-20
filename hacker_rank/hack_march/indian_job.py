import sys


#################################################
############ Trivial Cases ######################

def is_viable(added_time, total_time):
    return (added_time <= (total_time*2));

def check_single_viability(added_time, total_time):
    return added_time <=  total_time;



#########################################################################
###################### LPT SCHEDULE #####################################
####Return 1 :- if possible
####Return -1 :- if not possible
####Return 0: if cant be sure##################################
def lpt(numbers, time_allowed):
    numbers.sort(reverse = True);
    pack1  = 0;
    pack2 = 0;
    for num in numbers:
        if pack1 < pack2:
            pack1 += num;
        else:
            pack2 += num;
    lpt_sol = max(pack1, pack2);
    opt_possible = float(lpt_sol)/(1.17);
    if lpt_sol <= time_allowed:
        return 1;
    if opt_possible > time_allowed:
        return -1;
    return 0;



#########################################################################
## Since the nearest possible solution seems to be pseudo polynomial ##
    

def is_heist_possible_larger(numbers, time_allowed):
    possible_sum = 0;
    total_sum = sum(numbers);
    cap_number_allowed = total_sum/2;
    cap_allowed = (1 << (cap_number_allowed))-1;
    gap = time_allowed - cap_number_allowed;
    part_gap = (1 << (cap_number_allowed-gap-1))-1;
    for num in numbers:
        added_values = ((possible_sum) << num) & cap_allowed;
        added_values = added_values | ( 1 << num-1);
        possible_sum = possible_sum | added_values;
        if possible_sum >= part_gap:
            return True;
    return False;
        



############### Running test cases #################
inp_stream = sys.stdin;
#inp_stream = open('test.txt', 'r');
test_case_count = int(inp_stream.readline());
while test_case_count > 0:
    (number_count, time_allowed) = map(int, inp_stream.readline().strip().split());
    numbers = map(int, inp_stream.readline().strip().split());
    ## Pruning zero numbers
    numbers = [num for num in numbers if num > 0];
    added_time = sum(numbers);
    if len(numbers) == 0:
        print "YES";
    elif max(numbers) > time_allowed:
        print "NO";
    elif not is_viable(added_time, time_allowed):
        print "NO";
    elif check_single_viability(added_time, time_allowed):
        print "YES";
    else:
        lpt_result = lpt(numbers, time_allowed);
        if lpt_result == 1:
            print "YES"
        elif lpt_result == -1:
            print "NO"
        else:
            if is_heist_possible_larger(numbers, time_allowed):
                print "YES";
            else:
                print "NO";
    test_case_count -= 1;
