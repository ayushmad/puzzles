import sys

inp_stream = sys.stdin;
test_case_count = int(inp_stream.readline());
while test_case_count > 0:
    stock_count = int(inp_stream.readline().strip());
    stock_prices = map(int, inp_stream.readline().strip().split());
    profit = [0 for i in range(stock_count)];
    buy_cost = [0 for j in range(stock_count)];
    buy_cost[0] = stock_prices[0];
    for pos in range(1, stock_count):
        cur_stock_cost = stock_prices[pos];
        max_profit = 0;
        for buy_from in range(pos-1):
            cur_profit =  profit[buy_from] + (pos - buy_from)*cur_stock_cost - buy_cost[buy_from];
            if cur_profit > max_profit:
                max_profit = cur_profit;
        profit[pos] = max_profit;
        for cur_index in range(pos):
            buy_cost[cur_index] = buy_cost[cur_index] + cur_stock_cost;
    print max(profit); 
    test_case_count -= 1
