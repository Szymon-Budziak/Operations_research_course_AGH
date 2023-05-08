import numpy as np

from src.model import Settings, generate_random_solution
from src.algorithm import BeesSolver, stop_iterations, calculate_cost

settings = Settings(num_rocket_types=2,
                    num_module_types=4,
                    num_rockets=4,
                    rocket_capacity=10,
                    additional_fuel_costs=np.array(
                        [[3.22714791, 6.39551519, 5.92349917, 3.02169468],
                         [9.31912442, 8.56746934, 9.37825445, 1.80524675]]),
                    fuel_costs=np.array([39.9175704, 47.029129]),
                    module_amounts=np.array([6, 15, 9, 5]))

solver = BeesSolver(settings=settings,
                    population_size=12,
                    modules_mutations=5,
                    rockets_type_mutations=1,
                    elite_sites=3,
                    normal_sites=3,
                    elite_site_size=2,
                    normal_site_size=4)

if __name__ == '__main__':
    print('Random solution')
    random_solution = generate_random_solution(settings)
    print(random_solution.rocket_type_allocation)
    print(random_solution.module_allocation)
    print(calculate_cost(random_solution, settings))

    print('\nBees solution')
    bees_solution = solver.find_best_solution(stop_iterations(1000))
    print(bees_solution.rocket_type_allocation)
    print(bees_solution.module_allocation)
    print(calculate_cost(bees_solution, settings))
