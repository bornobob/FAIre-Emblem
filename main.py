from unit import Unit
from unitcontrollers import AIUnitController
from evolutionaryalgorithm import EvoluationaryAlgorithm
import matplotlib.pyplot as plt
import numpy as np
import os
from json import dumps


c1 = Unit((100, 4), {'hp': 30, 'atk': 4, 'range': 1, 'move': 3}, team='Chaos', name='A')
c2 = Unit((100, 8), {'hp': 45, 'atk': 2, 'range': 1, 'move': 2}, team='Chaos', name='B')
c3 = Unit((100, 12), {'hp': 25, 'atk': 6, 'range': 2, 'move': 3}, team='Chaos', name='C')
c4 = Unit((100, 13), {'hp': 20, 'atk': 6, 'range': 2, 'move': 3}, team='Chaos', name='D')
c5 = Unit((100, 14), {'hp': 35, 'atk': 2, 'range': 1, 'move': 3}, team='Chaos', name='E')

c6 = Unit((102, 4), {'hp': 30, 'atk': 4, 'range': 1, 'move': 3}, team='Chaos', name='F')
c7 = Unit((102, 8), {'hp': 45, 'atk': 2, 'range': 1, 'move': 2}, team='Chaos', name='G')
c8 = Unit((102, 12), {'hp': 25, 'atk': 6, 'range': 2, 'move': 3}, team='Chaos', name='H')
c9 = Unit((102, 13), {'hp': 20, 'atk': 6, 'range': 2, 'move': 3}, team='Chaos', name='I')
c10 = Unit((102, 14), {'hp': 35, 'atk': 2, 'range': 1, 'move': 3}, team='Chaos', name='J')

o1 = Unit((150, 4), {'hp': 30, 'atk': 4, 'range': 1, 'move': 3}, team='Order', name='1-10-1 Yone')
o2 = Unit((150, 8), {'hp': 45, 'atk': 2, 'range': 1, 'move': 2}, team='Order', name='Im a healer, but...')
o3 = Unit((150, 12), {'hp': 25, 'atk': 6, 'range': 2, 'move': 3}, team='Order', name='Ziggs')
o4 = Unit((150, 13), {'hp': 20, 'atk': 6, 'range': 2, 'move': 3}, team='Order', name='Jhon')
o5 = Unit((150, 14), {'hp': 35, 'atk': 2, 'range': 1, 'move': 3}, team='Order', name='GrabShock')

o6 = Unit((152, 4), {'hp': 30, 'atk': 4, 'range': 1, 'move': 3}, team='Order', name='1-10-1 Yone2')
o7 = Unit((152, 8), {'hp': 45, 'atk': 2, 'range': 1, 'move': 2}, team='Order', name='Im a healer, but...2')
o8 = Unit((152, 12), {'hp': 25, 'atk': 6, 'range': 2, 'move': 3}, team='Order', name='Ziggs2')
o9 = Unit((152, 13), {'hp': 20, 'atk': 6, 'range': 2, 'move': 3}, team='Order', name='Jhon2')
o10 = Unit((152, 14), {'hp': 35, 'atk': 2, 'range': 1, 'move': 3}, team='Order', name='GrabShock2')

oc1 = AIUnitController(o1, state=None)
oc2 = AIUnitController(o2, state=None)
oc3 = AIUnitController(o3, state=None)
oc4 = AIUnitController(o4, state=None)
oc5 = AIUnitController(o5, state=None)
oc6 = AIUnitController(o6, state=None)
oc7 = AIUnitController(o7, state=None)
oc8 = AIUnitController(o8, state=None)
oc9 = AIUnitController(o9, state=None)
oc10 = AIUnitController(o10, state=None)


if __name__ == '__main__':
    epochs = 30

    ea_units_testing = [
        [c1, c2, c3, c4, c5, c6],
        [c1, c2, c3, c4, c5, c6, c7, c8],
        [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]
    ]

    enemy_ucs_testing = [
        [oc1, oc2, oc3, oc4, oc5, oc6],
        [oc1, oc2, oc3, oc4, oc5, oc6, oc7, oc8],
        [oc1, oc2, oc3, oc4, oc5, oc6, oc7, oc8, oc9, oc10]
    ]
    
    pop_sizes = [10, 20]
    point_mutates = [0.20, 0.40]

    SAVE_DIR = os.path.join(os.getcwd(), 'results')

    # begin of tests
    for ea_units, enemy_ucs in zip(ea_units_testing, enemy_ucs_testing):
        for pop_size in pop_sizes:
            for point_mutate in point_mutates:
                ea = EvoluationaryAlgorithm(
                    board_size=(500, 500),
                    ea_units=ea_units,
                    enemy_ucs=enemy_ucs,
                    team_ordering=['Order', 'Chaos'],
                    random_seed=2112
                )
                best_genes, scores, individuals = ea.ea(pop_size=pop_size,
                                                        epochs=epochs,
                                                        point_mutate=point_mutate)

                best_scores = [indvs[0] for indvs in scores]
                not_the_best_scores = [indvs[1:] for indvs in scores]
                
                medians = np.median(scores, axis=1)
                means = np.mean(scores, axis=1)

                all_epochs = list(range(epochs))

                plt.clf()
                plt.plot(all_epochs, best_scores, label='Best scores')

                for srs, e in zip(not_the_best_scores, all_epochs):
                    for sc in srs:
                        plt.plot(e, sc, 'gx')
                
                plt.plot([], [], 'gx', label='Individual scores')

                plt.plot(all_epochs, medians, '--', label='Median scores')
                plt.plot(all_epochs, means, '.-.', label='Average scores')
                
                plt.legend(loc='best')

                plt.xlabel('Epoch')
                plt.ylabel('Score')
                plt.title(f'Performance for: #units: {len(ea_units)} vs {len(enemy_ucs)},\npoint mutate: {point_mutate}, population size: {pop_size}')

                sub_pth = f'{len(ea_units)}_vs_{len(enemy_ucs)}_PM_{point_mutate}_PS_{pop_size}'
                pth = os.path.join(SAVE_DIR, sub_pth)
                os.mkdir(pth)
                image_pth = os.path.join(pth, 'result.png')
                plt.savefig(image_pth)
                genes_pth = os.path.join(pth, 'genes.json')
                with open(genes_pth, 'w') as f:
                    f.write(dumps(best_genes, indent=2))
