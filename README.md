# Operations research project "Delivery of space base modules to Mars"

Our task is to deliver all modules of the space base to Mars. We have a limited number of rockets of a specific capacity
at our disposal, differing in base fuel combustion and matching the modules. The rocket's final fuel consumption depends
on the modules being carried and consists of baseline combustion and module-dependent combustion. The goal is to choose
a combination of rockets that burns as little fuel as possible.

To solve this problem we will be using the [Bees algorithm](https://en.wikipedia.org/wiki/Bees_algorithm).

## Dependencies

- Python >= 3.8
- numpy

## Project structure

### src folder

Inside **src** folder there are *algorithm.py* and *model.py* files.

- **algorithm.py** provides an implementation of an optimization algorithm based on the bees algorithm. This algorithm
  is used to solve optimization problems by simulating a bee colony, and its main objective is to generate a set of
  possible solutions, which can be improved iteratively to reach an optimal solution. The algorithm starts by generating
  a population of solutions (each representing a colony of bees). Then, it performs several iterations in which it
  evolves the population by selecting the best solutions, generating new ones, and applying mutations to them.


- **model.py** inside this file we define two classes Settings and Solution and several functions for solving an
  optimization problem related to the allocation of rockets and modules. The problem consists of allocating a given
  number of modules to a given number of rockets, where each rocket has a limited capacity, and the cost of transporting
  a module depends on the type of rocket used to transport it.

### example.py file

In **example.py** file we provide an example of how to use our algorithm. We are creating an example settings and solver
objects. Then we are solving it using a *random solver* and *bees algorithm*. To run the code, simply execute the
script. The output will include the rocket type allocation, module allocation, and cost for both a random solution and
the optimized Bees solution.

## Installation

1. Clone the repository:

```shell
git clone https://github.com/Szymon-Budziak/Operations_research_course_AGH.git
```

2. Create virtual environment, activate it and install dependencies:

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run the example:

```shell
python example.py
```

#### Credits

This project was created by Szymon Budziak, Alicja Hurbol and [Jakub Szymczak](https://github.com/SzymczakJ).