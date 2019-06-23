# Background
Implement an easy to use real-coded genetic algorithm (rcga) library, that is both easy to use and to customise. 


# Description
A real coded-genetic algorithm is a stochastic optimisation technique that can be used in a wide range of applications, from the design of engineering equipment to the determination of optimal parameters of machine learning algorthms.

The current library has the following features:
1. Ability to easily specify a search space from a text file 
2. Ability to easily specify parameters via a text file 
3. Different operators for selection, crossover and mutation and ability to extend them
4. Can write the results to an excel file, including statistics and the set of parameters used, without overwritting previous executions


## Output
Excel file with optimal point and evolution of population fitness with generations. The excel file where results are stored is copied from a defined template (set in inputs.yaml), to a subdirectory in 'outputs/'. The current date_time is used to generate the name of the subdirectory and output file. This prevents accidental overwriting.

## Input data ( See file 'inputs.yaml')
1. Search space

    User-defined decision variables, including lower and upper bounds, as well as the variable type. Types supported are: float, int, enumerate and binary.

2. Main parameters
    - *opt_type*: type of optimisation -- Possible values: min / max --
    - *seed*: seed number to use when generating random numbers -- Possible values: int / None --
    - *model_function*: name of function to be optimised -- Possible values: str --
    - *population_size*: size of the population -- Possible values: positive int --
    - *max_generations*: maximum number of generations to be executed -- Possible values: positive int --
    - *elitism_params*: Elitism. Maps to parameters below.
    - *selection_params: Selection. Maps to parameters below.
    - *crossover_params: Crossover. Maps to parameters below.
    - *mutation_params: Mutation. Maps to parameters below.
    - *output_template*: name of the excel template for results -- Possible values: str --
    - *write_to_console*: determines whether results are written to the console or not -- Possible values: True / False --


3. Elitism
    - *use_elitism*: decides whether elitism is used or not -- Possible values: True / False --
    - *elitism_function*: name of elitism function used -- Possible values: str --
    - *n_ind_elitism*: number of individuals maintained from one generation to the next -- Possible values: positive int --

4. Selection
    - *selection_function*: name of selection function used -- Possible values: str --
    - *n_ind_tournament*: number of individuals in tournament -- Possible values: int --
    - *mating_pool_fraction*: determines size of mating pool (fraction of population size) -- Possible values: float in interval [0, 1] --

5. Crossover
    - *crossover_function*: name of crossover function used -- Possible values: str --
    - *alpha*: parameter that determines new crossover offspring -- Possible values: float --
    - *p_crossover*: probability of crossover -- Possible values: float in interval [0, 1 --

6. Mutation
    - *mutation_function*: name of mutation function used -- Possible values: str --
    - *distribution_constant*: constant in polynomial mutation -- Possible values: float --
    - *p_mutation*: probability of mutation -- Possible values: float in interval [0, 1] -- 
	

# Operators implemented

- Tournament selection
- Blend-alpha crossover
- Polynomial mutation
- Elitism
	
	
# Technologies used
Python3 including the libraries:

	- math
	- os
	- os.path
	- datetime
	- openpyxl
	- sys
	- copy
	- random


# Status
This work is still in development.


# Known issues


# Future enhancements
1. Add sql connectivity
2. Add more operators
3. Add more statistics (especially on operator performance)


# How to use it
1. Open *ga_main.py* and run it.


# How to customise it to your needs
1. Define a function in *model/models.py* and set model name in input parameters

2. Define a search space in the inputs file. This corresponds to the set of decision variables

3. Open *ga_main.py* and run it.