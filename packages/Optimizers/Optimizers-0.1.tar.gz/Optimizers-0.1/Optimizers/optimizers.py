

from Optimizers import optimize

class ECHO:
    def __init__(self, data):
        self.data = data
        self.timelimit = 60

    def solve(self):
        self.solution = optimize(self.data, self.timelimit)
        return self.solution

    def print(self):
        print("\n".join("{}:\t{}".format(k, v) for k, v in self.solution.items()))

    def plot(self):
        # TODO: draw the solution map
        print("\n".join("{}:\t{}".format(k, v) for k, v in self.solution.items()))
        
class VRPTW:
    def __init__(self, data):
        self.data = data
        self.data["optimizer"] = "VRPTW"
        self.timelimit = 60

    def parameters(self, parameters):
        self.data['parameters'] = parameters

    def solve(self):
        self.solution = optimize(self.data, self.timelimit)
        return self.solution

    def print(self):
        print("\n".join("{}:\t{}".format(k, v) for k, v in self.solution.items()))

    def plot(self):
        # TODO: draw the solution map
        print("\n".join("{}:\t{}".format(k, v) for k, v in self.solution.items()))

class CLSP:
    def __init__(self, data):
        self.data = data
        self.data["optimizer"] = "CLSP"
        self.timelimit = 60

    def parameters(self, parameters= [40, 1000, 0.000005, 6, 20]):
        self.data['parameters'] = parameters

    def solve(self):
        self.solution = optimize(self.data, self.timelimit)
        return self.solution

    def print(self):
        print("\n".join("{}:\t{}".format(k, v) for k, v in self.solution.items()))

    def plot(self):
        # TODO: draw the solution map
        print("\n".join("{}:\t{}".format(k, v) for k, v in self.solution.items()))




# import numpy as np
# import ctypes
# from ctypes import POINTER, byref, c_double, c_int, c_char_p
# import os
# import json
# from numpy.ctypeslib import ndpointer

# LIB_PATH = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'lib')
# array_double = np.ctypeslib.ndpointer(dtype=np.double)
# array_int = np.ctypeslib.ndpointer(dtype=np.uintp)
# array2D_int = ndpointer(dtype=np.uintp, ndim=1, flags='C')
# array2D_double = ndpointer(dtype=np.double, ndim=1, flags='C')
# def matrix_int(x):
#   return (x.__array_interface__['data'][0] + np.arange(x.shape[0]) * x.strides[0]).astype(np.uintp)
# def matrix_double(x):
#   return (x.__array_interface__['data'][0] + np.arange(x.shape[0]) * x.strides[0]).astype(np.double)



# def VRPTW(data, timelimit=60, parameters=[]):
#     try:
#         path_vrptw = os.path.join(LIB_PATH, 'testlib.so')
#         solver_VRPTW = ctypes.CDLL(path_vrptw).myprint
#         solver_VRPTW.argtypes = [POINTER(c_int), POINTER(c_double), ctypes.c_char_p, c_int, array_double, array_double,
#                                  array_double, array_double]
#         # solver_VRPTW.restype = c_char_p
#         _parameters = np.array(parameters,np.float64)
#         _vehicles_matrix = np.array(data['vehicles'],np.float64)
#         _nodes_matrix = np.array(data['nodes'],np.float64)
#         _distance_matrix = np.array(data['distance'],np.float64)
#         nNode = 11
#         _routes = np.arange(nNode * 2.,dtype=np.uintp).reshape((nNode, 2))

#         status = c_int()
#         obj = c_double()

#         output= ctypes.create_string_buffer(10240)

#         solver_VRPTW(byref(status), byref(obj), output, timelimit, _parameters, _vehicles_matrix, _nodes_matrix,
#                                 _distance_matrix)
#         print("here:", output.value)
#         print(status.value, obj.value, _routes);

#         solution = json.loads(output.value)

#         # solution = json.loads(
#         #     requests.put(config.server_url, data=json.dumps(req), headers={"Content-Type": "application/json"}).text)
#         return solution
#     except Exception as err:
#         return {"status": f'error loading offline optimziers {err}'}
