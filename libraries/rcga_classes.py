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

    def get_solution(self):
        return self.solution

    def get_fitness(self):
        return self.fitness

    def update_fitness(self, new_fitness):
        self.fitness = new_fitness
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
        self.Search_space = Search_space(search_space)

    def __str__(self):
        s = "Size: {}\nSeed: {}\n".format(self.size, self.seed)
        for i in self.ind_list:
            s += i.__str__() + "\n"
        return s

    def get_seed(self):
        return self.seed

    def get_individual(self, ind_id):
        return self.ind_list[ind_id]

    def get_individuals(self):
        return self.ind_list

    def initialise(self, pop_size):
        rand.seed(a=self.seed)
        vars_names = self.Search_space.get_variables_names()
        for i in range(pop_size):
            solution = {}
            for v in vars_names:
                var_type = self.Search_space.get_variable_type(v)
                if var_type == 'int' or var_type == 'float':
                    lb = self.Search_space.get_variable_lbound(v)
                    ub = self.Search_space.get_variable_ubound(v)
                    solution[v] = lb + (ub - lb)*rand.random()
                elif var_type == 'enumerate':
                    values = self.Search_space.get_variable_values(v)
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
        return 0

    def insert_individual(self, solution):
        ind = Individual(self.size+1, solution)
        self.ind_list.append(ind)
        self.size += 1
        return 0

    def evaluate_population(self, f_model):
        self.N_failed_evals = 0
        for i in range(len(self.ind_list)):
            fitness = eval(f_model)(self.ind_list[i].get_solution())
            if fitness:
                self.ind_list[i].update_fitness(fitness)
            else:
                self.N_failed_evals += 1
        return self.N_failed_evals

#----------------------------------------------------------------------------------------
# TESTING
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass