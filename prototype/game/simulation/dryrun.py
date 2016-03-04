from math import sin
from random import randint

from game.simulation.engine import Item, State

items = [
    Item("Bacon", 10.0, 50, 0.5, lambda t: (sin(t / 10.0) + 0.5) * 40)
]

items = {item.name: item for item in items}

state = State(items)

print(state)

for i in range(0, 50):
    state.tick()
    item = state.items["Bacon"]
    item.owned = max(0, item.owned + randint(10, 20) ** 1.5)
    print(state)


