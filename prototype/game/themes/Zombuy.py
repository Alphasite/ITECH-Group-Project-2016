# -*- coding: utf-8 -*-

from game.simulation.engine import State, Item, SalesCalculation


class Simulation:
    def __init__(self):
        pass

    name = "Zombuy"
    description_short = "asfsdfads"
    description_long = "Asdadasdadasdasdasdasdasd"
    rules = [
        "asdasdas",
        "sadasffdg",
        "sdfsfdsfgsfd"
    ]

    small_icon_path = "themes/zombuy/images/icon-small.png"
    small_banner_path = "themes/zombuy/images/banner-small.png"

    time_limit = 15

    def progress_function(self, state):
        return state.time / self.time_limit

    def progress_label_function(self, state):
        return "{} months remaining".format(self.time_limit - state.time)

    @property
    def simulation(self):

        # Python cannot pickle functions.
        return State(self.items, 500, self)

    @property
    def items(self):
        return [
            Item(
                "BRAINZ", 25, 100, 0.8, SalesCalculation(3, 200),
                description="Its not just a brain; its a farm reared, ginger haired M&S brain."
            ),
            Item(
                "Genuine Fake Chinese Brainz", 4, 500, 0.2, SalesCalculation(3, 1000, -500),
                description="º¤ø,¸¸,ø¤ºº¤ø,¸¸,¸,øºø,¸,ø¤ºº¤ø,¸¸,ø¤HIGHLY RECOMMENDED º."
            ),
            Item(
                "ARMZZZ", 8, 20, 0.2, SalesCalculation(5, 24, -4),
                description="For when your own just wont stay on..."
            ),
            Item(
                "Stapler", 20, 10, 0.1, SalesCalculation(5, 12, -2),
                description="See 'ARMZZZ'."
            ),
            Item(
                "Dr Zomboids Zomball Cure!", 50, 20, 0.2, SalesCalculation(6, 20, 10),
                description="Got a case of the humans? Make it disappear with just this one easy pill!"
            ),
            Item(
                "Estus Flask", 100, 1, 0.8, SalesCalculation(10, 2),
                description="A green glass bottle of unknown make. But that is of little concern, "
                            "for any Undead knows the value of these precious flasks."
            ),
            Item(
                "Dr Zomboids Stay Upper (10 pack)", 5, 100, 0.1, SalesCalculation(2, 50),
                description="The little blue pill who could..."
            ),
        ]

