import os
import random
import sys


WINDOW_MAX = 2000;
HEIGHT_MAX = 2000;
SCORE_MAX = 100;
WINDOW_SELECTED = 0;
HEIGHT_SELECTED = 0;
TIME_LINE_SELECTED = random.randint(0, 100000000);
ENTRY_COUNT_MAX = 10000;
# random.randint(0, 10000);



def enter_height_width(stream):
    global HEIGHT_SELECTED, WINDOW_SELECTED;
    HEIGHT_SELECTED = random.randint(100, HEIGHT_MAX);
    WINDOW_SELECTED = random.randint(0, WINDOW_MAX);
    stream.write("%d %d %d\n"%(ENTRY_COUNT_MAX,
                             WINDOW_SELECTED,
                             HEIGHT_SELECTED));

def write_story(stream, timer):
    global HEIGHT_SELECTED, HEIGHT_MAX, SCORE_MAX
    #print HEIGHT_SELECTED;
    #raw_input();
    score_selected = random.randint(1, SCORE_MAX);
    prob = random.random();
    height = 0;
    if prob < 0.4:
        height = random.randint(1, HEIGHT_SELECTED/8);
    elif prob < 0.8:
        height = random.randint(1, HEIGHT_SELECTED/4);
    elif prob < 0.95:
        height = random.randint(1, HEIGHT_SELECTED/2);
    else:
        height = random.randint(1, HEIGHT_MAX);
    stream.write('S %d %d %d\n'%(timer,
                               score_selected,
                               height));
    return;

def refresh(stream, timer):
    stream.write("R %d\n"%(timer));
    return;

entry_count = 0;
timer = random.randint(0, 20);
stream = open(sys.argv[1], "w");
enter_height_width(stream);
write_story(stream, timer);
timer += 1;
entry_count += 1;
while entry_count < ENTRY_COUNT_MAX:
    prob = random.random();
    if prob < 0.6:
        write_story(stream, timer);
        entry_count += 1;
        timer += 1;
    elif prob < 0.8:
        refresh(stream, timer);
        entry_count += 1;
        timer += 1;
    else:
        entry_count += 1;
        timer += random.randint(0, 6);



