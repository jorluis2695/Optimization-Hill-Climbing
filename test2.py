import numpy as np
from function import UtilityFunction, BackendAgnosticUtilityFunction
from hillClimb import *
from collections import OrderedDict
import json
import time


def getConf(num):
    with open('conf/conf' + str(num) + '.json', 'r') as fp:
        event = json.load(fp)


    MRCs = event['mrc']
    memoriaTotal = event['totalMemory']
    frequency = event['frequency']
    pesos = event['weights']
    memoriaMinima = event['minimumMemory']
    cdi = event['cdi']
    bdi = event['bdi']
    #
    # MRC_curves = []
    # print("Total memory: %s"%(tm))
    # for e in names:
    #     file = open(e, 'r')
    #     tmp_array = np.loadtxt(file, delimiter=',')
    #     MRC_curves.append(tmp_array)
    #     print(tmp_array)
    MRC_curves = []
    for e in MRCs:
        tmp_array = np.array(e)
        #print(tmp_array)
        MRC_curves.append(tmp_array)
    #print(MRC_curves)


    return MRC_curves, memoriaTotal, frequency, pesos, memoriaMinima, cdi, bdi

cant = 1

c17 = (np.zeros(cant)+17).tolist()
c19 = (np.zeros(cant)+19).tolist()
c4 = (np.zeros(cant)+4).tolist()
c7 = (np.zeros(cant)+7).tolist()
c5 = (np.zeros(cant)+5).tolist()
c6 = (np.zeros(cant)+6).tolist()
c22 = (np.zeros(cant)+22).tolist()
c23 = (np.zeros(cant)+23).tolist()
c2 = (np.zeros(cant)+2).tolist()
c9 = (np.zeros(cant)+9).tolist()
c50 = (np.zeros(cant)+50).tolist()
c51 = (np.zeros(cant)+51).tolist()
c52 = (np.zeros(cant)+52).tolist()
c53 = (np.zeros(cant)+53).tolist()
c54 = (np.zeros(cant)+54).tolist()
c55 = (np.zeros(cant)+55).tolist()
c56 = (np.zeros(cant)+56).tolist()
c57 = (np.zeros(cant)+57).tolist()

fun = []
for i in range (1, 21):
    fun = fun + (np.zeros(cant)+i).tolist()



# fun = [17, 17, 17, 17, 17, 17, 19, 19, 19, 19, 19, 19,
#        4, 4, 4, 4, 4, 4, 7, 7, 7, 7, 7, 7,
#        5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6,
#        22, 22, 22, 22, 22, 22, 23, 23, 23, 23, 23, 23,
#        2, 2, 2, 2, 2, 2, 9, 9, 9, 9, 9, 9]

fun = c2
# fun = c17 + c19 + c4 + c7 + c5 + c6
# #fun = c50 + c51 + c52 + c53 + c54 +c55 +c56 +c57
# fun = c4 + c7

for i in fun:
    i = int(i)
    try:
        MRC_files, memoriaTotal, frequency, pesos, memoriaMinima, cdi, bdi = getConf(i)
        ti = time.time()
        # MRCs = []
        c = 0   #este será usado como el Id de la aplicación

        # print(MRC_files)
        solver = HillClimbingSolver(memoriaTotal)

        for e in MRC_files:

            Ufunction = BackendAgnosticUtilityFunction(e, frequency[c], pesos[c], cdi[c], bdi[c])
            solver.add_function(Ufunction, c, memoriaMinima[c])

            c += 1

        #indices = solver.get_indices()
        print("Solver!!!")
        # solution is a list of tuples with the structure: (id_of_instance, index)
        #print(solver.get_x_values(solver.search_max()))
        solution = solver.search_max_with_ids()
        tf = time.time()
        #Indeces for optimized values
        indeces = [x[1] for x in solution]
        # Here we get the actual number of blocks for each instance
        Optimized_blocks =  solver.get_x_values(indeces)
        #Optimized_blocks2 = solver.get_x_values(indices)

        # solver.get_index(memoriaTotal/2))
        print("Solved!!")
        print("Block allocation: " + str(Optimized_blocks))
        #print("Block allocation: " + str(Optimized_blocks2))
        func = str(solver.evaluate_list(indeces))
        #func2 = str(solver.evaluate_list(indices))
        print("Value of sumation function: " + str(solver.evaluate_list(indeces)))
        #print("Value of sumation function: " + str(solver.evaluate_list(indices)))

        #print("Value of sumation function: " + str(solver.evaluate()))
        print("Total Blocks used = %d" % ( sum( Optimized_blocks ) ))
        print("tiempo:  %f segundos" % (tf-ti))

        percent = str(sum(Optimized_blocks) / memoriaTotal)

        res = str(i)+','+str(tf-ti) + ',' + str(percent)+ ',' + func
        for j in Optimized_blocks:
            res = res + ',' + str(j)
        with open('Tests.txt', 'a') as fp:
            fp.write(res)
            fp.write('\n')
        #func = str(solver.evaluate_list(indices))
        res = str(i) + ',' + func
        for j in Optimized_blocks:
            res = res + ',' + str(j)
        # with open('respt1.txt', 'a') as fp:
        #     fp.write(res)
        #     fp.write('\n')

    except:
        continue