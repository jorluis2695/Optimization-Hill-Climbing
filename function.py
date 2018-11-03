import numpy as np


class UtilityFunction(object):

    values = None   # 2-D numpy array with shape (n,2). This holds the x-values and y-values.
    length = 0  # length of array

    def __init__(self,Values):
        super().__init__()

        if isinstance(Values,np.ndarray):
            self.values = Values
            self.length = Values.shape[0]
        elif isinstance(Values,str):
            self.readfromfile(Values)
            self.length = self.values.shape[0]

    # def readfromfile(self, fileName, rows_to_skip=0):
    #     file = open(fileName, 'r')
    #     self.values = np.loadtxt(file, delimiter=',', skiprows=rows_to_skip)

    def evaluate_function(self,x_value):
        # If there is more than one row (which means that self.values is a 2D array)
        if len(self.values.shape) == 2:
            try:
                # Search  x_value in the first row. If it doesn't exist in self.values it will raise an exception.
                position = np.where(self.values[:,0] == x_value)
                # Lets extract the integer reflecting the position from the tuple of arrays (?)
                row = position[0][0]
                return self.values[row, 1]
            except:
                print("The function can't be evaluated at this x_value.\n")
        else:
            try:
                # This next statemnet is just to check whether x_value exists in the 1-D array. if it does, we know where the y_value is
                position = np.where(self.values == x_value)
                #row = position[0][0]
                return self.values[1]
            except:
                print("The function can't be evaluated at this x_value. (1-D array)\n")

    def return_x_value(self,index):
        if index < 0:
            raise IndexError("Index can't be less than zero!")
        if index >= self.length:
            raise IndexError("Index can't be equal or larger than the function length!")
        return self.values[index,0]

    def return_y_value(self,index):
        if index < 0:
            raise IndexError("Index can't be less than zero!")
        if index >= self.length:
            raise IndexError("Index can't be equal or larger than the function length!")
        return self.values[index,1]

    def get_indice(self, value):
        dif = 1000000000
        indice = 0
        for i in range(0, len(self.values)):
            val = abs(self.return_x_value(i) - value)
            if val < dif:
                dif = val
                indice = i
        return indice

    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

class BackendAgnosticUtilityFunction(UtilityFunction):

    request_freq = 0
    request_weight = 0
    request_cdi = 0
    request_bdi = 0


    def __init__(self,Values, freq = 1, weight = 1, cdi = 1, bdi = 1):
        super().__init__(Values)
        if freq >0:
            self.request_freq = freq
        else:
            self.request_freq = 0
        if weight > 0:
            self.request_weight = weight
        else:
            self.request_weight = 0
        if cdi > 0:
            self.request_cdi = cdi
        else:
            self.request_cdi = 0
        if bdi > 0:
            self.request_bdi = bdi
        else:
            self.request_bdi = 0

    def output(self,index):
        if index < 0:
            raise IndexError("Index can't be less than zero!")
        if index >= self.length:
            raise IndexError("Index can't be equal or larger than the function length!")
        #tmp = self.request_freq * (1 - self.return_y_value(index))
        hi = 1 - self.return_y_value(index)
        eat = hi * self.request_cdi + (1-hi) * self.request_bdi
        Ui = -self.request_freq * eat
        tmp = self.request_weight * Ui
        # print(tmp)
        return tmp