import sys


"""
    Algorithm 
    Get all the stock price.
    Sort them in decreasing order of price
    If iterate over the stocks and keep selling the margin
"""

class StockPattern:

    def __init__(self, stocks):
        self.stocks_by_price = []
        self.stocks_by_date = []
        running_sum = 0;
        for day, price in enumerate(stocks):
            self.stocks_by_price.append((day, price))
            running_sum += price
            self.stocks_by_date.append(running_sum)
        self.stocks_by_price.sort(key = lambda x: x[1], reverse = True)
        self.last_sell_day = 0

    def profit_by_selling_on(self, day, price):
        if day <= self.last_sell_day:
            # Already sold all the stocks before
            # this date
            return 0
        
        prev_stock_cost = 0
        if self.last_sell_day != 0:
            # Already sold stocks before this
            prev_stock_cost = self.stocks_by_date[self.last_sell_day]
        
        current_stock_cost = 0
        if day != 0:
            current_stock_cost = self.stocks_by_date[day-1]
        
        stocks_sold = (day - self.last_sell_day) -1# Removing 1 for sell date        
        if self.last_sell_day == 0:
            stocks_sold = day

        self.last_sell_day = day

        return (stocks_sold*price) - (current_stock_cost - prev_stock_cost)

    def get_profit(self):
        profit = 0
        for (day, price) in self.stocks_by_price:
            gen_profit = self.profit_by_selling_on(day, price)
            if gen_profit > 0:
                profit += gen_profit
        return profit



if __name__ == "__main__":
    test_case_count = int(raw_input())
    while test_case_count > 0:
        raw_input() # wasting the read of stock count
        stocks = map(int, raw_input().split())
        print StockPattern(stocks).get_profit()
        test_case_count -= 1
