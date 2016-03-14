import math
from collections import deque

from game.simulation.utility import clamp, average, trendline


def simulate(state):
    pass


ERROR_CORRECTION = 0.000000001


class State:
    def __init__(self, items):
        self.items = items
        self.time = 0

    def tick(self):
        for item in self.items.values():
            item.update_price(self.time)

        self.time += 1

    def __str__(self, *args, **kwargs):
        items = [str(item) for item in self.items.values()]

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
        self.owned_per_quarter.append(self.owned)

    def update_price(self, number_of_ticks):
        """The sales curve here models inelastic demand
        :param number_of_ticks: The current time in the simulation.
        :type number_of_ticks: int
        """

        price = self.price
        sales = max(0, self.sales_function(number_of_ticks)) + (self.owned - self.owned_per_quarter[-1])

        self.owned_per_quarter.append(self.owned)

        sales_delta = self.average_sales - sales
        sales_percentage_of_normal = sales_delta / self.average_sales if self.average_sales != 0 else 1
        sales_exponent = clamp(sales_percentage_of_normal, -1, 1)

        # this uses a sigmoid curve to bound the upper and lower limits of the natural swing,
        # and make price_sensitivity useful.
        # Error correction is to account for the division, to avoid 1/(1 + -1)
        sales_delta_percentage = 1 / (1 + pow(math.e, sales_exponent) + ERROR_CORRECTION) - 0.5

        price_delta = self.price_sensitivity * sales_delta_percentage * price

        self.sales_per_quarter.append(int(sales))
        self.prices_per_quarter.append(price + price_delta)

    @property
    def price(self):
        return self.prices_per_quarter[-1]

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

    def __str__(self, *args, **kwargs):
        return "{} || Sales: £{:4,.2f}x{} Average: £{:4,.2f}x{:4,.2f}".format(
                self.name,
                self.price,
                self.sales_per_quarter[-1],
                self.average_price,
                self.average_sales,
        )
