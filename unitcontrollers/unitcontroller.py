import abc

class UnitController(abc.ABC):
    def __init__(self, unit, state):
        self.unit = unit
        self.state = state
        self.state.add_unit(unit)

    @abc.abstractmethod
    def next_movement(self):
        """
        Function that gives back either a tuple being the new position,
        or False if the unit does not want to make some move.
        """
        ...

    @abc.abstractmethod 
    def next_attack(self):
        """
        Function that gives back an enemy unit to attack, or False if the
        unit does not want to attack an enemy unit.
        """
        ...

    @abc.abstractmethod
    def decide_order_weight(self):
        """
        Function that gives the weight which decides the ordering of units
        in the next turn.
        """
        ...
