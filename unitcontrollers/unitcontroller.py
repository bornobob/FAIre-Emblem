import abc

class UnitController(abc.ABC):
    """
    Base UnitController, classes that implement a UnitController must override
    at least the abstract methods.
    UnitControllers can be seen as strategies that control a unit. You could
    create multiple unit controllers and see which one works best, for example.
    """

    def __init__(self, unit, state):
        """
        The initializer for a unit controller must at least get the unit it
        controls, and the state of the game. This does not add the unit to the
        given state.
        """
        self.unit = unit
        self.state = state

    def reset_unit(self):
        """
        Resets the unit of the unit controller.
        """
        self.unit = self.unit.clone_original()

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

    def possible_moves(self):
        """
        Creates a list of the possible movement actions the Unit belonging to
        this UnitController can make.
        :return: A list of all possible movement actions for the Unit 
                    belonging to this UnitController.
        """
        res = []
        lower_x_range = self.unit.x - self.unit.move
        upper_x_range = self.unit.x + self.unit.move + 1
        for x in range(lower_x_range, upper_x_range):
            diff = self.unit.move - abs(self.unit.x - x)
            for y in range(self.unit.y - diff, self.unit.y + diff + 1):
                if self.state.movement_allowed(self.unit, (x, y)):
                    res.append((x, y))
        return res

    def seed_random(self, random_seed):
        """
        Seed the random instance of this unit controller. By default, this does
        nothing, override only if needed.
        :param random_seed: the random seed to set.
        """
        pass
