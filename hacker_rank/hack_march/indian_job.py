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

###Iterative Pseudo polynomial

def can_be_mixed_larger(numbers, max_time):
    stack = [];
    pack1 = 0;
    pack2 = 0;
    index = 0;
    while True:
        failed_to_fill = False;
        while index < len(numbers):
            if pack1 > pack2:
                if pack2+numbers[index] > max_time:
                    failed_to_fill = True;
                    break;
                pack2 += numbers[index];
                stack.append((pack1+numbers[index], pack2, index+1));
            else:
                if pack1+numbers[index] > max_time:
                    failed_to_fill = True;
                    break;
                pack1 += numbers[index];
                stack.append((pack1, pack2+numbers[index], index+1));
            index += 1;
        if not failed_to_fill:
            return "YES";
        if len(stack) == 0:
            break;
        (pack1, pack2, index) = stack.pop();
    return "NO";
        
            




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

