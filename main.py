from unit import Unit
from unitcontrollers import AIUnitController
from evolutionaryalgorithm import EvoluationaryAlgorithm


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

oc1 = AIUnitController(o1, state=None)
oc2 = AIUnitController(o2, state=None)
oc3 = AIUnitController(o3, state=None)
oc4 = AIUnitController(o4, state=None)
oc5 = AIUnitController(o5, state=None)


if __name__ == '__main__':
    ea = EvoluationaryAlgorithm(
        board_size=(500, 500),
        ea_units=[c1, c2, c3, c4, c5],
        enemy_ucs=[oc1, oc2, oc3, oc4, oc5],
        team_ordering=['Order', 'Chaos']
    )
    best_genes, scores = ea.ea(pop_size=4, epochs=10)
    print(scores)
