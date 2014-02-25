import sys

number_list = [];
non_zero_num  = 1;
zero_count = 0;

inp_stream = sys.stdin
entry_count = int(inp_stream.readline());
count = entry_count;
while count > 0:
    number = int(inp_stream.readline());
    number_list.append(number);
    if number == 0:
        zero_count += 1;
        if zero_count > 1:
            break;
    else:
        non_zero_num *= number;
    count -= 1;

count = 0;
if zero_count > 1:
    while count < entry_count:
        print 0;
        count += 1;

elif zero_count == 1:
    while count < entry_count:
        num = number_list[count];
        if num == 0:
            print non_zero_num;
        else:
            print 0;
        count += 1;
else:
    while count < entry_count:
         num = number_list[count];
         print non_zero_num/num;
         count += 1;
