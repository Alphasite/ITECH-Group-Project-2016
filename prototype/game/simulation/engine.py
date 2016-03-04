from collections import deque
from math import log

import math

from game.simulation.utility import clamp, average, trendline


def simulate(state):
    pass


class State:
    def __init__(self, items):
        self.items = items
        self.time = 0

    def tick(self):
        for item in self.items.values():
            item.update_price(self.time)

        self.time += 1

    def __str__(self, *args, **kwargs):
        items = []
        for item in self.items.values():
            items.append("{}: £{:,.2f}x{}".format(
                item.name,
                item.price,
                get_deque_tail(item.sales_per_quarter)
            ))

        return "Time: {} {}".format(self.time, "\t\n".join(items))


class Item:
    def __init__(self, name, price, sales, price_sensitivity, sales_function):
        self.name = name

        self.owned_per_quarter = deque(maxlen=12)

        self.prices_per_quarter = deque(maxlen=12)
        self.sales_per_quarter = deque(maxlen=12)
        self.price_sensitivity = price_sensitivity
        self.sales_function = sales_function

        self.sales_per_quarter.append(sales)
        self.prices_per_quarter.append(price)

        self.owned = 0

    def update_price(self, number_of_ticks):
        self.owned_per_quarter.append(self.owned)

        price = self.price
        sales = max(0, self.sales_function(number_of_ticks)) + (self.owned - get_deque_tail(self.owned_per_quarter))

        sales_delta = self.average_sales - sales
        sales_delta_percentage = 1 / (1 + pow(math.e, clamp(sales_delta / self.average_sales, -1, 1))) - 0.5

        price_delta = self.price_sensitivity * sales_delta_percentage * price

        self.sales_per_quarter.append(int(sales))
        self.prices_per_quarter.append(price + price_delta)

    @property
    def price(self):
        return get_deque_tail(self.prices_per_quarter)

    @property
    def average_price(self):
        return average(self.prices_per_quarter)

    @property
    def average_sales(self):
        return average(self.sales_per_quarter)

    @property
    def sales_trendline(self):
        return trendline(self.sales_per_quarter)

    @property
    def prices_trendline(self):
        return trendline(self.prices_per_quarter)


def get_deque_tail(deque):
    return deque[len(deque) - 1]
