import random
from statecontroller import StateController
from unitcontrollers import GeneUnitController
from collections import defaultdict


class EvoluationaryAlgorithm:
    def __init__(self, board_size, ea_units, enemy_ucs, team_ordering,
                 random_seed=1):
        """
        Initializes an EvolutionaryAlgorithm, takes the board size, the units
        to learn, the team ordering and the enemy unit *controllers* as
        arguments. You can also set the random seed through this initializer.
        """
        self.board_size = board_size
        self.ea_units = ea_units
        self.enemy_ucs = enemy_ucs
        self.team_ordering = team_ordering
        self.random_seed = random_seed
        self.random = random.Random()
        self.random.seed(self.random_seed)

    def rand_value(self):
        """
        Random value between 0 and 1 with two decimal digits.
        """
        return self.random.randrange(0, 100, 1) / 100

    def init_unit(self):
        """
        Initialize a set of genes for a unit.
        """
        return {
            "initiative": self.rand_value(),
            "greed": self.rand_value(),
            "focus": self.rand_value(),
            "teamplayer": self.rand_value(),
            "evasiveness": self.rand_value()
        }

    def init_individual(self):
        """
        Initializes a dictionary of genes for a team of units.
        """
        return {
            u.name: self.init_unit() for u in self.ea_units
        }

    def init_pop(self, pop_size):
        """
        Initialize a population of size n.
        """
        population = []
        for _ in range(pop_size):
            population.append(self.init_individual())
        return population

    def crossover(self, p1, p2):
        """
        Create two new individuals based on two parents
        """
        c1 = defaultdict(lambda: defaultdict(float))
        c2 = defaultdict(lambda: defaultdict(float))
        for u in p1:
            for x in p1[u]:
                if self.random.random() >= 0.5:
                    c1[u][x] = p1[u][x]
                    c2[u][x] = p2[u][x]
                else:
                    c1[u][x] = p2[u][x]
                    c2[u][x] = p1[u][x]
            c1[u] = dict(c1[u])
            c2[u] = dict(c2[u])
        return dict(c1), dict(c2)

    def mutate(self, genes, point_mutate):
        """
        Mutate the genes of an individual.
        """
        for u, v in genes.items():
            for g, v2 in v.items():
                if self.random.random() < point_mutate:
                    old = int(v2 * 100)
                    from_range = max(0, old - 50)
                    until_range = min(old + 50, 100)
                    val = self.random.randrange(from_range, until_range, 1) / 100
                    genes[u][g] = val

    def weighted_random(self, pairs):
        """
        Applies weighted random on tuples of (object, int), where the integers
        decide the weight.
        Returns the tuple (object, int) that got chosen.
        """
        total = sum(pair[1] for pair in pairs)
        r = self.random.randint(1, total)
        for value, weight in pairs:
            r -= weight
            if r <= 0: return value, weight

    def get_enemy_ucs(self, state):
        """
        Create a list of enemy Unit Controllers, this is done by resetting the
        known unit controllers such that the units in them are the same as they
        originally were.
        """
        res = []
        for uc in self.enemy_ucs:
            uc.reset_unit()
            uc.state = state
            res.append(uc)
        return res
        
    def simulation(self, genes):
        """
        Applies the given set of genes to a game and returns the score for the
        EA team.
        """
        sc = StateController(self.board_size, self.team_ordering)

        all_ucs = self.get_enemy_ucs(sc.state)
        for u in self.ea_units:
            orig_unit = u.clone_original()
            guc = GeneUnitController(orig_unit, sc.state, genes[u.name])
            all_ucs.append(guc)

        sc.add_unit_controllers(all_ucs)
        sc.process_game()
        playing_team = self.ea_units[0].team
        return sc.state.evaluate_game(playing_team)

    def seed_random(self):
        """
        Seeds the enemy unit controllers.
        """
        self.random.seed(self.random_seed)
        for uc in self.enemy_ucs:
            uc.seed_random(self.random_seed)

    def ea(self, pop_size=10, epochs=100, point_mutate=0.15):
        """
        Apply the evolutionary algorithm, takes some optional parameters:
         - the population size (default 10)
         - the number of epochs (default 100)
         - the point mutate chance (default .15) (applies on each gene)
        This returns the best set of genes and also the best evaluation for
        each epoch.
        """
        population = self.init_pop(pop_size)
        evals = []
        best_individuals = []
        for e in range(epochs):
            print('EPOCH', e)
            self.seed_random()
            simulations = [(p, self.simulation(p)) for p in population]
            sorted_sims = sorted(simulations, key=lambda s: -s[1])
            evals.append([sims[1] for sims in sorted_sims])
            best_individuals.append(sorted_sims[0][0])
            new_pop = list(s[0] for s in sorted_sims[:pop_size // 2])
            while len(new_pop) < pop_size:
                p1, score = self.weighted_random(sorted_sims)
                parents = list(sorted_sims)
                parents.remove((p1, score))
                p2, _ = self.weighted_random(parents)
                c1, c2 = self.crossover(p1, p2)
                self.mutate(c1, point_mutate)
                self.mutate(c2, point_mutate)
                new_pop.append(c1)
                if len(new_pop) < pop_size:
                    new_pop.append(c2)
            population = new_pop
        return sorted_sims[0][0], evals, best_individuals
