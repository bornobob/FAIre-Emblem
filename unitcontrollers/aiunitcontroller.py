import random
from unitcontrollers.unitcontroller import UnitController


class AIUnitController(UnitController):
    def get_enemies(self):
        res = []
        for u in self.state.units:
            if u.team != self.unit.team:
                res.append(u)
        return res

    def distance(self, x, y, u2):
        return abs(abs(x - u2.x) + abs(y - u2.y) - self.unit.range)

    def get_closest_enemy(self):
        closest_enemy, closest_distance = None, 99999
        for enemy in self.get_enemies():
            dist = self.distance(self.unit.x, self.unit.y, enemy)
            if dist < closest_distance:
                closest_distance, closest_enemy = dist, enemy
        return closest_enemy

    def possible_moves(self):
        res = []
        for x in range(self.unit.x - self.unit.move, self.unit.x + self.unit.move + 1):
            diff = self.unit.move - abs(self.unit.x - x)
            for y in range(self.unit.y - diff, self.unit.y + diff + 1):
                if self.state.movement_allowed(self.unit, (x, y)):
                    res.append((x, y))
        return res

    def next_movement(self):
        enemy = self.get_closest_enemy()
        moves = self.possible_moves()
        sorted_moves = list(sorted(moves, key=lambda m: self.distance(*m, enemy)))
        if sorted_moves:
            return sorted_moves[0]

    def next_attack(self):
        enemy = self.get_closest_enemy()
        if self.state.attack_allowed(self.unit, enemy):
            return enemy
    
    def decide_order_weight(self):
        return random.random()
