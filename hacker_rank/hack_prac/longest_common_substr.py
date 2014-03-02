import os
import math
import sys
import pprint;
pp = pprint.PrettyPrinter(indent=4);

def find_max_matching(str1, str2, mistakes):
    dp_table = [[[0 for j in range(0, len(str2)+1)] for i in range(0, len(str1)+1)] for k in range(0, mistakes+1)];
    max_val = 0;
    for mistake in range(0, mistakes+1):
        for i_str1 in range(0, len(str1)):
                i_str1_index = i_str1 + 1;
                for i_str2 in range(0, len(str2)):
                    i_str2_index = i_str2 + 1;
                    res = 0;
                    '''
                    print "------------------------------------------------"
                    print "Current index in str1 %d Current index in str2 %d"%(i_str1_index, 
                                                                               i_str2_index);
                    pp.pprint(dp_table);
                    raw_input();
                    '''
                    if str1[i_str1] == str2[i_str2]:
                        res = 1 +  dp_table[mistake][i_str1_index - 1][i_str2_index - 1];
                        dp_table[mistake][i_str1_index][i_str2_index] = res
                    else:
                        if mistake > 0:
                            res = 1 + dp_table[mistake-1][i_str1_index - 1][i_str2_index - 1];
                            dp_table[mistake][i_str1_index][i_str2_index] = res;
                        else:
                            dp_table[mistake][i_str1_index][i_str2_index] = 0;
                    if res > max_val:
                        max_val = res;
    return max_val;



if __name__ == "__main__":
    inp_stream = open('test.txt', 'r');
    test_case_count  = int(inp_stream.readline());
    while test_case_count > 0:
        (mistakes_allowed, str1, str2) = inp_stream.readline().split();
        print str1;
        print str2;
        print find_max_matching(str1, str2, int(mistakes_allowed));
        test_case_count -= 1;
