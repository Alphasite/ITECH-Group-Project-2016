# -*- coding: utf-8 -*-

import math
from collections import deque

import datetime

from game.simulation.utility import clamp, average, trendline

VERSION = 0

ERROR_CORRECTION = 0.000000001


class State:
    def __init__(self, items, starting_balance, theme):
        self.items = items
        self.time = 0
        self.events = theme.events
        self.balance = starting_balance
        self.theme = theme
        self.last_played = datetime.datetime.now()

        for item in items:
            item.state = self


    def tick(self):
        for event in self.current_events:
            event.apply(state=self)

        for item in self.items:
            self.balance -= item.update_price(self.time)

        self.time += 1

        self.last_played = datetime.datetime.now()

    @property
    def progress(self):
        return self.theme.progress_function(self)

    @property
    def remaining_label(self):
        return self.theme.progress_label_function(self)

    @property
    def past_events(self):
        past_events = []
        for event in self.events:
            if event.end_time < self.time:
                past_events.append(event)

        past_events.sort(key=lambda e: e.end_time)

        return past_events

    @property
    def current_events(self):
        active_events = []
        for event in self.events:
            if event.start_time <= self.time <= event.end_time:
                active_events.append(event)

        active_events.sort(key=lambda e: e.end_time)

        return active_events

    @property
    def future_events(self):
        future_events = []
        for event in self.events:
            if self.time < event.start_time:
                future_events.append(event)

        future_events.sort(key=lambda e: e.start_time)

        return future_events

    @property
    def score(self):
        return self.balance + sum([item.total_spent_on_inventory for item in self.items])

    @property
    def item_graphs(self):
        item_graphs = []

        for item in self.items:
            lower_bound = self.time
            upper_bound = self.time + len(item.prices_per_quarter)

            graph_data = {
                "x": list(range(lower_bound, upper_bound)) + [upper_bound + 3],
                "y": list(item.prices_per_quarter) + [item.prices_trendline * 3 + item.current_price]
            }

            item_graphs.append(graph_data)

        return item_graphs

    def __str__(self, *args, **kwargs):
        items = [str(item) for item in self.items.values()]

        return "Time: {} {}".format(self.time, "\t\n".join(items))


class Item:
    def __init__(self, name, price, sales, price_sensitivity, sales_function, description):
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

        self.description = description

        self.total_spent_on_inventory = 0

        self.state = None

        self.price_delta_to_apply = 0

    def update_price(self, number_of_ticks):
        """The sales curve here models inelastic demand
        :param number_of_ticks: The current time in the simulation.
        :type number_of_ticks: int
        """

        # This needs to stay stable, through the calculation.
        current_price = self.current_price
        owned_delta = self.owned - self.owned_per_quarter[-1]
        balance_delta = owned_delta * current_price

        self.total_spent_on_inventory += balance_delta

        sales = int(max(0, self.sales_function.calculate(number_of_ticks))) + owned_delta

        self.owned_per_quarter.append(self.owned)

        sales_delta = self.average_sales - sales
        sales_percentage_of_normal = sales_delta / self.average_sales if self.average_sales != 0 else 1
        sales_exponent = clamp(sales_percentage_of_normal, -1, 1)

        # this uses a sigmoid curve to bound the upper and lower limits of the natural swing,
        # and make price_sensitivity useful.
        # Error correction is to account for the division, to avoid 1/(1 + -1)
        sales_delta_percentage = 1 / (1 + pow(math.e, sales_exponent) + ERROR_CORRECTION) - 0.5

        price_delta = self.price_sensitivity * sales_delta_percentage * current_price * self.price_delta_to_apply

        self.sales_per_quarter.append(int(sales))
        self.prices_per_quarter.append(current_price + price_delta)

        self.price_delta_to_apply = 0

        return balance_delta

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

    @property
    def number_owned(self):
        return self.owned_per_quarter[-1]

    @property
    def current_price(self):
        return self.prices_per_quarter[-1]

    @property
    def average_purchase_price(self):
        return self.total_spent_on_inventory / self.number_owned if self.number_owned != 0 else 0

    @property
    def number_purchasable(self):
        return int(self.state.balance / self.current_price)

    def __str__(self, *args, **kwargs):
        return "{} || Sales: £{:4,.2f}x{} Average: £{:4,.2f}x{:4,.2f}".format(
                self.name,
                self.current_price,
                self.sales_per_quarter[-1],
                self.average_price,
                self.average_sales,
        )


class SalesCalculation:
    def __init__(self, cycle_period, amplitude, offset_from_zero=0.0):
        self.cycle_period = cycle_period
        self.amplitude = amplitude
        self.offset_from_zero = offset_from_zero

    def calculate(self, t):
        return (math.sin(t / self.cycle_period) + 0.5) * (self.amplitude / 2.0) + self.offset_from_zero


class Event():
    def __init__(self,start_time,end_time,name,description,effect,effects):
        self.start_time = start_time
        self.end_time = end_time
        self.name = name
        self.description = description
        self.effect = effect
        self.effects = effects

        # not sure if this is the best way to do this,
        # but I was not sure how to differentiate between the
        # event affecting the buy price vs the sell price


    def apply(self, state):
        #mutate the state, namely change the price according the multiplier in the event.
        for item in state.items:
            if item.name == self.effects:
                item.price_delta_to_apply = self.effect

        return self


