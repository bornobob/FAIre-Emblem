from collections import defaultdict


class State:
    """
    Creates a State object.
    """
    def __init__(self, board_dimensions):
        """
        Initializes a State object. Sets the dimensions of the playing board,
        creates a Unit list and a set of Unit positions.
        :param board_dimensions: The dimensions of the playing board.
        """
        self.board_dimensions = board_dimensions
        self.units = []
        self.unit_positions = set()
        self.original_units = []
        self.damage_done = defaultdict(int)

    def add_unit(self, unit):
        """
        Adds unit to the Unit list if the position of unit is not already used.
        :param unit: The Unit to add to the board.
        """
        assert (unit.x, unit.y) not in self.unit_positions
        assert 0 <= unit.x < self.board_dimensions[0]
        assert 0 <= unit.y < self.board_dimensions[1]
        self.units.append(unit)
        self.unit_positions.add((unit.x, unit.y))

    def simulate_move(self, unit, new_pos):
        """
        Simulates a move on the playing board by removing unit from its
        old position and moving it to its new (valid) position.
        :param unit: The Unit that wants to move.
        :param new_pos: The new position unit wants to move to.
        """
        assert self.movement_allowed(unit, new_pos)
        self.unit_positions.remove((unit.x, unit.y))
        self.unit_positions.add(new_pos)
        unit.x, unit.y = new_pos

    def movement_allowed(self, unit, new_pos):
        """
        Checks whether unit is valid and can move to the new position requested
        (within board dimensions, within the movement range of Unit and position not taken).
        :param unit: The Unit that wants to move.
        :param new_pos: The new position Unit wants to move to.
        :return: True if the Unit can move to the new position, False otherwise.
        """
        return (unit in self.units
                and 0 <= new_pos[0] < self.board_dimensions[0]
                and 0 <= new_pos[1] < self.board_dimensions[1]
                and (new_pos == (unit.x, unit.y) or new_pos not in self.unit_positions)
                and unit.movement_allowed(new_pos))

    def attack_allowed(self, unit, attacked_unit):
        """
        Checks whether unit can attack attacked_unit (attacked_unit at attack range of Unit).
        :param unit: Unit that wants to attack.
        :param attacked_unit: The Unit that is attacked by unit.
        :return: True if unit can attack attacked_unit, False otherwise.
        """
        return (unit in self.units
                and attacked_unit in self.units
                and unit.attack_allowed(attacked_unit))

    def simulate_attack(self, unit, attacked_unit):
        """
        Simulates an attack by unit on attacked_unit. Assumes the attack is valid.
        The number of hit points deducted from attacked_unit is equal to the attack
        stat of unit. If attacked_unit dies, it is removed from the board.
        :param unit: Unit that makes an attack.
        :param attacked_unit: Unit that is attacked by unit.
        """
        assert self.attack_allowed(unit, attacked_unit)
        self.damage_done[unit.team] += min(unit.atk, attacked_unit.hp)
        attacked_unit.hp -= unit.atk
        if attacked_unit.is_dead():
            self.unit_positions.remove((attacked_unit.x, attacked_unit.y))
            self.units.remove(attacked_unit)

    def game_finished(self):
        """
        Checks whether the game is finished or not. A game is finished if only one team has Units left.
        :return: True if the number of teams alive is 1 or less, False otherwise.
        """
        alive_teams = []
        for unit in self.units:
            if unit.team not in alive_teams:
                alive_teams.append(unit.team)
        return len(alive_teams) <= 1

    def evaluate_game(self, team):
        """
        Evaluate the results of the game
        """
        allies = list(filter(lambda x: x.team == team, self.original_units))
        living_allies = list(filter(lambda x: x.team == team, self.units))
        damage_done = self.damage_done[team]
        hp_left = sum(a.hp for a in living_allies)
        units_alive = len(list(filter(lambda u: u in self.units, allies)))
        return damage_done + hp_left + units_alive * 3

    def __str__(self):
        """
        Creates a string for the State object. Includes all the Units in the current state.
        :return: An overwritten string object for the State class.
        """
        return '\n'.join(str(u) for u in self.units)
