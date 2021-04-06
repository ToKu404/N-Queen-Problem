import os
import time
import psutil
import random


class GeneticAlgorithm:
    def __init__(self, n=int, max_fitness=float, population=list, generation=int):
        self.n = n
        self.max_fitness = max_fitness
        self.population = population
        self.generation = generation
        self.status = False

    # making random chromosomes
    @classmethod
    def random_chromosome(cls, size):
        return [random.randint(1, size) for _ in range(size)]

    def fitness(self, chromosome):
        bar = []
        for queen in chromosome:
            bar.append(chromosome.count(queen)-1)
        temp = [chromosome.count(queen) - 1 for queen in chromosome]

        horizontal_collisions = (sum(temp) / 2)

        n = len(chromosome)

        left_diagonal = [0] * 2 * n
        right_diagonal = [0] * 2 * n

        for i in range(n):
            left_diagonal[i + chromosome[i] - 1] += 1
            right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

        diagonal_collisions = 0

        for i in range(2 * n - 1):
            counter = 0

            if left_diagonal[i] > 1:
                counter += left_diagonal[i] - 1
            if right_diagonal[i] > 1:
                counter += right_diagonal[i] - 1

            diagonal_collisions += counter / (n - abs(i - n + 1))

        # 28 - (2 + 3) = 23
        return int(self.max_fitness - (horizontal_collisions + diagonal_collisions))

    def probability(self, chromosome, fitness):
        return fitness(chromosome) / self.max_fitness

    def random_pick(self, population, probabilities):
        population_with_probability = zip(population, probabilities)
        total = sum(w for c, w in population_with_probability)
        r = random.uniform(0, total)
        upto = 0

        for c, w in zip(population, probabilities):
            if upto + w >= r:
                return c

            upto += w

        assert False, "Shouldn't get here"

    # doing cross_over between two chromosomes
    def reproduce(self, x, y):
        n = len(x)
        c = random.randint(0, n - 1)

        return x[0:c] + y[c:n]

    # randomly changing the value of a random index of a chromosome
    def mutate(self, x):
        n = len(x)
        c = random.randint(0, n - 1)
        m = random.randint(1, n)
        x[c] = m

        return x

    def genetic_lizard(self, population, fitness):
        new_population = []
        mutation_probability = 0.03
        probabilities = [self.probability(i, fitness) for i in population]

        for i in range(len(population)):
            # best chromosome 1
            x = self.random_pick(population, probabilities)
            # best chromosome 2
            y = self.random_pick(population, probabilities)
            # creating two new chromosomes from the best 2 chromosomes
            child = self.reproduce(x, y)

            if random.random() < mutation_probability:
                child = self.mutate(child)

            self.print_chromosome(child)
            new_population.append(child)

            if fitness(child) == self.max_fitness:
                break

        return new_population

    def print_chromosome(self, chromosome):
        print(
            f"Chromosome = {str(chromosome)},  fitness = {self.fitness(chromosome)}")

    def solve(self):
        if self.n == 2 or self.n == 3:
            print(f"No solution possible for {self.n} queens.")
            return

        while not self.max_fitness in [
            self.fitness(chromosome) for chromosome in self.population
        ]:
            print(f"------------- Generation {self.generation} -------------")
            self.population = self.genetic_lizard(
                self.population, self.fitness)
            print("")
            print(
                f"Max. fitness = {max([self.fitness(i) for i in self.population])}")
            print("")
            self.generation += 1

        chrom_out = []

        print(f"Solved in generation {self.generation - 1}")

        for chrom in self.population:
            if self.fitness(chrom) == self.max_fitness:
                print("")
                print("One of the solutions: ")
                chrom_out = chrom
                self.print_chromosome(chrom)

        board = [[] for i in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                board[i].append(0)

        for i in range(self.n):
            board[self.n - chrom_out[i]][i] = 1

        # return board
        self.status = True
        return board

    def print_solution_and_status(self):
        print(f"Solving {self.n} Baby Lizard problem with genetic algorithm\n")
        # initialize time and memory usage
        start = time.time()
        process = psutil.Process(os.getpid())
        # get the solution
        solution = self.solve()
        # print the solution
        print()
        for i in range(self.n):
            for j in range(self.n):
                print(solution[i][j], end=" ")
            print()
        # print complexity
        print("\nStatus\t :", "Complete" if self.status else "Uncompleted")
        print(f"Memori\t : {process.memory_info().rss / 1024 ** 2} MB")
        print(f"Time\t : {time.time() - start} seconds")
        # return solution
        return solution


# if __name__ == "__main__":
#     n = int(input("Masukkan jumlah Lizard : "))
#     max_fitness = (n * (n - 1)) / 2
#     population = [GeneticAlgorithm.random_chromosome(n) for _ in range(100)]
#     generation = 1
#     n_queen_ga = GeneticAlgorithm(n, max_fitness, population, generation)
#     solution = n_queen_ga.print_solution_and_status()
