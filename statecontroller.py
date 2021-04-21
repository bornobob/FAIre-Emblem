from state import State


class StateController:
    def __init__(self, board_dimensions, team_ordering, turn_complete_callback=None):
        self.state = State(board_dimensions)
        self.unit_controllers = []
        self.team_ordering = team_ordering
        self.turn_complete_callback = turn_complete_callback

    def add_unit_controllers(self, unit_controllers):
        self.unit_controllers += unit_controllers

    def get_team_ucs(self, team):
        return filter(lambda u: u.unit.team == team, self.unit_controllers)

    def get_turn_ordering(self):
        ordering = []
        for team in self.team_ordering:
            ordering += list(sorted(self.get_team_ucs(team), key=lambda u: -u.decide_order_weight()))
        return ordering

    def process_movement(self, unit_controller):
        new_position = unit_controller.next_movement()
        if new_position:
            self.state.simulate_move(unit_controller.unit, new_position)

    def process_attack(self, unit_controller):
        attacked_unit = unit_controller.next_attack()
        if attacked_unit:
            self.state.simulate_attack(unit_controller.unit, attacked_unit)

    def process_game(self):
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
