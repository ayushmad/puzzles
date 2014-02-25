import sys
import bisect




def count_insort_shifts(numbers):
    sorted_sublist = [];
    count  = 0;
    sub_list_len = 0;
    for index in range(0, len(numbers)):
        num = int(numbers[index]);
        pos =  bisect.bisect(sorted_sublist, num);
        sorted_sublist.insert(pos, num);
        count += (sub_list_len - pos);
        sub_list_len += 1;
    return count;

if __name__ == "__main__":
    #inp_stream = sys.stdin;
    inp_stream = open('test.txt', 'r');
    test_case_count = int(inp_stream.readline());
    while test_case_count > 0:
        number_count = int(inp_stream.readline());
        numbers = inp_stream.readline().strip().split();
        print count_insort_shifts(numbers);
        test_case_count -= 1;
