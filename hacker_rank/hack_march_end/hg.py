import sys

#inp_stream = sys.stdin;
inp_stream = open('input02.txt', 'r');
test_case_count = int(inp_stream.readline());
base_count  = 1
while test_case_count > 0:
    grid_size = int(inp_stream.readline());
    grid = []
    grid.append(inp_stream.readline().strip());
    grid.append(inp_stream.readline().strip());
    count = 0;
    black_count = 0;
    top_black = False;
    bot_black = False;
    out_put_set_flag = False;
    if base_count == 36:
        print grid;
    while count < grid_size:
        if base_count == 36:
            print "+++++++++++++++++++++++++++++++++++++"
            print grid[0][count];
            print grid[1][count];
            print top_black;
            print bot_black;
            print black_count;
            raw_input();
        if grid[0][count] == '1':
            top_black = True;
            black_count += 1;
            if bot_black == True:
                # Here we are splitting the grid so check crap
                if black_count % 2 == 0:
                    out_put_set_flag = True;
                    print "NO"
                    break;
                black_count = 0;
                top_black = False;
        else:
            top_black = False;
        if grid[1][count] == '1':
            bot_black = True;
            black_count += 1;
            if top_black == True:
                # Here we are splitting the grid so check crap
                if black_count % 2 == 1:
                    out_put_set_flag = True;
                    print "NO"
                    break;
                bot_black = False;
                black_count = 0;
        else:
            bot_black = False;
        count += 1;
    if not out_put_set_flag:
        print "Output From here";
        if black_count % 2 == 1:
            print "NO";
        else:
            print "YES";

    test_case_count -= 1
    base_count += 1;
