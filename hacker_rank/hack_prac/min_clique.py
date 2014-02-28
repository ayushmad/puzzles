import sys
import math

def max_edge(nodes, clique_size):
    return ((clique_size-2)*pow(nodes, 2))/(2*(clique_size-1));


def find_min_clique(nodes, edges):
    max_clique_size = nodes;
    min_clique_size = 2;
    '''
    print "-----------------Starting a test case------------------";
    print nodes;
    print edges;
    '''
    while max_clique_size - min_clique_size > 1:
        mid_clique_size = (min_clique_size + max_clique_size)/2;
        allowed_edges = max_edge(nodes, mid_clique_size);
        '''
        print "Nodes %d" %(nodes);
        print "Edges %d" %(edges);
        print "Min CLique size %d" %(min_clique_size);
        print "Max Clique size %d" %(max_clique_size);
        print "Selceted Clique size %d" %(mid_clique_size);
        print "Allowed edges %d" %(allowed_edges);
        raw_input();
        '''
        if edges <= allowed_edges:
            max_clique_size = mid_clique_size;
        else:
            min_clique_size = mid_clique_size+1;
    return max_clique_size;


test = [1,2,3]

if __name__ == "__main__":
    # inp_stream = open('test.txt', 'r');
    inp_stream = sys.stdin;
    test_case_count = int(inp_stream.readline());
    while test_case_count > 0:
        (nodes, edges) = map(int, inp_stream.readline().split());
        print find_min_clique(nodes, edges);
        test_case_count -= 1;
