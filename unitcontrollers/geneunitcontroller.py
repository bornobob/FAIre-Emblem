import random
from unitcontrollers.unitcontroller import UnitController


class GeneUnitController(UnitController):
    """
    
    """
    def __init__(self, unit, state, genes):
        super().__init__(unit, state)
        self.genes = genes
        self.initiative = genes['initiative']  # Turn order 
        self.greed = genes['greed']  # Focus low hp over high attack
        self.focus = genes['focus']  # Is more likely to target enemy unit that is in range

    def get_enemies(self):
        """
        Gets a list of Units on the opposing team(s).
        :return: Returns a list of Units on opposing team(s).
        """
        for u in self.state.units:
            if u.team != self.unit.team:
                res.append(u)
        return res
        return [u for u in self.state.units if u.team != self.unit.team]
        

    def distance(self, x, y, u2):
        """
        Calculates the distance between the given (x, y) and the position of u2.
        :param x: The x-position of the Unit belonging to this UnitController.
        :param y: The y-position of the Unit belonging to this UnitController.
        :param u2: The Unit u2.
        :return: Returns the distance between the x, y and the position of u2.
        """
        return abs(abs(x - u2.x) + abs(y - u2.y) - self.unit.range)

    def within_attack_distance(self, x, y, u2):
        """
        Calculates whether unit u2 is able to attack position (x, y)
        :param x: The x-position of the Unit belonging to this UnitController.
        :param y: The y-position of the Unit belonging to this UnitController.
        :param u2: The Unit u2.
        :return: True if the position can be attacked by unit u2, False otherwise.
        """
        return abs(abs(x - u2.x) + abs(y - u2.y)) - u2.range <= 0

    def max_expected_damage(self, x, y):
        """
        Calculates whether unit u2 is able to attack position (x, y)
        :param x: The x-position of the Unit belonging to this UnitController.
        :param y: The y-position of the Unit belonging to this UnitController.
        :return: the sum total of damage that could be dealt to this unit if the unit chooses to move to position (x, y).
        """
        return sum([e.atk for e in self.get_enemies() if self.within_attack_distance(x, y, e)])

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

    def get_lowest_enemy(self):
        """
        Gets the enemy with the lowest hit points.
        :return: The enemy with lowest hit points on the field if it exists, None otherwise.
        """
        lowest_enemy = list(sorted(self.get_enemies(), key=lambda h: h.hp))
        if lowest_enemy:
            return lowest_enemy[0]

    def get_highest_hp(self):
        return max(e.hp for e in self.get_enemies())

    def get_highest_atk(self):
        return max(e.atk for e in self.get_enemies())

    def get_most_appealing_enemy(self):
        """
        This function calculates which enemy seems best to attack based in this unit's genes.
        If the unit has more focus, it will prefer an enemy within attack range. 
        If the unit has more greed, it will prefer low hp targets.
        :return: The enemy that looks most appealing to attack to this unit.
        """
        inv_scale_hp = lambda u: 1 - (u.hp / self.get_highest_hp())
        scale_atk = lambda u: u.atk / self.get_highest_atk()
        focus_modifier = lambda h: (self.distance(self.unit.x, self.unit.y, h) < self.unit.move) * self.focus
        enemies = list(sorted(self.get_enemies(), key=lambda h: -(inv_scale_hp(h) * self.greed + scale_atk(h) * (1 - self.greed) + focus_modifier(h))))
        if enemies:
            return enemies[0]

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
        UnitController based on the possible moves and the most appealing enemy.
        :return: A list of possible movement actions if any were found, None otherwise.
        """
        enemy = self.get_most_appealing_enemy()
        moves = self.possible_moves()
        sorted_moves = list(sorted(moves, key=lambda m: self.distance(*m, enemy)))
        if sorted_moves:
            return sorted_moves[0]

    def next_attack(self):
        """
        Acts out an attack on the lowest enemy Unit if an attack can be made on that Unit.
        :return: The enemy to be attacked if one is chosen, None otherwise.
        """
        attacks = filter(lambda x: self.state.attack_allowed(self.unit, x), self.get_enemies())
        sorted_attacks = list(sorted(attacks, key=lambda a: a.hp))
        if sorted_attacks:
            return sorted_attacks[0]
    
    def decide_order_weight(self):
        """
        Gives back an order weight that decides the Unit order in a team.
        :return: A random order weight.
        """
        return 1 - self.initiative
