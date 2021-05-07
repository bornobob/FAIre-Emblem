from state import State


class StateController:
    """
    Creates a StateController object.
    """
    def __init__(self, board_dimensions, team_ordering,
                 turn_complete_callback=None):
        """
        Initializes a StateController object.
        :param board_dimensions: The x- and y-dimensions of the playing board.
        :param team_ordering: The turn order of the teams on the playing board.
        :param turn_complete_callback:
        """
        self.state = State(board_dimensions)
        self.unit_controllers = []
        self.team_ordering = team_ordering
        self.turn_complete_callback = turn_complete_callback

    def add_unit_controllers(self, unit_controllers):
        """
        Adds all the UnitControllers to the StateController.
        :param unit_controllers: A list of all the UnitController objects, one
                                 per Unit that should be on the board.
        """
        self.unit_controllers += unit_controllers

    def get_team_ucs(self, team):
        """
        Gets all the UnitControllers from the given team.
        :param team: The team whose UnitControllers are requested.
        :return: A list of UnitControllers for all Units on team.
        """
        return filter(lambda u: u.unit.team == team, self.unit_controllers)

    def get_turn_ordering(self):
        """
        Gets a list of the order of every Unit on the field. Is done per team,
        for each team the Unit order is sorted by their order weight.
        :return: A ordered list for all the Units on the field.
        """
        ordering = []
        for team in self.team_ordering:
            ordering += list(sorted(self.get_team_ucs(team),
                                    key=lambda u: u.decide_order_weight()))
        return ordering

    def process_movement(self, unit_controller):
        """
        Makes unit_controller act out the move action of the corresponding Unit
        if it has a new position.
        :param unit_controller: UnitController of the Unit that moves.
        """
        new_position = unit_controller.next_movement()
        if new_position:
            self.state.simulate_move(unit_controller.unit, new_position)

    def process_attack(self, unit_controller):
        """
        Makes unit_controller act out the attack action of the corresponding
        Unit if it attacks something.
        :param unit_controller: UnitController of the Unit that makes an
                                attack.
        """
        attacked_unit = unit_controller.next_attack()
        if attacked_unit:
            self.state.simulate_attack(unit_controller.unit, attacked_unit)

    def process_game(self):
        """
        Processes an entire game until only one team is alive.
        """
        self.state.original_units = list(self.state.units)
        not_finished = True
        turn = 1
        while not_finished:
            for u_c in self.get_turn_ordering():
                if u_c.unit.is_dead(): 
                    continue
                self.process_movement(u_c)
                self.process_attack(u_c)
                if self.state.game_finished():
                    not_finished = False
                    break
            if self.turn_complete_callback:
                self.turn_complete_callback(turn, self.state)
            turn += 1
