import sys

###################################################################################################
############# Variables  ##########################################################################
################ val_range - The number values that can be formed by considering values from [1, range]
################ one_count - No of ones at any point
################ two_count - No of twos at any point

def unique_results_on_addition(one_count, two_count, val_range):
    if one_count > 0:
        return min(val_range, one_count+2*two_count);
    else:
        return min((val_range-1)/2, two_count);




def unique_results(one_count, two_count, val_range):
    ###### First base case where we take care of the range
    if two_count == 0:
        ###### Return no of ones or the range which ever is smaller
        return min(val_range, one_count);
    if val_range == 0:
        return 0;
    ######################################################
    ### Now to the tricky part
    two_exp_val = two_count;
    total_unique_val_covered = 0;
    cur_range = 0;
    cur_range_uninitlized = True;

    ##############################################################################
    ########## Normally we expect ranges to be not including the top part#########
    while two_exp_val > 0:
        ### These Exponent numbers would have been above range
        if pow(2, two_exp_val) > val_range:
            two_exp_val -= 1;
            continue;
        if cur_range_uninitlized:
            cur_range_uninitlized = False;
            cur_range = val_range - pow(2, two_exp_val);
        additive_unique_number = unique_results_on_addition(one_count, two_count- two_exp_val, cur_range);
        if additive_unique_number >= cur_range:
            ### Though this can be never greater see unique_results_on_addition for understanding the reason
            total_unique_val_covered += cur_range;
            ################## HERE WE MIGHT SET THE BREAK FLAG #####################################
        else:
            multiplicative_unique_number = unique_results(one_count, two_count - two_exp_val, cur_range);
            if multiplicative_unique_number > additive_unique_number:
                if multiplicative_unique_number >= cur_range:
                    ### Though this can be never greater see unique_results_on_addition for understanding the reason
                    total_unique_val_covered += cur_range;
                    ################## HERE WE MIGHT SET THE BREAK FLAG #####################################
                else:
                    total_unique_val_covered += multiplicative_unique_number;
            else:
                total_unique_val_covered += additive_unique_number;
        total_unique_val_covered += 1;
        cur_range = pow(2, two_exp_val) - pow(2, two_exp_val-1) - 1;
        two_exp_val -= 1;
    if one_count >0:
        total_unique_val_covered += 1;
    return total_unique_val_covered;



#inp_stream = sys.stdin;
inp_stream = open('test.txt', 'r');
test_case_count = int(inp_stream.readline().strip());
while test_case_count > 0:
    (ones, twos) = map(int, inp_stream.readline().strip().split());
    print unique_results(ones, twos, float('inf'));
    test_case_count -= 1;
