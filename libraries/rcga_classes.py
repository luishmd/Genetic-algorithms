__author__ = "Luis Domingues"
__maintainer__ = "Luis Domingues"
__email__ = "luis.hmd@gmail.com"

#----------------------------------------------------------------------------------------
# Notes
#----------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
import random as rand
import copy
import models
import rcga_operators as op


#----------------------------------------------------------------------------------------
# CLASSES
#----------------------------------------------------------------------------------------
class Individual(object):
    """ Creates an individual class to be used in a population """
    def __init__(self, ind_id, solution, fitness=None):
        self.id = ind_id
        self.solution = solution
        self.fitness = fitness

    def __str__(self):
        if self.fitness:
            return "Individual {} has fitness {}".format(self.id, self.fitness)
        else:
            return "Individual {} has fitness None".format(self.id)

    def copy(self):
        return copy.deepcopy(self)

    def get_solution(self):
        return self.solution

    def get_fitness(self):
        return self.fitness

    def update_fitness(self, new_fitness):
        self.fitness = new_fitness
        return 0

    def update_solution(self, new_solution, new_fitness=None):
        self.solution = new_solution
        if new_fitness:
            self.fitness = new_fitness
        else:
            self.fitness = None
        return 0


class Search_space(object):
    """ Creates a search space """
    def __init__(self, search_space):
        self.search_space = search_space

    def get_number_variables(self):
        return len(self.search_space)

    def get_variables_names(self):
        return tuple(self.search_space.keys())

    def get_variable_type(self, var):
        try:
            return self.search_space[var]["Type"]
        except KeyError:
            return None

    def get_variable_lbound(self, var):
        try:
            return self.search_space[var]["LBound"]
        except KeyError:
            return None

    def get_variable_ubound(self, var):
        try:
            return self.search_space[var]["UBound"]
        except KeyError:
            return None

    def get_variable_values(self, var):
        try:
            return self.search_space[var]["Values"]
        except KeyError:
            return None


class Population(object):
    """ Creates a population, which is a collection of individuals with extrac functionality """
    def __init__(self, search_space, seed=None):
        self.size = 0
        self.ind_list = []
        self.N_failed_evals = 0
        self.seed = seed
        self.search_space = search_space

    def __str__(self):
        s = "Size: {}\nSeed: {}\n".format(self.size, self.seed)
        for i in self.ind_list:
            s += i.__str__() + "\n"
        return s

    def copy(self):
        return copy.deepcopy(self)

    def __enforce_solution_bounds(self, solution):
        solution_bounded = {}
        vars_names = self.search_space.get_variables_names()
        for v in vars_names:
            var_type = self.search_space.get_variable_type(v)
            if var_type == 'int' or var_type == 'float':
                lb = self.search_space.get_variable_lbound(v)
                ub = self.search_space.get_variable_ubound(v)
                if (solution[v] >= lb) and (solution[v] <= ub):
                    solution_bounded[v] = solution[v]
                elif (solution[v] >= ub):
                    solution_bounded[v] = ub
                else: # solution[v] <= lb
                    solution_bounded[v] = lb
            elif var_type == 'enumerate':
                values = self.search_space.get_variable_values(v)
                if solution[v] in values:
                    solution_bounded[v] = solution[v]
                else:
                     solution_bounded[v] = values[rand.randint(len(values))]
            elif var_type == 'binary':
                if solution[v] in [0,1]:
                    solution_bounded[v] = solution[v]
                else:
                    solution_bounded[v] = rand.randint(2)
            else:
                print("Could not enforce bounds for variable {}".format(v))
        return solution_bounded

    def get_seed(self):
        return self.seed

    def get_size(self):
        return self.size

    def get_search_space(self):
        return self.search_space

    def get_individual(self, ind_id):
        return self.ind_list[ind_id]

    def get_individuals(self):
        return self.ind_list

    def initialise(self, pop_size):
        rand.seed(a=self.seed)
        vars_names = self.search_space.get_variables_names()
        for i in range(pop_size):
            solution = {}
            for v in vars_names:
                var_type = self.search_space.get_variable_type(v)
                if var_type == 'int' or var_type == 'float':
                    lb = self.search_space.get_variable_lbound(v)
                    ub = self.search_space.get_variable_ubound(v)
                    solution[v] = lb + (ub - lb)*rand.random()
                elif var_type == 'enumerate':
                    values = self.search_space.get_variable_values(v)
                    solution[v] = values[rand.randint(0, len(values)-1)]
                elif var_type == 'binary':
                    solution[v] = rand.randint(2)
                else:
                    print("Could not determine type for variable {}".format(v))
                    solution[v] = None
            self.insert_individual(solution)
        return 0

    def sort_by_fitness(self, reverse=False):
        ind_list_sorted = []
        tuple_list = []
        for i in range(self.size):
            t = (i, self.ind_list[i].get_fitness())
            tuple_list.append(t)
        tuple_list.sort(key=lambda tup: tup[1], reverse=reverse)
        for t in tuple_list:
            ind_list_sorted.append(self.ind_list[t[0]])
        self.ind_list = ind_list_sorted
        return 0

    def insert_individual(self, solution, fitness=None):
        sol = self.__enforce_solution_bounds(solution)
        ind = Individual(self.size+1, sol, fitness=fitness)
        self.ind_list.append(ind)
        self.size += 1
        return 0

    def evaluate_population(self, f_model):
        self.N_failed_evals = 0
        for i in range(len(self.ind_list)):
            if self.ind_list[i].get_fitness() == None:
                fitness = eval(f_model)(self.ind_list[i].get_solution())
                if fitness:
                    self.ind_list[i].update_fitness(fitness)
                else:
                    self.N_failed_evals += 1
        return self.N_failed_evals


class rcga(object):
    """ Creates a real-coded genetic algorithm """
    def __init__(self, search_space, params):
        self.N_gen = 0
        self.params = params
        self.search_space = Search_space(search_space)
        self.seed = params['seed']
        self.pop_size = params['population_size']
        self.max_gen = params['max_generations']
        self.model_function = params['model_function']
        if params['opt_type'] == 'min':
            self.reverse = False
        else:
            self.reverse = True

    def execute(self):

        # Get functions
        f_model = 'models.' + self.params['model_function']
        f_elitism = 'op.'+self.params['elitism_params']['elitism_function']
        f_selection = 'op.' + self.params['selection_params']['selection_function']
        f_crossover = 'op.' + self.params['crossover_params']['crossover_function']
        f_mutation = 'op.' + self.params['mutation_params']['mutation_function']

        # Initialise and evaluate population
        Pop = Population(self.search_space, seed=self.seed)
        Pop.initialise(self.pop_size)
        Pop.evaluate_population(f_model)

        # Select mating pool
        mp = eval(f_selection)(Pop, self.params)
        print(mp)

        # Apply crossover


        # Apply elitism
        elitism_ind = eval(f_elitism)(Pop, self.params, reverse=self.reverse)

        # Construct new population
        Pop_new = Pop.copy()

        # Apply mutation
        Pop_new = eval(f_mutation)(Pop_new, self.params)
        Pop_new.evaluate_population(f_model)

        # Write results



        return 0

#----------------------------------------------------------------------------------------
# TESTING
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass