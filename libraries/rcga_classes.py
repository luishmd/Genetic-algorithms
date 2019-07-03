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
import datetime
import lib_directory_ops
import lib_path_ops
import lib_file_ops
import lib_excel_ops_openpyxl as lib_excel


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
        self.N_evals = 0
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
        """
        Internal function that enforces the bounds prior to inserting an individual in the population.
        """
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

    def get_individual(self, ind_index):
        """
        Function that returns a single individual from its index in the population
        """
        return self.ind_list[ind_index]

    def get_individuals(self):
        """
        Function that returns all the individual it contains.
        """
        return self.ind_list

    def get_best_individual(self, opt_type):
        """
        Function that returns the best individual
        """
        best_ind = None
        # Determine optimisation type
        if opt_type == 'max':
            best_fitness = float('-Inf')
        else:
            best_fitness = float('+Inf')
        # Search for best individual
        for i in self.ind_list:
            fitness = i.get_fitness()
            if opt_type == 'max' and fitness > best_fitness:
                best_ind = i
            if opt_type == 'min' and fitness < best_fitness:
                best_ind = i
        return best_ind

    def initialise(self, pop_size):
        """
        Function that initialises a population of a given size
        """
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
        """
        Function that sorts a population by fitness, depending on the optimisation type (min in ascending order)
        """
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
        """
        Function that inserts an individual in the population, given a solution.
        """
        sol = self.__enforce_solution_bounds(solution)
        ind = Individual(self.size+1, sol, fitness=fitness)
        self.ind_list.append(ind)
        self.size += 1
        return 0

    def evaluate_population(self, f_model):
        """
        Function that evaluates the population
        """
        for i in range(len(self.ind_list)):
            if self.ind_list[i].get_fitness() == None:
                fitness = eval(f_model)(self.ind_list[i].get_solution())
                self.N_evals += 1
                if fitness:
                    self.ind_list[i].update_fitness(fitness)
                else:
                    self.N_failed_evals += 1
        return [self.N_evals, self.N_failed_evals]


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
        self.opt_type = params['opt_type']
        self.best_ind = None
        self.N_evals = 0
        self.N_failed_evals = 0
        self.statistics = {}
        self.write = {}
        if self.opt_type == 'min':
            self.reverse = False
        else:
            self.reverse = True

    def __create_output_dir(self):
        """
        Internal function that creates the output dir and copies the template file
        """
        # Create results directory and create output file from template
        dir_name = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        output_dir = lib_directory_ops.create_dir(self.params['Excel output dir'], dir_name)
        assert output_dir != None
        new_file = 'output_' + dir_name + '.xlsx'
        output_file = lib_path_ops.join_paths(output_dir, new_file)
        r = lib_file_ops.copy_file(self.params['Excel template file'], output_file)
        self.params['Excel output file'] = output_file
        self.write['generation row index'] = 13
        assert r != None

    def __write_parameters(self):
        """
        Internal function that writes the parameters
        """
        ws = self.wb["Parameters"]
        # Write parameters
        row_i = 4
        for param in self.params.keys():
            ws.cell(row=row_i, column=1, value=param)
            if type(self.params[param]) == type({}):
                ws.cell(row=row_i, column=2, value=str(self.params[param]))
            else:
                ws.cell(row=row_i, column=2, value=self.params[param])
            row_i += 1
        return 0

    def __write_optimal_point(self):
        """
        Internal function that writes the optimal point
        """
        ws = self.wb["Optimisation"]
        if self.params['write_to_console']:
            print("\nOptimal point:")
        # Write optimal point
        col_i = 2
        for v in self.search_space.get_variables_names():
            ws.cell(row=5, column=col_i, value=v)
            ws.cell(row=6, column=col_i, value=self.best_ind.get_solution()[v])
            if self.params['write_to_console']:
                s = '{}: {}'.format(v, self.best_ind.get_solution()[v])
                print(s)
            col_i += 1
        return 0

    def __write_generation(self):
        """
        Internal function that writes the generation results
        """
        ws = self.wb["Optimisation"]
        # Write variables names
        col_i = 3
        for v in self.search_space.get_variables_names():
            ws.cell(row=12, column=col_i, value=v)
            col_i += 1
        # Write generation info
        row_i = self.write['generation row index']
        ws.cell(row=row_i, column=1, value=self.N_gen)
        ws.cell(row=row_i, column=2, value=self.best_ind.get_fitness())
        col_i = 3
        for v in self.search_space.get_variables_names():
            ws.cell(row=row_i, column=col_i, value=self.best_ind.get_solution()[v])
            col_i += 1
        self.write['generation row index'] += 1

        # Write to console
        if self.params['write_to_console']:
            s = "\t{}\t{}".format(self.N_gen, self.best_ind.get_fitness())
            print(s)
        return 0

    def __write_statistics(self):
        """
        Internal function that writes the statistics
        """
        ws = self.wb["Statistics"]
        # Write statistics
        ws.cell(row=3, column=2, value=self.statistics['N_failed_evals'])
        ws.cell(row=4, column=2, value=self.statistics['N_evals'])
        return 0

    def execute(self):
        """
        Main function of the class, as it runs the rcga algorithm.
        """

        # Get functions
        f_model = 'models.' + self.params['model_function']
        f_elitism = 'op.'+self.params['elitism_params']['elitism_function']
        f_selection = 'op.' + self.params['selection_params']['selection_function']
        f_crossover = 'op.' + self.params['crossover_params']['crossover_function']
        f_mutation = 'op.' + self.params['mutation_params']['mutation_function']

        # Initialise and evaluate population
        Pop = Population(self.search_space, seed=self.seed)
        Pop.initialise(self.pop_size)
        N_evals, N_failed_evals = Pop.evaluate_population(f_model)
        self.best_ind = Pop.get_best_individual(self.opt_type)

        # Statistics
        self.statistics['N_evals'] = N_evals
        self.statistics['N_failed_evals'] = N_failed_evals

        # Create output directory and files
        self.__create_output_dir()
        self.wb = lib_excel.open_workbook(self.params['Excel output file'])

        # Write initial results
        if self.params['write_to_console']:
            print("\nGen.\tFitness")
        self.__write_parameters()
        self.__write_generation()

        # Determine next generation
        while self.N_gen < self.max_gen:
            # Select mating pool
            mating_pop = eval(f_selection)(Pop, self.params)

            # Apply crossover
            crossed_pop = eval(f_crossover)(mating_pop, self.params)

            # Apply mutation
            mut_pop = eval(f_mutation)(crossed_pop, self.params)

            # Apply elitism
            elitism_ind_list = eval(f_elitism)(Pop, self.params, reverse=self.reverse)

            # Build new population
            del Pop
            Pop = Population(self.search_space, seed=self.seed)
            for i in elitism_ind_list:
                Pop.insert_individual(i.get_solution(), fitness=i.get_fitness())
            for i in mut_pop.get_individuals():
                if Pop.get_size() < self.pop_size:
                    Pop.insert_individual(i.get_solution())
            N_evals, N_failed_evals = Pop.evaluate_population(f_model)
            self.best_ind = Pop.get_best_individual(self.opt_type)

            # Increment generation
            self.N_gen += 1

            # Statistics
            self.statistics['N_evals'] += N_evals
            self.statistics['N_failed_evals'] += N_failed_evals

            # Write results
            self.__write_generation()

        # Write optimal results and statistics
        self.__write_optimal_point()
        self.__write_statistics()

        # Close necessary files
        lib_excel.save_workbook(self.wb, self.params['Excel output file'])
        self.wb.close()

        return self.best_ind

#----------------------------------------------------------------------------------------
# TESTING
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass