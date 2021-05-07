class Unit:
    """
    Represents a Unit placed in the world.
    """
    
    id = 1

    def __init__(self, location, stats, team, name=''):
        """
        Creates a Unit object. A Unit has statistics that influence its
        movement on the map, its survivability and the damage it does to enemy
        Units. It also has a team and a name.
        """
        self.team = team
        self.max_hp = stats['hp']
        self.hp = stats['hp']
        self.atk = stats['atk']
        self.range = stats['range']
        self.move = stats['move']
        self.x = location[0]
        self.y = location[1]
        self.name = name
        self.id = Unit.id
        Unit.id += 1

    def movement_allowed(self, new_pos):
        """
        Checks whether movement to new position is allowed.
        :param new_pos: The position unit wants to move to.
        :return: True if the new position is within movement range of unit,
                 False otherwise.
        """
        x, y = new_pos
        return abs(x - self.x) + abs(y - self.y) <= self.move

    def attack_allowed(self, enemy_unit):
        """
        Checks if unit can make an attack against a unit on another team.
        :param enemy_unit: The enemy unit that is to be attacked.
        :return: True if the unit is at attack range, False otherwise.
        """
        x, y = enemy_unit.x, enemy_unit.y
        return (abs(x - self.x) + abs(y - self.y) == self.range
                and self.team != enemy_unit.team)

    def is_dead(self):
        """
        Checks whether a unit is dead, meaning it has 0 (or less) hit points.
        :return: True when the unit has 0 or less hit points.
        """
        return self.hp <= 0

    def __str__(self):
        """
        Creates a string for the Unit object including its team, name, position
        and current hit points.
        :return: An string object for the Unit class.
        """
        return f'<{self.team}\'s {self.name},' + \
               f' ({self.x}, {self.y}) {self.hp} hp>'
