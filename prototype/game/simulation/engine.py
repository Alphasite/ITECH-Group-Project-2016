from collections import deque, defaultdict
from math import log

from game.simulation.utility import clamp, average, trendline


class State:
    def __init__(self, items):
        super().__init__()

        self.items = items
        self.time = 0
        self.purchases = defaultdict(default_factory=lambda: 0)

    def tick(self):
        for item in self.items:
            item.update_price(self.time, self.purchases[item.name])

        self.purchases = {}


class Item:
    def __init__(self, name, price, sales, price_sensitivity, sales_function):
        super().__init__()

        self.name = name

        self.prices = deque(maxlen=12)
        self.sales = deque(maxlen=12)
        self.price_sensitivity = price_sensitivity
        self.sales_function = sales_function

        self.sales.append(sales)
        self.prices.append(price)

    def update_price(self, number_of_ticks, user_sales):
        price = self.prices[-1]
        sales = self.sales_function(number_of_ticks) + user_sales

        sales_delta = sales - self.average_sales
        sales_delta_percentage = log(clamp(sales_delta / self.average_sales, -1, 1) + 1, 10)

        price_delta = self.price_sensitivity * sales_delta_percentage * price

        self.prices.append(price + price_delta)

    @property
    def average_price(self):
        return average(self.prices)

    @property
    def average_sales(self):
        return average(self.sales)

    @property
    def sales_trendline(self):
        return trendline(self.sales)

    @property
    def prices_trendline(self):
        return trendline(self.prices)
