from config import G, N
import numpy as np
from selection.selection_method import SelectionMethod
from copy import copy, deepcopy
from model.fitness_functions import Fx2
from model.population import Population
from model.encoding import FloatEncoder
from scipy.stats import rankdata


# class LinearRankingRWS(SelectionMethod):
#     def __init__(self, beta_value):
#         self.beta_value = beta_value

#     def select(self, population):
#         num_offsprings = [0 for _ in range(len(population.chromosomes))]
#         fitness_list = population.fitnesses
#         n = len(fitness_list)
#         rank_order = np.argsort(fitness_list)
#         ranks = np.empty(n)
#         ranks[rank_order] = np.arange(0, n)

#         probabilities = ((2 - self.beta_value) / n) + (2 * ranks * (self.beta_value - 1)) / (n * (n - 1))

#         chosen = np.random.choice(len(population.chromosomes), size=n, p=probabilities)

#         for i in chosen:
#             num_offsprings[i] += 1

#         mating_pool = [deepcopy(population.chromosomes[i]) for i in chosen]
#         np.random.shuffle(mating_pool)
#         population.update_chromosomes(mating_pool)

#         return num_offsprings
    

class ExponentialRankingRWS(SelectionMethod):
    def __init__(self, с_value):
        self.с_value = с_value

    def select(self, population):
        num_offsprings = [0 for _ in range(len(population.chromosomes))]
        fitness_list = population.fitnesses
        n = len(fitness_list)
        rank_order = np.argsort(fitness_list)
        ranks = np.empty(n)
        ranks[rank_order] = np.arange(0, n)

        unnormalized_probabilities = (self.с_value - 1) / (self.с_value ** n - 1) * self.с_value ** (n - ranks)

        # Normalize probabilities
        sum_probabilities = np.sum(unnormalized_probabilities)
        probabilities = unnormalized_probabilities / sum_probabilities

        chosen = np.random.choice(len(population.chromosomes), size=n, p=probabilities)

        for i in chosen:
            num_offsprings[i] += 1

        mating_pool = [deepcopy(population.chromosomes[i]) for i in chosen]
        np.random.shuffle(mating_pool)
        population.update_chromosomes(mating_pool)

        return num_offsprings


class LinearRankingRWS(SelectionMethod):

    def __init__(self, b=1.4):
        self.b = b

    @staticmethod
    def get_offspring_count(population: Population, chosen_individuals):
        offspring_counts = np.zeros_like(population.chromosomes)
        for chr in chosen_individuals:
            offspring_counts[chr.id] += 1
        num_offsprings = np.zeros_like(offspring_counts)
        for i in range(num_offsprings.shape[0]):
            num_offsprings[i] = offspring_counts[population.chromosomes[i].id]
        assert np.sum(num_offsprings) == num_offsprings.shape[0]
        return num_offsprings

    def select(self, population):
        fitness_list = population.fitnesses

        rng = np.random.default_rng()
        length = len(fitness_list)

        # fitness_list = population.fitnesses
        # length = len(fitness_list)
        ranks = np.argsort(np.argsort(fitness_list))
        probabilities = (2 - self.b) / length + 2 * ranks * (self.b - 1) / (length * (length - 1))

        indices = np.arange(length)
        rng.shuffle(indices)

        shuffled_chromosomes = population.chromosomes[indices]
        shuffled_probabilities = probabilities[indices]

        chosen = np.random.choice(shuffled_chromosomes, size=N, p=shuffled_probabilities)

        num_offsprings = self.get_offspring_count(population, chosen)

        mating_pool = np.array([copy(chr) for chr in chosen])
        population.update_chromosomes(mating_pool)

        return num_offsprings


# class LinearRankingModifiedRWS(SelectionMethod):
#     def __init__(self, beta_value_modified):
#         self.beta_value_modified = beta_value_modified

#     def select(self, population):
#         num_offsprings = [0 for _ in range(len(population.chromosomes))]
#         fitness_list = population.fitnesses
#         n = len(fitness_list)
#         rank_order = np.argsort(fitness_list)
#         ranks = np.empty(n)
#         ranks[rank_order] = np.arange(0, n)
#         chromosomes = [(i, ch) for i, ch in enumerate(population.chromosomes)]

#         # Calculate modified ranks for chromosomes with equal fitness
#         modified_ranks = np.empty(n)
#         i = 0
#         while i < n:
#             count = 1
#             while i + count < n and fitness_list[rank_order[i]] == fitness_list[rank_order[i + count]]:
#                 count += 1
#             modified_ranks[i:i + count] = np.mean(ranks[i:i + count])
#             i += count

#         probabilities = ((2 - self.beta_value_modified) / n) + (2 * modified_ranks * (self.beta_value_modified - 1)) / (
#                     n * (n - 1))

#         chosen = np.random.choice(len(population.chromosomes), size=n, p=probabilities)

#         for i in chosen:
#             num_offsprings[i] += 1

#         mating_pool = [deepcopy(population.chromosomes[i]) for i in chosen]
#         np.random.shuffle(mating_pool)
#         population.update_chromosomes(mating_pool)

#         return num_offsprings


class LinearRankingModifiedRWS(SelectionMethod):

    def __init__(self, b=1.4):
        self.b = b

    def select(self, population):
        fitness_list = population.fitnesses

        rng = np.random.default_rng()
        length = len(fitness_list)

        ranks = rankdata(fitness_list, method='average') - 1
        # probabilities = compute_probabilities(ranks, self.b, length)
        probabilities = (2 - self.b) / length + 2 * ranks * (self.b - 1) / (length * (length - 1))
        probabilities /= probabilities.sum()

        indices = np.arange(length)
        rng.shuffle(indices)

        shuffled_chromosomes = population.chromosomes[indices]
        shuffled_probabilities = probabilities[indices]

        chosen = rng.choice(shuffled_chromosomes, size=N, p=shuffled_probabilities)

        num_offsprings = LinearRankingRWS.get_offspring_count(population, chosen)

        mating_pool = np.array([copy(chr) for chr in chosen])
        population.update_chromosomes(mating_pool)

        return num_offsprings


if __name__ == '__main__':
    population = Population(Fx2(FloatEncoder(0.0, 10.23, 10)))
    # lrr = LinearRankingModifiedRWS(2.)
    lrr = LinearRankingRWS(2.)
    num_offsprings = lrr.select(population)
    print(f'#offspring = {num_offsprings}')