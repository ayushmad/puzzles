import sys
import math
from bisect import insort_left

def get_kth_smallest_number(selection_list, rank):
    selected_rank_list = [float('inf')];
    ranked_count = 1;
    for entry in selection_list:
        if entry < selected_rank_list[-1]:
            insort_left(selected_rank_list, entry);
            ranked_count += 1;
            if ranked_count > rank:
                selected_rank_list = selected_rank_list[:-1];
    return selected_rank_list[-1];




def answer_query(entries, start_index, end_index, rank):
    selection_list = entries[start_index-1: end_index];
    sub_list_len = end_index - start_index + 1;
    sub_list_time = int(math.log(sub_list_len, 2));
    if sub_list_time > rank:
        return get_kth_smallest_number(selection_list, rank);
    # elif sub_list_time > (sub_list_len - rank):
    #    return get_kth_largest_number(selection_list, sub_list_len - rank);
    else:
        selection_list.sort();
        return selection_list[rank-1];

def update_entry(entries, index, books):
    entries[index-1] = books;
    return entries;

def process_test_case(inp_stream):
    global  entries;
    number_of_books = inp_stream.readline();
    entries = map(int, inp_stream.readline().split());
    query_count  = int(inp_stream.readline());
    while query_count > 0:
        query = inp_stream.readline();
        if query[0] == '0':
            (query_id, start_index, end_index, rank) = map(int, query.split());
            #print query.strip();
            #print entries
            print answer_query(entries, start_index, end_index, rank);
            #raw_input();
        else:
            (query_id, index, new_book_count) = map(int, query.split());
            #print query.strip();
            #print entries;
            #raw_input();
            entries  = update_entry(entries, index, new_book_count);
        query_count -= 1;


inp_stream = sys.stdin;
test_case_count = int(inp_stream.readline());
while test_case_count > 0:
    process_test_case(inp_stream);
    test_case_count -= 1;
