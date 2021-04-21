from unit import Unit
from statecontroller import StateController
from unitcontrollers import AIUnitController
from exporter import AsciiExporter


def turn_callback(turn, state):
    AsciiExporter.export(state, f'./results/Turn-{turn}.txt')


def simulation1():
    sc = StateController((500, 500), ['Chaos', 'Order'], turn_complete_callback=turn_callback)

    c1 = Unit((100, 4), {'hp': 30, 'atk': 4, 'range': 1, 'move': 3}, team='Chaos', name='Ze hadden een Yorick?')
    c2 = Unit((100, 8), {'hp': 45, 'atk': 2, 'range': 1, 'move': 3}, team='Chaos', name='Caravan eigenaar')
    c3 = Unit((100, 12), {'hp': 25, 'atk': 6, 'range': 2, 'move': 3}, team='Chaos', name='10-1-10 Yasuo')
    c4 = Unit((100, 13), {'hp': 20, 'atk': 6, 'range': 2, 'move': 3}, team='Chaos', name='Bad')
    c5 = Unit((100, 14), {'hp': 35, 'atk': 2, 'range': 1, 'move': 3}, team='Chaos', name='Also Bad + 10 pushups')

    o1 = Unit((200, 4), {'hp': 30, 'atk': 4, 'range': 1, 'move': 3}, team='Order', name='1-10-1 Yone')
    o2 = Unit((200, 8), {'hp': 45, 'atk': -2, 'range': 1, 'move': 3}, team='Order', name='Im a healer, but...')
    o3 = Unit((200, 12), {'hp': 25, 'atk': 6, 'range': 2, 'move': 3}, team='Order', name='Ziggs')
    o4 = Unit((200, 13), {'hp': 20, 'atk': 6, 'range': 2, 'move': 3}, team='Order', name='Jhon')
    o5 = Unit((200, 14), {'hp': 35, 'atk': 2, 'range': 1, 'move': 3}, team='Order', name='GrabShock')

    oc1 = AIUnitController(o1, sc.state)
    oc2 = AIUnitController(o2, sc.state)
    oc3 = AIUnitController(o3, sc.state)
    oc4 = AIUnitController(o4, sc.state)
    oc5 = AIUnitController(o5, sc.state)

    cc1 = AIUnitController(c1, sc.state)
    cc2 = AIUnitController(c2, sc.state)
    cc3 = AIUnitController(c3, sc.state)
    cc4 = AIUnitController(c4, sc.state)
    cc5 = AIUnitController(c5, sc.state)

    sc.add_unit_controllers([oc1, oc2, oc3, oc4, oc5, cc1, cc2, cc3, cc4, cc5])
    return sc

if __name__ == '__main__':
    sc = simulation1()
    sc.process_game()
