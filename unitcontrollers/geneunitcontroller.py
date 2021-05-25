from unitcontrollers.unitcontroller import UnitController


class GeneUnitController(UnitController):
    """
    The GeneUnitController is a UnitController based on genes.
    These genes indicate how a unit should move and what target they should
    attack. This controller is also used to "learn" using natural computing,
    since we can learn the genes using genetic programming.
    """
    def __init__(self, unit, state, genes):
        super().__init__(unit, state)
        self.genes = genes
        self.initiative = genes['initiative']  # Turn order
        self.greed = genes['greed']  # Focus low hp over high attack
        self.focus = genes['focus']  # Force focus in range target
        self.teamplayer = genes['teamplayer']  # Stay close to team
        self.evasiveness = genes['evasiveness']  # Evade high damage zones

    def get_enemies(self):
        """
        Gets a list of Units on the opposing team(s).
        :return: Returns a list of Units on opposing team(s).
        """
        return [u for u in self.state.units if u.team != self.unit.team]

    def get_allies(self):
        """
        Gets a list of Units on the allied team.
        :return: Returns a list of Units on the allied team.
        """
        return [u for u in self.state.units if u.team == self.unit.team and u != self.unit]
        
    def ally_distance(self, x, y, u2):
        """
        Calculates the distance between the given (x, y) position and a unit u2
        :param x: The x-position of the Unit belonging to this UnitController.
        :param y: The y-position of the Unit belonging to this UnitController.
        :param u2: The Unit u2.
        :return: Returns the distance between the x, y and the position of u2 
        based on the Euclidean distance between the units.
        """
        return abs(abs(x - u2.x) + abs(y - u2.y))

    def mlp_score(self, x, y):
        """
        Calculates a score that determines whether a unit likes a position
        (x, y) based on the amount of allies in the vicinity, as well as the 
        teamplayer gene normalised over the maximum amount of allies.
        :param x: The x-position of the Unit belonging to this UnitController.
        :param y: The y-position of the Unit belonging to this UnitController.
        :return: A score 
        """
        allies = self.get_allies()
        max_allies = len(allies)
        allies_in_range = sum(
            [1 for u in allies if self.ally_distance(x, y, u) <= u.range]
        )
        return (allies_in_range / (max_allies+0.001)) * self.teamplayer
    

    def distance(self, x, y, u2):
        """
        Calculates the distance between the given (x, y) and the position of u2
        :param x: The x-position of the Unit belonging to this UnitController.
        :param y: The y-position of the Unit belonging to this UnitController.
        :param u2: The Unit u2.
        :return: Returns the distance between the x, y and the position of u2 
        based on the Euclidean distance between the units and the range of this 
        Unit.
        """
        return abs(abs(x - u2.x) + abs(y - u2.y) - self.unit.range)

    def within_attack_distance(self, x, y, u2):
        """
        Calculates whether unit u2 is able to attack position (x, y)
        :param x: The x-position of the Unit belonging to this UnitController.
        :param y: The y-position of the Unit belonging to this UnitController.
        :param u2: The Unit u2.
        :return: True if the position can be attacked by unit u2, False
                 otherwise.
        """
        return abs(abs(x - u2.x) + abs(y - u2.y)) - u2.range <= 0

    def max_expected_damage(self, x, y):
        """
        Calculates whether unit u2 is able to attack position (x, y)
        :param x: The x-position of the Unit belonging to this UnitController.
        :param y: The y-position of the Unit belonging to this UnitController.
        :return: the sum total of damage that could be dealt to this unit if
                 the unit chooses to move to position (x, y).
        """
        return sum([e.atk for e in self.get_enemies()
                    if self.within_attack_distance(x, y, e)])

    def get_closest_enemy(self):
        """
        Gets the enemy closest to the Unit belonging to this UnitController.
        :return: The enemy closest to the Unit belonging to this UnitController
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
        :return: The enemy with lowest hit points on the field if it exists,
                 None otherwise.
        """
        lowest_enemy = list(sorted(self.get_enemies(), key=lambda h: h.hp))
        if lowest_enemy:
            return lowest_enemy[0]

    def get_highest_hp(self):
        """
        Obtain the maximum hp of all enemies.
        """
        return max(e.hp for e in self.get_enemies())

    def get_highest_atk(self):
        """
        Obtain the maximum attack of all enemies.
        """
        return max(e.atk for e in self.get_enemies())

    def get_sum_atk(self):
        """
        Obtain the maximum attack of all enemies.
        """
        return sum(e.atk for e in self.get_enemies())

    def in_walking_range(self, unit):
        """
        Indicates whether some unit is in range to attack it, after being
        allowed movement.
        """
        return self.distance(self.unit.x, self.unit.y, unit) < self.unit.move

    def get_sorted_appealing_enemies(self, enemies):
        """
        Sorts the given list of enemies based on which enemy is the most
        appealing target. If the unit has more focus, it will prefer an enemy
        within attack range. If the unit has more greed, it will prefer low hp
        targets.
        :param enemies: enemies to sort.
        :return: Sorted enemies based on which enemy is most appealing.
        """
        inv_scale_hp = lambda u: 1 - (u.hp / self.get_highest_hp())
        scale_atk = lambda u: u.atk / self.get_highest_atk()
        focus_modifier = lambda u: self.in_walking_range(u) * self.focus
        targets = sorted(
            enemies, 
            key=lambda h: -(
                inv_scale_hp(h) * self.greed +
                scale_atk(h) * (1 - self.greed) +
                focus_modifier(h)
            )
        )
        return list(targets)

    def get_most_appealing_enemy(self):
        """
        This function calculates which enemy seems best to attack based in this
        unit's genes. If the unit has more focus, it will prefer an enemy
        within attack range. If the unit has more greed, it will prefer low hp
        targets.
        :return: The enemy that looks most appealing to attack to this unit.
        """
        targets = self.get_sorted_appealing_enemies(self.get_enemies())
        if targets:
            return targets[0]

    def evasiveness_score(self, summed_atk, x, y):
        norm_attack =  summed_atk / (self.max_expected_damage(x, y) + 1e-3)
        return norm_attack * self.evasiveness

    def next_movement(self):
        """
        Decides the movement action of the Unit belonging to this
        UnitController based on the possible moves and the most appealing
        enemy.
        :return: A list of possible movement actions if any were found,
                 None otherwise.
        """
        enemy = self.get_most_appealing_enemy()
        moves = self.possible_moves()
        sum_atk = self.get_sum_atk()

        sorted_moves = list(
            sorted(
                moves,
                key=lambda m: self.distance(*m, enemy) -
                              self.mlp_score(*m) * 3 +
                              self.evasiveness_score(sum_atk, *m) * 3
            )
        )

        if sorted_moves:
            return sorted_moves[0]

    def next_attack(self):
        """
        Acts out an attack on the lowest enemy Unit if an attack can be made on
        that Unit.
        :return: The enemy to be attacked if one is chosen, None otherwise.
        """
        attacks = filter(
            lambda x: self.state.attack_allowed(self.unit, x), 
            self.get_enemies()
        )
        sorted_attacks = self.get_sorted_appealing_enemies(attacks)
        if sorted_attacks:
            return sorted_attacks[0]

    def decide_order_weight(self):
        """
        Gives back an order weight that decides the Unit order in a team.
        For the GeneUnitController this is 1 - the initiative gene.
        """
        return 1 - self.initiative
