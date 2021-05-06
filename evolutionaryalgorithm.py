import random
from unit import Unit
from statecontroller import StateController
from unitcontrollers import AIUnitController, GeneUnitController
from exporter import AsciiExporter
from collections import defaultdict


class EvoluationaryAlgorithm:
    def __init__(self, ucs, team, epochs=100, pop_size=10, point_mutate=0.15, random_seed=1):
        random.seed(random_seed)
        self.epochs = epochs
        self.point_mutate = point_mutate
        self.pop_size = pop_size
        self.ucs = ucs
        self.team = team
        
    @staticmethod
    def rand_value():
        """
        Random value between 0 and 1 with two decimal digits.
        """
        return random.randrange(0, 100, 1)/100

    @staticmethod
    def init_unit():
        """
        Initialize a set of genes for a unit.
        """
        return {
            "initiative": rand_value(),
            "greed": rand_value(),
            "focus": rand_value()
        }

    def get_units(self):
        pass

    def init_individual(self):
        """
        Initializes a dictionary of genes for a team of units.
        """
        return {'bob':init_unit(), 'bart':init_unit()}
        #{u: init_unit() for u in self.}
    
    def init_pop(self):
        """
        Initialize a population of size n. 
        """
        population = []
        for i in range(self.pop_size):
            population.append(self.init_individual(units))
        return population

    @staticmethod
    def crossover(p1, p2):
        """
        Create two new individuals based on two parents
        """
        c1 = defaultdict(lambda: defaultdict(float))
        c2 = defaultdict(lambda: defaultdict(float))
        for u in p1:
            for x in p1[u]:
                if random.random() >= 0.5:
                    c1[u][x] = p1[u][x]
                    c2[u][x] = p2[u][x]
                else:
                    c1[u][x] = p2[u][x]
                    c2[u][x] = p1[u][x]
            c1[u] = dict(c1[u])
            c2[u] = dict(c2[u])
        return dict(c1), dict(c2)

    def mutate(self, genes):
        """
        return a mutation from an individual
        """
        for u, v in genes.items():
            for g, v2 in v.items():
                if random.random() < self.point_mutate:
                    old = int(v2 * 100)
                    new_val = random.randrange(max(0, old - 50), min(old + 50, 100), 1) / 100
                    genes[u][g] = new_val


    def simulation(self, genes):
        sc = StateController((7, 7), ['Js', 'Bs'])

        c1 = Unit((0, 0), {'hp': 20, 'atk': 2, 'range': 2, 'move': 2}, team='Js', name='justin')
        c2 = Unit((1, 0), {'hp': 20, 'atk': 3, 'range': 3, 'move': 2}, team='Js', name='johan')

        o1 = Unit((3, 3), {'hp': 20, 'atk': 2, 'range': 2, 'move': 2}, team='Bs', name='bob')
        o2 = Unit((4, 3), {'hp': 20, 'atk': 3, 'range': 1, 'move': 2}, team='Bs', name='bart')

        default_genes = {'initiative': 0.5, 'greed': 0.5, 'focus': 0.5}


        a1 = GeneUnitController(c1, sc.state, default_genes)
        a2 = GeneUnitController(c2, sc.state, default_genes)

        g1 = GeneUnitController(o1, sc.state, genes[o1.name])
        g2 = GeneUnitController(o2, sc.state, genes[o2.name])


        sc.add_unit_controllers([a1, a2, g1, g2])
        sc.process_game()
        return sc.state.evaluate_game(team)

    @staticmethod
    def weighted_random(pairs):
        total = sum(pair[1] for pair in pairs)
        r = random.randint(1, total)
        for (value, weight) in pairs:
            r -= weight
            if r <= 0: return value, weight


    def ea(self):
        """
        Evolutionary algorithm
        """
        population = init_pop()
        best_evals = []
        for e in range(self.epochs):
            print('EPOCH', e)
            simulations = [(p, self.simulation(p)) for p in population]
            sorted_sims = sorted(simulations, key=lambda s: -s[1])
            best_evals.append(sorted_sims[0][1])
            new_pop = list(s[0] for s in sorted_sims[:pop_size // 2])
            while len(new_pop) < pop_size:
                p1, p1_score = weighted_random(sorted_sims)
                parents = list(sorted_sims)
                parents.remove((p1, p1_score))
                p2, _ = weighted_random(parents)
                baby1, baby2 = crossover(p1, p2)
                mutate(baby1)
                mutate(baby2)
                new_pop.append(baby1)
                if len(new_pop) < pop_size:
                    new_pop.append(baby2)
            population = new_pop
        return sorted_sims[0][0], best_evals

if __name__ == '__main__':
    pass
    #random.seed(1)
    #best_genes, evals = ea(['bob', 'bart'], pop_size=2)
    #print(evals)
    #print(best_genes)
    #simulation(best_genes, 'Bs')