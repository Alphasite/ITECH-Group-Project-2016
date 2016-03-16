from math import sin
from random import randint

from game.simulation.engine import Item, State

items1 = [
    Item("Bacon", 10.0, 50, 0.5, lambda t: (sin(t / 10.0) + 0.5) * 40)
]

items2 = [
    Item("Bacon", 10.0, 50, 0.5, lambda t: (sin(t / 10.0) + 0.5) * 40)
]

items1 = {item.name: item for item in items1}
items2 = {item.name: item for item in items2}

state1 = State(items1)
state2 = State(items2)

print(state1)
print(state2)

for i in range(0, 100):
    state1.tick()
    state2.tick()

    item = state1.items["Bacon"]
    item.owned = max(0, item.owned + randint(10, 20) ** 2)

    print(state1)
    print(state2)


