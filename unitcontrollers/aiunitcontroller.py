import random
from unitcontrollers.unitcontroller import UnitController


random.seed(1)


class AIUnitController(UnitController):
    """
    Creates an AIUnitController object. An AIUnitController object is a simple AI controller for a Unit that handles
    the interaction of a Unit, which includes movement and attacking actions.
    """
    def get_enemies(self):
        """
        Gets a list of Units on the opposing team(s).
        :return: Returns a list of Units on opposing team(s).
        """
        res = []
        for u in self.state.units:
            if u.team != self.unit.team:
                res.append(u)
        return res

    def distance(self, x, y, u2):
        """
        Calculates the distance between the given (x, y) and the position of u2.
        :param x: The x-position of the Unit belonging to this UnitController.
        :param y: The y-position of the Unit belonging to this UnitController.
        :param u2: The Unit u2.
        :return: Returns the distance between the x, y and the position of u2.
        """
        return abs(abs(x - u2.x) + abs(y - u2.y) - self.unit.range)

    def get_closest_enemy(self):
        """
        Gets the enemy closest to the Unit belonging to this UnitController.
        :return: The enemy closest to the Unit belonging to this UnitController.
        """
        closest_enemy, closest_distance = None, 99999
        for enemy in self.get_enemies():
            dist = self.distance(self.unit.x, self.unit.y, enemy)
            if dist < closest_distance:
                closest_distance, closest_enemy = dist, enemy
        return closest_enemy

    def possible_moves(self):
        """
        Creates a list of the possible movement actions the Unit belonging to this UnitController can make.
        :return: A list of all possible movement actions for the Unit belonging to this UnitController.
        """
        res = []
        for x in range(self.unit.x - self.unit.move, self.unit.x + self.unit.move + 1):
            diff = self.unit.move - abs(self.unit.x - x)
            for y in range(self.unit.y - diff, self.unit.y + diff + 1):
                if self.state.movement_allowed(self.unit, (x, y)):
                    res.append((x, y))
        return res

    def next_movement(self):
        """
        Decides the movement action of the Unit belonging to this
        UnitController based on the possible moves and its closest enemy.
        :return: A list of possible movement actions if any were found, None otherwise.
        """
        enemy = self.get_closest_enemy()
        moves = self.possible_moves()
        sorted_moves = list(sorted(moves, key=lambda m: self.distance(*m, enemy)))
        if sorted_moves:
            return sorted_moves[0]

    def next_attack(self):
        """
        Acts out an attack on the closest enemy Unit if an attack can be made on that Unit.
        :return: The enemy to be attacked if one is chosen, None otherwise.
        """
        enemy = self.get_closest_enemy()
        if self.state.attack_allowed(self.unit, enemy):
            return enemy
    
    def decide_order_weight(self):
        """
        Gives back a random order weight that decides the Unit order in a team.
        :return: A random order weight.
        """
        return random.random()
