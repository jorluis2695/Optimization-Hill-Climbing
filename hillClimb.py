from collections import OrderedDict
import itertools
import random
import numpy as np

class HillClimbingSolver(object):

    utilityFunctions = OrderedDict()
    max_memory = 0
    total_memory = 0
    step = 500
    state = None # Could be either "Max" or "Min"

    def __init__(self, max_memory):
        super().__init__()
        self.max_memory = max_memory
        self.utilityFunctions.clear()


    def add_function(self, function, id, min_memory = 0):
        tmp = {}
        index = 0
        tmp["function"] = function
        tmp["Min_memory"] = min_memory
        if self.total_memory + min_memory > self.max_memory:
            raise Exception("Problems with max memory and the minimum memories of the functions")
        self.total_memory += min_memory
        self.utilityFunctions[id] = tmp

        while function.return_x_value(index) < min_memory:
            index += 1
            if index > function.length -1:
                raise Exception("The value of min_memory given doesn't exist in this function")
        x = random.randint(index, int(function.length/4))
        # print(x)
        tmp["index"] = x

    def evaluate(self):
        sum = 0
        i = 0
        for e in self.utilityFunctions:
            i+=1
            index = self.utilityFunctions[e]['index']
            eval = self.utilityFunctions[e]['function'].output(index)
            sum += eval

        return sum

    # Evaluate the sumation of the functions at the given indeces
    def evaluate_list(self, index_list):
        if len(index_list) != len(self.utilityFunctions):
            raise IndexError("Number of values in index_list is not equals to the number of utilityFunctions.")
        sum = 0
        i = 0
        for e in self.utilityFunctions:
            index = index_list[i]
            i+=1
            eval = self.utilityFunctions[e]['function'].output(index)
            sum += eval

        return sum

    def get_Neighbor_nodes(self,index_list):

        index_combination_list = []

        for e in index_list:
            a1 = random.randint(1, self.step)
            a2 = random.randint(1, self.step)

            #a1 = a2 = random.randint(1, step)

            # a1 = a2 = 1

            #print(str(a1) + ' ---- ' + str(a2))
            tmp_list=[e-a1,e,e+a2]
            #print("Neighbor nodes:" + str(tmp_list) )
            index_combination_list.append(tmp_list)

        permuted_indeces = itertools.product(*index_combination_list)
        #print(permuted_indeces)
        return permuted_indeces

    # Given a list of indeces, get the x_values corresponding to those indices
    def get_x_values(self, index_list):
        if len(index_list) != len(self.utilityFunctions):
            raise IndexError("Number of values in index_list is not equals to the number of utilityFunctions.")
        i = 0
        list = []
        for e in self.utilityFunctions:
            index = index_list[i]
            i+=1
            list.append(self.utilityFunctions[e]['function'].return_x_value(index))

        return list

    def get_indices(self):
        list = []
        n = len(self.utilityFunctions)
        for e in self.utilityFunctions:
            list.append(self.utilityFunctions[e]['function'].get_indice(self.max_memory/len(self.utilityFunctions)))
        return  list


    def set_indeces(self, index_list):
        if len(index_list) != len(self.utilityFunctions):
            raise IndexError("Number of values in index_list is not equals to the number of utilityFunctions.")

        for i in range(len(self.utilityFunctions)):
            index = index_list[i]
            length = self.utilityFunctions[i]["function"].length
            if index >= length or index < 0:
                raise IndexError("Index out of bounds.")

            self.utilityFunctions[i]["index"] = index

        return
    # Search the max value of the summation of the functions
    def search_max(self):
        # get candidate values
        current_indeces = []
        for v in self.utilityFunctions.values():
            current_indeces.append(v["index"])
        current_value = self.evaluate_list(current_indeces)
        # print("Starting indeces:")
        # print(current_indeces)
        # print("\n\n\n")
        #neighbors = self.get_Neighbor_nodes(current_indeces)
        changed = True
        while changed:
            neighbors = self.get_Neighbor_nodes(current_indeces)
            changed = False
            #print("Current value: " + str(current_value))
            for e in neighbors:
                #print(e)

                try:
                    #print("Indeces:")
                    #print(e)
                    value = self.evaluate_list(e)
                    #print("Value:")
                    #print(value)
                    if value > current_value and not sum(self.get_x_values(e))>self.max_memory:
                        current_value = value
                        current_indeces = e
                        changed = True
                        #print("Highest Value")
                        #print(value)
                        #print("Chosen indeces:")
                        #print(current_indeces)
                        #print(e)
                        #print("\n")
                except:
                    #print("PING")
                    continue
                #sleep(2)
            #print("##################3\n\n")
        return current_indeces
    # Same as search_max() with the difference that it returns a list of tuples with ( id, index) instead of a list of indeces
    def search_max_with_ids(self):
        # get candidate values
        current_indeces = []
        for v in self.utilityFunctions.values():
            current_indeces.append(v["index"])
        current_value = self.evaluate_list(current_indeces)
        # print("Starting indeces:")
        # print(current_indeces)
        # print("\n\n\n")
        #neighbors = self.get_Neighbor_nodes(current_indeces)
        c = 0
        changed = True
        while changed:
            neighbors = self.get_Neighbor_nodes(current_indeces)
            changed = False
            #print("Current value: " + str(current_value))
            for e in neighbors:
                # print(e)

                try:
                    # print("Indeces:")
                    # print(e)
                    value = self.evaluate_list(e)
                    # print("Value:")
                    # print(value)
                    if value > current_value and not sum(self.get_x_values(e))>self.max_memory:
                        current_value = value
                        current_indeces = e
                        changed = True
                        # print("Highest Value")
                        # print(value)
                        # print("Chosen indeces:")
                        # print(current_indeces)
                        # print(e)
                        # print("\n")
                except:
                    #print("PING")
                    continue
                #sleep(2)
            #print("##################3\n\n")
            if changed == False:
                # print("CCCC")
                # print(self.step)
                self.step = random.randint(500, 700)
                if c < 50 :
                    c += 1
                    changed = True
            else:
                # self.step = 100 - c*10 + 1
                self.step = 500 - c*10 + 1
                # print(self.step)
            # if c > 0:
            #     print("XXX")
        i=0
        list = []
        # Tuple here are ( id , index, size) where index is given as a result of the optimization
        for e in self.utilityFunctions:
            tuple = (e, current_indeces[i], self.utilityFunctions[e]["function"].return_x_value(current_indeces[i]))
            list.append(tuple)
            i+=1

        return list
