import sys
import math

inp_stream = open('test.txt', 'r');
test_case_count = int(inp_stream.readline());
while test_case_count > 0:
    polygon = list(inp_stream.readline().strip());
    polygon_size = len(polygon);
    iso_count = 0;
    print polygon_size;
    print int(math.ceil(polygon_size/3)+1);
    raw_input();
    for shift_amount in range (1, int(math.ceil(polygon_size/3)+1)):

        for start_node in range(0, polygon_size):
            if polygon[start_node] == polygon[(start_node+shift_amount)%polygon_size] and polygon[start_node] == polygon[(start_node-shift_amount)%polygon_size]:
                iso_count += 1;
            """
            print "Current polygon position startnode %d shhiftamount %d"%(start_node, shift_amount);
            print "polygon value " + polygon[start_node] + "-" + polygon[(start_node+shift_amount)%polygon_size] + "-" + polygon[(start_node-shift_amount)%polygon_size];
            raw_input();
            """
    print iso_count
    test_case_count -= 1
