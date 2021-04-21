class State:
    def __init__(self, board_dimensions):
        self.board_dimensions = board_dimensions
        self.units = []
        self.unit_positions = set()

    def add_unit(self, unit):
        assert (unit.x, unit.y) not in self.unit_positions
        assert unit.x >= 0 and unit.x < self.board_dimensions[0]
        assert unit.y >= 0 and unit.y < self.board_dimensions[1]
        self.units.append(unit)
        self.unit_positions.add((unit.x, unit.y))

    def simulate_move(self, unit, new_pos):
        assert self.movement_allowed(unit, new_pos)
        self.unit_positions.remove((unit.x, unit.y))
        self.unit_positions.add(new_pos)
        unit.x, unit.y = new_pos

    def movement_allowed(self, unit, new_pos):
        return (unit in self.units
                and new_pos[0] >= 0 and new_pos[0] < self.board_dimensions[0]
                and new_pos[1] >= 0 and new_pos[1] < self.board_dimensions[1]
                and (new_pos == (unit.x, unit.y) or new_pos not in self.unit_positions)
                and unit.movement_allowed(new_pos))

    def attack_allowed(self, unit, attacked_unit):
        return (unit in self.units
                and attacked_unit in self.units
                and unit.attack_allowed(attacked_unit))

    def simulate_attack(self, unit, attacked_unit):
        assert self.attack_allowed(unit, attacked_unit)
        attacked_unit.hp -= unit.atk
        if attacked_unit.is_dead():
            self.unit_positions.remove((attacked_unit.x, attacked_unit.y))
            self.units.remove(attacked_unit)

    def game_finished(self):
        alive_teams = []
        for unit in self.units:
            if unit.team not in alive_teams:
                alive_teams.append(unit.team)
        return len(alive_teams) <= 1

    def __str__(self):
        return '\n'.join(str(u) for u in self.units)
