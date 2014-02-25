import os
import math
import sys
from random import *

def distance_between_points(x1, y1, x2, y2):
    return pow(pow((x1-x2), 2) + pow((y1-y2), 2), 0.5);



class keep_top:
    def __init__(self, k):
        print "staying at init";
        self.k = k;
        self.__list__ = [{'distance':float('inf'), 'x': None, 'y':None}];
        return;

    def max_val(self):
        if len(self.__list__) == self.k:
            return self.__list__[-1]['distance'];
        else:
            return float('inf');

    def add_close_node(self, x, y, dist):
        # max_case is dealt as a special case
        # Only in case if max entry do we add in between
        for ele_count in xrange(0, len(self.__list__)):
            if self.__list__[ele_count]['distance']  > dist:
                # This is were we insert the node
                # Resolve conflict in this case
                if ele_count == self.k - 1 and abs(self.__list__[ele_count]['distance'] - dist) < 0.001:
                    # This is the last entry
                    # Keep the smaller one with topics
                    return;
                else:
                    self.__list__.insert(ele_count, {'distance': dist, 'x': x, 'y': y});
                    break;
        
        # If list size grows beyond boundary remove 
        while len(self.__list__) > self.k:
            del self.__list__[-1];
        return;

    def __str__(self):
        result_str = "";
        for element in self.__list__:
            result_str += str(element['x']) + "," + str(element['y'])  + ' ---- ';
        return result_str;

MAX = 100000;
MIN = -100000;
COUNT = 100000;
dist = float('inf');
TEST_FILE = 'test_outfile.out';
mylist = keep_top(5);

q_x = randint(MIN, MAX);
q_y = randint(MIN, MAX);

result_list = [];
fo = open(TEST_FILE, 'w');

while COUNT > 0:
    nx = randint(MIN, MAX);
    ny = randint(MIN, MAX);
    current_dist = distance_between_points(q_x, q_y, nx, ny);
    if current_dist < mylist.max_val():
        #result_list = [(nx, ny)];
        mylist.add_close_node(nx, ny, current_dist);
    fo.write("%d\t%d\n"%(nx, ny));
    COUNT -= 1;
fo.write("%d\t%d"%(q_x, q_y));
fo.close();
print mylist;
