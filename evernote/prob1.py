import sys

current_head = 0;
current_tail = 0;
circ_buffer = [];
buffer_size = 0;
entry_count = 0;



def add_to_circ_buffer(word):
    global circ_buffer, current_head, current_tail, buffer_size, entry_count;
    if entry_count == buffer_size:
        current_head = (current_head + 1)%buffer_size;
    circ_buffer[current_tail] = word;
    current_tail += 1;
    current_tail = current_tail % buffer_size;
    entry_count = min(entry_count+1, buffer_size);

def remove_n_elements(n):
    global circ_buffer, current_head, current_tail, buffer_size, entry_count;
    while n >  0:
        if current_head == current_tail and entry_count != buffer_size:
            break;
        circ_buffer[current_head] = None;
        current_head = (current_head + 1) % buffer_size;
        n -= 1
        entry_count -= 1;

def list_buffer():
    global circ_buffer, current_head, current_tail, buffer_size, entry_count;
    if entry_count == 0:
        return;
    count = 1;
    read_head = current_head;
    print circ_buffer[current_head];
    while count < entry_count:
        read_head = (read_head+1)%buffer_size;
        print circ_buffer[read_head];
        count += 1;

def append_next_n_words(n, stream):
    while n > 0:
        word = (stream.readline());
        word = word.strip();
        add_to_circ_buffer(word);
        n -= 1;
    return;


inp_stream = sys.stdin;
buffer_size = int(inp_stream.readline());
circ_buffer = [None]*buffer_size;

while True:
    line = inp_stream.readline();
    line = line.strip();
    query = line[0];
    if query == 'A':
        append_next_n_words(int(line.split()[-1]), inp_stream);
    elif query == "R":
        remove_n_elements(int(line.split()[-1]));
    elif query == "L":
        list_buffer();
    else:
        break;
