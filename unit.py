class Unit:
    def __init__(self, location, stats, team, name=''):
        self.team = team
        self.max_hp = stats['hp']
        self.hp = stats['hp']
        self.atk = stats['atk']
        self.range = stats['range']
        self.move = stats['move']
        self.x = location[0]
        self.y = location[1]
        self.name = name

    def movement_allowed(self, new_pos):
        x, y = new_pos
        return abs(x - self.x) + abs(y - self.y) <= self.move

    def attack_allowed(self, enemy_unit):
        x, y = enemy_unit.x, enemy_unit.y
        return (abs(x - self.x) + abs(y - self.y) == self.range
                and self.team != enemy_unit.team)

    def is_dead(self):
        return self.hp <= 0

    def __str__(self):
        return f'<{self.team}\'s {self.name}, ({self.x}, {self.y}) {self.hp} hp>'
