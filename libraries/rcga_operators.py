__author__ = "Luis Domingues"
__maintainer__ = "Luis Domingues"
__email__ = "luis.hmd@gmail.com"

#----------------------------------------------------------------------------------------
# Notes
#----------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------




#----------------------------------------------------------------------------------------
# OPERATORS
#----------------------------------------------------------------------------------------

# Elitism
def elitism(Pop, params, reverse=False):
    best_ind_list = []
    if params['use_elitism']:
        n_best_ind = params['n_ind_elitism']
        Pop.sort_by_fitness(reverse=reverse)
        ind_list = Pop.get_individuals()
        for i in range(n_best_ind):
            best_ind_list.append(ind_list[i])
    return best_ind_list


# Selection


# Crossover


# Mutation