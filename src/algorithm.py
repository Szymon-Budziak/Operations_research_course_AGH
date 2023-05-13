import numpy as np
import random
import copy

from src.model import Solution, Settings, calculate_cost, generate_random_solution


class BeesSolver:
    """
    Represents an optimization algorithm that simulates a bee colony to solve a problem (bees algorithm)
    """

    def __init__(self, settings: Settings, population_size: int, modules_mutations: int, rockets_type_mutations: int,
                 elite_sites: int, normal_sites: int, elite_site_size: int, normal_site_size: int) -> None:
        """
        Args:
            settings (Settings): the settings of the problem
            population_size (int): the size of the population of bees used in the algorithm
            modules_mutations (int): the number of mutations to perform on the modules allocation
            rockets_type_mutations (int): the number of mutations to perform on the rockets type allocation
            elite_sites (int): the number of elite sites that are maintained in the population
            normal_sites (int): the number of normal sites that are maintained in the population
            elite_site_size (int): the size of the elite site
            normal_site_size (int): the size of each normal site

        Returns:
            None
        """
        self.settings = settings
        self.population_size = population_size
        self.modules_mutations = modules_mutations
        self.rockets_type_mutations = rockets_type_mutations
        self.elite_sites = elite_sites
        self.normal_sites = normal_sites
        self.elite_site_size = elite_site_size
        self.normal_site_size = normal_site_size
        self.population = []

    def __mutate_rockets_type_allocation(self, solution: Solution) -> None:
        """
        Mutates the type of rocket allocation for a given solution

        Args:
            solution (Solution): the solution to mutate

        Returns:
            None
        """
        rocket_index = random.randrange(self.settings.num_rockets)
        new_rocket_type = random.randrange(self.settings.num_rocket_types)
        solution.rocket_type_allocation[rocket_index] = new_rocket_type

    def __mutate_modules_allocation(self, solution: Solution) -> None:
        """
        Mutates the module allocation for a given solution

        Args:
            solution (Solution): the solution to mutate

        Returns:
            None
        """
        rocket_capacities = self.settings.rocket_capacity - solution.module_allocation.sum(axis=1)

        module_type_index = random.randrange(self.settings.num_module_types)

        to_rocket_index = random.choice(np.argwhere(rocket_capacities > 0).flatten())

        from_rocket_index = random.choice(np.argwhere(solution.module_allocation[:, module_type_index] > 0).flatten())

        max_module_amount = min(solution.module_allocation[from_rocket_index, module_type_index],
                                rocket_capacities[to_rocket_index])

        module_amount = random.randint(1, max_module_amount)
        solution.module_allocation[from_rocket_index, module_type_index] -= module_amount
        solution.module_allocation[to_rocket_index, module_type_index] += module_amount

    def __mutate_solution(self, solution: Solution) -> None:
        """
        Mutates a given solution by calling _mutate_rockets_type_allocation() and _mutate_modules_allocation() based on
        the defined number of mutations

        Args:
            solution (Solution): the solution to mutate

        Returns:
            None
        """
        for _ in range(self.modules_mutations):
            self.__mutate_modules_allocation(solution)

        for _ in range(self.rockets_type_mutations):
            self.__mutate_rockets_type_allocation(solution)

    def __find_best_neighbour(self, solution: Solution, neighbours_count: int) -> Solution:
        """
        Finds the best neighbouring solution for a given solution by creating a number of mutated solutions and
        selecting the best one based on the cost

        Args:
            solution (Solution): the solution to find the best neighbour for
            neighbours_count (int): the number of neighbours to create

        Returns:
            solution (Solution): the best neighbouring solution
        """
        neighbours = [copy.deepcopy(solution) for _ in range(neighbours_count)]

        for n in neighbours:
            self.__mutate_solution(n)

        neighbours.append(solution)

        return sorted(neighbours, key=lambda sol: calculate_cost(sol, self.settings))[0]

    def simulate_population(self) -> None:
        """
        Simulates the population by applying the _find_best_neighbour() function to the elite and normal sites of the
        population and generating new random solutions for the rest

        Returns:
            None
        """
        self.population.sort(key=lambda sol: calculate_cost(sol, self.settings))

        for i in range(0, self.elite_sites):
            self.population[i] = self.__find_best_neighbour(self.population[i], self.elite_site_size)

        for i in range(self.elite_sites, self.elite_sites + self.normal_sites):
            self.population[i] = self.__find_best_neighbour(self.population[i], self.normal_site_size)

        for i in range(self.elite_sites + self.normal_sites, len(self.population)):
            self.population[i] = generate_random_solution(self.settings)

    def find_best_solution(self, iterations: int) -> Solution:
        """
        Evolves the population of solutions for a given number of iterations and returns the best solution found

        Args:
            iterations (int): the number of iterations to evolve the population

        Returns:
            solution (Solution): the best solution found
        """
        self.population = [generate_random_solution(self.settings) for _ in range(self.population_size)]

        for _ in range(iterations):
            self.simulate_population()

        return self.population[0]

    def init_population(self) -> None:
        """
        Generates random population.

        Returns:
            None
        """
        self.population = [generate_random_solution(self.settings) for _ in range(self.population_size)]

    def current_cost(self) -> float:
        """
        Returns current cost of first solution from population.

        Returns:
            float: current cost of first solution from population
        """
        return calculate_cost(self.population[0], self.settings)


if __name__ == "__main__":
    pass
