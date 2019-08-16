class State:
    def __init__(self, inflow, volume, height, pressure, outflow):
        self.quantities = [inflow, volume, height, pressure, outflow]
        # eg. entity container has 5 quantities: volume, height, pressure

class Quantity:
    def __init__(self, name, quantity_space, quantity, derivative, affects, corresponds):
        self.name = name
        self.quantity_space = quantity_space
        self.quantity = quantity
        self.derivative = derivative
        self.affects = affects
        self.corresponds = corresponds

