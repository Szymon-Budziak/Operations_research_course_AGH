# Operations research project "Delivery of space base modules to Mars"

Our task is to deliver all modules of the space base to Mars. We have a limited number of rockets of a specific capacity
at our disposal, differing in base fuel combustion and matching the modules. The rocket's final fuel consumption depends
on the modules being carried and consists of baseline combustion and module-dependent combustion. The goal is to choose
a combination of rockets that burns as little fuel as possible.

To solve this problem we will be using the [Bees algorithm](https://en.wikipedia.org/wiki/Bees_algorithm).

## Dependencies

- Python >= 3.8

## Project structure

### src folder

Inside **src** folder there are *algorithm.py* and *model.py** files.

- **algorithm.py**
- **model.py** inside this file we define two classes Settings and Solution and several functions for solving an
  optimization problem related to the allocation of rockets and modules. The problem consists of allocating a given
  number of modules to a given number of rockets, where each rocket has a limited capacity, and the cost of transporting
  a module depends on the type of rocket used to transport it.

#### Credits

This project was created by Szymon Budziak, Alicja Hurbol, [Jakub Szymczak](https://github.com/SzymczakJ).