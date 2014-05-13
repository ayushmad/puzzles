import os

time_required_till = [];

def min_time_till(start_time):
    global time_required_till
    if start_time == 0:
        return 0
    else:
        current_min_value = float('inf');
        for block_data in time_required_till:
            if block_data[0] < start_time and block_data[1] >= start_time:
                if block_data[2] < current_min_value:
                    current_min_value = block_data[2];
        return current_min_value;


def time_ending(blocks, total_byte_size, latency, byte_rate):
    global time_required_till;
    start_sorted_blocks = list(blocks)
    start_sorted_blocks.sort()
    for block in start_sorted_blocks:
        # Error check here if the block is starting on time
        till_now_time = min_time_till(block[0])
        current_time = till_now_time + (((block[1]-block[0])/byte_rate) + (latency*2));
        print block;
        print current_time;
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++"
        # Now we need to push into the global table
        time_required_till.append((block[0], block[1], current_time));
    return min_time_till(total_byte_size);



if __name__ == "__main__":
    byte_size = int(raw_input());
    latency = int(raw_input());
    bandwidth = int(raw_input());
    chunk_count = int(raw_input());
    blocks = [];
    while chunk_count > 0:
        blocks.append(map(int, raw_input().strip().split(',')))
        chunk_count -= 1
    print time_ending(blocks, byte_size, latency, bandwidth);
