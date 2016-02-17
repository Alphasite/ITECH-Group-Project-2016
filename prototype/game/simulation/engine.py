class State:
    def __init__(self):
        super().__init__()

        self.items = [

        ]


class Item:
    def __init__(self, price: int):
        super().__init__()

        self.price = price
        self.priceDelta = 0
        self.priceDeltaDelta = 5
