__author__ = "Luis Domingues"
__maintainer__ = "Luis Domingues"
__email__ = "luis.hmd@gmail.com"

#----------------------------------------------------------------------------------------
# Notes
#----------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
import math
import random as rand
import rcga_classes



#----------------------------------------------------------------------------------------
# OPERATORS
#----------------------------------------------------------------------------------------

# Elitism
def elitism(Pop, params, reverse=False):
    P = Pop.copy()
    elitism_params = params['elitism_params']
    best_ind_list = []
    if elitism_params['use_elitism']:
        n_best_ind = elitism_params['n_ind_elitism']
        P.sort_by_fitness(reverse=reverse)
        ind_list = P.get_individuals()
        for i in range(n_best_ind):
            best_ind_list.append(ind_list[i])
    return best_ind_list


# Selection
def tournament(Pop, params):
    rand.seed(a=Pop.get_seed())
    opt_type = params['opt_type']
    n_ind_tournament = params['selection_params']['n_ind_tournament']
    mp_fraction = params['selection_params']['mating_pool_fraction']
    mp_size = math.floor( mp_fraction*Pop.get_size() )
    mp = rcga_classes.Population(Pop.get_search_space(), seed=Pop.get_seed())

    # Fill in the mating pool
    for m in range(mp_size):
        candidates = []
        best_ind_index = None
        if opt_type == 'max':
            best_fitness = float('-inf')
        else:
            best_fitness = float('+inf')

        # Run a tournament
        for i in range(n_ind_tournament):
            ind_index = math.floor( rand.random()*Pop.get_size())
            # Make sure individual is not in the candidates for this tournament
            while ind_index in candidates:
                ind_index = math.floor(rand.random() * Pop.get_size())

            candidates.append(ind_index)
            ind_fitness = Pop.get_individual(ind_index).get_fitness()

            # Update best
            if opt_type == 'max' and ind_fitness > best_fitness:
                best_ind_index = ind_index
                best_fitness = ind_fitness
            if opt_type == 'min' and ind_fitness < best_fitness:
                best_ind_index = ind_index
                best_fitness = ind_fitness

        # Insert winner in mating pool
        ind = Pop.get_individual(best_ind_index)
        mp.insert_individual(ind.get_solution(), fitness=best_fitness)

    return mp

# Crossover


# Mutation
def polynomial_mutation(Pop, params):
    rand.seed(a=Pop.get_seed())
    p_mut = params['mutation_params']['p_mutation']
    C = params['mutation_params']['distribution_constant']
    search_space = Pop.get_search_space()
    vars_names = search_space.get_variables_names()
    Pop_new = rcga_classes.Population(Pop.get_search_space(), seed=Pop.get_seed())
    for i in Pop.get_individuals():
        solution = i.get_solution()
        mutation_occurred = False
        for v in vars_names:
            if rand.random() < p_mut:
                mutation_occurred = True
                # Mutate
                var_type = search_space.get_variable_type(v)
                if var_type == 'int' or var_type == 'float':
                    # Generate tau_k
                    r = rand.random()
                    if r < 0.5:
                        tau_k = (2.0 * r) ** (1 / (C + 1)) - 1
                    else:
                        tau_k = 1 - (2.0 * (1 - r)) ** (1 / (C + 1))
                    lb = search_space.get_variable_lbound(v)
                    ub = search_space.get_variable_ubound(v)
                    solution[v] = solution[v] + (ub - lb)*tau_k
                elif var_type == 'enumerate':
                    values = search_space.get_variable_values(v)
                    solution[v] = values[rand.randint(0, len(values)-1)]
                elif var_type == 'binary':
                    solution[v] = rand.randint(2)
                else:
                    print("Could not determine type for variable {}".format(v))
                    solution[v] = None

        if mutation_occurred:
            Pop_new.insert_individual(solution)
        else:
            Pop_new.insert_individual(solution, fitness=i.get_fitness())

    return Pop_new