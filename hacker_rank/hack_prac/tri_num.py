import os
import sys

"""
    We are first going to write API to generate triangle numbers
    That will give us some idea about solution
"""


class TriNum:

    def __init__(self):
        self.tri_layer = [[1]]
        self.max_length = 20

    def gen_next_level(self):
        cur_level = self.tri_layer[-1]
        next_level = []
        pos = -2
        max_size = len(cur_level)
        while pos < max_size and pos < self.max_length:
            temp = 0
            added_sum = 0
            while temp < 3:
                if (temp + pos) >= 0 and (temp + pos) < max_size:
                    added_sum += cur_level[temp + pos]
                temp += 1
            pos += 1
            next_level.append(added_sum)
        self.tri_layer.append(next_level)

    def __str__(self):
        result = ""
        for temp_list in self.tri_layer:
            result += " ".join(map(str, temp_list))
            result += "\n"
        return result

    @staticmethod
    def get_first_even(cur_list):
        selected_pos = -2
        for pos, entry in enumerate(cur_list):
            if entry % 2 == 0:
                selected_pos = pos
                break
        return selected_pos + 1

    def get_top_k_first_evens(self, k):
        start = len(self.tri_layer)
        even_pos_list = []
        while start < k:
            self.gen_next_level()
            start += 1

        for cur_list in self.tri_layer:
            even_pos_list.append(self.get_first_even(cur_list))
        return even_pos_list

    @staticmethod
    def static_generator(row_no):
        if row_no < 3:
            return -1
        if row_no % 2 == 1:
            return 2
        elif row_no % 4 == 0:
            return 3
        else:
            return 4

"""
check_count = 1000000
get_calc_list = TriNum().get_top_k_first_evens(check_count)
for index, pos in enumerate(get_calc_list):
    if pos != TriNum.static_genrator(index+1):
        print "Holy law has failed on line %d" % (index)
"""

test_case_count = int(raw_input())
while test_case_count > 0:
    print TriNum.static_generator(int(raw_input()))
    test_case_count -= 1
