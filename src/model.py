import numpy as np


class Settings:
    """
    Stores the settings required for the optimization problem
    """

    def __init__(self, num_rocket_types: int, num_module_types: int, num_rockets: int, rocket_capacity: int,
                 additional_fuel_costs: np.ndarray, fuel_costs: np.ndarray, module_amounts: np.ndarray) -> None:
        """
        Args:
            num_rocket_types (int): the number of different rocket types
            num_module_types (int): the number of different module types
            num_rockets (int): the number of available rockets
            rocket_capacity (int): the maximum capacity of each single rocket
            additional_fuel_costs (np.ndarray): the additional fuel costs for each rocket type. The array has a length
                                               equal to rocket_types_number
            fuel_costs (np.ndarray): the fuel costs for each rocket type. The array has a length equal to num_rocket_types
            module_amounts (np.ndarray): the amount of each module type. The array has a length equal to num_module_types

        Returns:
            None
        """
        self.num_rocket_types = num_rocket_types
        self.num_module_types = num_module_types
        self.num_rockets = num_rockets
        self.rocket_capacity = rocket_capacity
        self.additional_fuel_costs = additional_fuel_costs
        self.fuel_costs = fuel_costs
        self.module_amounts = module_amounts


class Solution:
    """
    Stores the solution for the optimization problem
    """

    def __init__(self, rocket_type_allocation: np.ndarray, module_allocation: np.ndarray) -> None:
        """
        Args:
            rocket_type_allocation (np.ndarray): the allocation of rocket types to transport the modules
            module_allocation (np.ndarray): the allocation of modules to each rocket

        Returns:
            None
        """
        self.rocket_type_allocation = rocket_type_allocation
        self.module_allocation = module_allocation


def is_valid_capacity(solution: Solution, settings: Settings) -> bool:
    """
    Checks whether the capacity of the rockets is sufficient to carry the modules allocated to them

    Args:
        solution (Solution): the solution to check
        settings (Settings): the settings of the problem

    Returns:
        True/False (bool): whether the solution is valid or not
    """
    return np.all(solution.module_allocation.sum(axis=1) <= settings.rocket_capacity)


def is_valid_module_total(solution: Solution, settings: Settings) -> bool:
    """
    Checks whether the total number of modules allocated to the rockets is equal to the number of modules available

    Args:
        solution (Solution): the solution to check
        settings (Settings): the settings of the problem

    Returns:
        True/False (bool): whether the solution is valid or not
    """
    return np.all(solution.module_allocation.sum(axis=0) == settings.module_amounts)


def calculate_cost(solution: Solution, settings: Settings) -> float:
    """
    Calculates the total cost of the solution

    Args:
        solution (Solution): the solution to check
        settings (Settings): the settings of the problem

    Returns:
        cost (float): the total cost of the solution
    """
    additional_fuel_cost = np.sum(
        solution.module_allocation * settings.additional_fuel_costs[solution.rocket_type_allocation, :])
    rockets_fuel_cost = np.sum(settings.fuel_costs[solution.rocket_type_allocation])
    return additional_fuel_cost + rockets_fuel_cost


def generate_random_rockets_type_allocation(settings: Settings) -> np.ndarray:
    """
    Generates a random allocation of rocket types

    Args:
        settings (Settings): the settings of the problem

    Returns:
        rockets_type_allocation (np.ndarray): the allocation of rocket types
    """
    return np.random.randint(low=0, high=settings.num_rocket_types, size=settings.num_rockets)


def generate_random_modules_allocation(settings: Settings) -> np.ndarray:
    """
    Generates a random allocation of modules to rockets

    Args:
        settings (Settings): the settings of the problem

    Returns:
        modules_allocation (np.ndarray): the allocation of modules to rockets
    """
    if settings.num_rockets * settings.rocket_capacity < settings.module_amounts.sum():
        raise ValueError('Not enough capacity to carry all modules.')

    allocation = np.zeros((settings.num_rockets, settings.num_module_types), dtype=np.int32)

    for module_type, amount in enumerate(settings.module_amounts):
        allocation[:, module_type] = np.random.multinomial(amount, np.ones(settings.num_rockets) / settings.num_rockets)

    while np.any(allocation.sum(axis=1) > settings.rocket_capacity):
        rocket_module_counts = allocation.sum(axis=1)

        # Find the rocket with the most modules and the one with the least modules
        max_rocket_index = np.argmax(rocket_module_counts)
        min_rocket_index = np.argmin(rocket_module_counts)

        # Find the module type with the most amount of modules in the rocket with the most modules
        module_index = np.argmax(allocation[max_rocket_index])

        # Calculate the amount of modules that need to be transferred
        num_modules_to_transfer = min(allocation[max_rocket_index, module_index],
                                      rocket_module_counts[max_rocket_index] - settings.rocket_capacity)

        # Transfer the modules from the rocket with the most modules to the one with the least
        allocation[max_rocket_index, module_index] -= num_modules_to_transfer
        allocation[min_rocket_index, module_index] += num_modules_to_transfer

    return allocation


def generate_random_solution(settings: Settings) -> Solution:
    """
    Generates a random solution for the optimization problem

    Args:
        settings (Settings): the settings of the problem

    Returns:
        solution (Solution): the generated solution
    """
    solution = Solution(generate_random_rockets_type_allocation(settings), generate_random_modules_allocation(settings))

    if not (is_valid_capacity(solution, settings) and is_valid_module_total(solution, settings)):
        raise RuntimeError('Solution is not valid.')

    return solution


if __name__ == "__main__":
    pass
