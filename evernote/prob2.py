import sys
selected_list = [float('-inf')]*4;
get_top = 4;

def is_better_number(term):
    global selected_list;
    if term > selected_list[-1]:
        return True;
    return False;

def add_number(term):
    global selected_list, get_top;
    for index in xrange(0, get_top):
        if selected_list[index] < term:
            selected_list.insert(index, term);
            break;
    selected_list = selected_list[:-1];
    return ;

inp_stream = sys.stdin;
count = int(inp_stream.readline());
while count > 0:
    term = int(inp_stream.readline());
    if is_better_number(term):
        add_number(term);
    count -= 1;

for ele in selected_list:
    print ele
