import numpy as np
from random import randint, shuffle, choice
import pickle
from collections import Counter

with open('datas/h_2x2x2.pkl', 'rb') as half_dic:
    #This dictionary maps a 2x2x2 cube's ID to the number of moves requred to solve it under the half turn metric.
    #File at https://www.dropbox.com/sh/ef93m1riegor6i4/AABFlgJUDizUUU3jGxL69o-Da?dl=0
    h_dic = pickle.load(half_dic)

with open('datas/q_2x2x2.pkl', 'rb') as quarter_dic:
    #This dictionary maps a 2x2x2 cube's ID to the number of moves requred to solve it under the quarter turn metric.
    #File at https://www.dropbox.com/sh/ef93m1riegor6i4/AABFlgJUDizUUU3jGxL69o-Da?dl=0
    q_dic = pickle.load(quarter_dic)

def cube_builder(length, dim):
    #Returns a rubiks cube or arbitrary length and dimension.
    def empty(length, dim):
        shape = [(length+2) for x in range(dim)]
        return np.zeros(shape, dtype=int)

    def first_face(length, dim):
        if dim == 2:
            return np.array([0]+[1 for x in range(length)]+[0])
        else:
            input = np.array([first_face(length, dim-1) for x in range(length)])
            buff = np.expand_dims(empty(length, dim-2), axis=0)
            return np.vstack((buff, input, buff))

    first = np.expand_dims(first_face(length, dim), axis=0)
    blank = empty(length, dim - 1)
    input = np.array([blank for x in range(length +1)])
    cubeonius = np.vstack((first, input))
    hypercube = cubeonius * 0
    for n in range(dim):
        new_face = np.swapaxes(cubeonius, 0, n)
        hypercube = np.add(hypercube, (n+1)*new_face)
        hypercube = np.add(hypercube, (dim+n+1)*np.flip(new_face))
    return hypercube

def sides_obj(cube):
    #Returns a list of slice objects. Sides[i][j] represents the (rotatable) unit of the cube with axis i, index j.
    sides = [[0 for _ in range(cube.shape[1])] for _ in range(cube.ndim)]
    for i in range(cube.ndim):
        for j in range(cube.shape[1]):
            obj = tuple([slice(None) for _ in range(i)] + [j])
            sides[i][j] = obj
    return sides

class Cube:
    def __init__(self, length=3, dim=3):
        self.length = length
        self.dim = dim
        self.cube = cube_builder(length, dim)
        self.init = self.cube.copy() #Don't ever change init or things break
        self.init.setflags(write=False)
        self.side_obj = sides_obj(self.cube)
        self.shape = tuple([self.length+2 for _ in range(self.dim)])
        self.nonzero = np.nonzero(self.cube)
        self.qrotations = self.qrotations()
        self.hrotations = self.hrotations()

    def slices(self):
        #Returns a list of all rotatable slices of a cube.
        slices = [[0 for _ in range(self.length)] for _ in range(self.dim)]
        for i in range(self.dim):
            for j in range(1, self.length+1):
                obj = tuple([slice(None) for _ in range(i)] + [j])
                slices[i][j-1] = self.cube[obj]
                if j == 1:
                    obj0 = tuple([slice(None) for _ in range(i)] +[0])
                    slices[i][j-1] = np.array([self.cube[obj0], self.cube[obj]])
                if j == self.length:
                    objl = tuple([slice(None) for _ in range(i)] + [self.length+1])
                    slices[i][j-1] = np.array([self.cube[obj], self.cube[objl]])

        slices = [arr for sublist in slices for arr in sublist]
        return slices

    def rotate(self, axis, index, k=1):
        #Rotates self.cube in place
        if index == 1:
            self.cube[self.side_obj[axis][index]] = np.rot90(self.cube[self.side_obj[axis][index]], k)
            self.cube[self.side_obj[axis][0]] = np.rot90(self.cube[self.side_obj[axis][0]], k)
        elif index != self.length:
            self.cube[self.side_obj[axis][index]] = np.rot90(self.cube[self.side_obj[axis][index]], k)
        if index == self.length:
            for n in range(self.length):
                self.cube[self.side_obj[axis][n]] = np.rot90(self.cube[self.side_obj[axis][n]], -k)

    def scramble(self, n=None):
        #Just one application of this method should thoughoughly scramble any cube
        if n == None:
            n = 10 * self.length * self.dim
        for x in range(n):
            axis = randint(0, self.dim - 1)
            index = randint(1, self.length)
            k = randint(1, 3)
            self.rotate(axis, index, k)

    def is_same_as(self, target):
        return (self.cube[self.nonzero] == target[self.nonzero]).all()

    def solved(self):
        #Checks if the cube is solved
        if self.is_same_as(self.init):
            return True
        else:
            return False

    def ID(self):
        #Hashes the cube
        string = ''
        val_len = int(2*self.dim/5)
        for value in self.cube[self.nonzero]:
            new_val = str(value).zfill(val_len)
            string += new_val
        return string

    def assume_ID(self, ID):
        #self.cube goes to value of ID
        val_len = int(2*self.dim/5)
        num_stickers = int(len(ID)/val_len)
        iterable = (ID[val_len*x: val_len*(x+1)] for x in range(num_stickers))
        new_cube = np.fromiter(iterable, dtype=int, count=num_stickers)
        self.cube[self.nonzero] = new_cube

    def one_hot(self): 
        #Returns a one-hot encoding of self.cube to_one_hot = {}. Zeros are encoded by all-zero arrays and integers are 1-indexed.
        rcolors = 2*self.dim+1
        to_one_hot = {}
        for n in range(rcolors):
            to_one_hot[n] = np.fromiter((0 if x is not n-1 else 1 for x in range(rcolors-1)), int, rcolors-1)
        one_hot = np.array([to_one_hot[x] for x in self.cube.flatten()]) #try to increase the efficiancy of this line
        shape = list(self.shape) + [2*self.dim]
        return np.reshape(one_hot, shape)

    def sequential(self):
        #Returns a cube with non-zero elements sequential. May be useful later.
        save = self.cube.copy()
        self.cube[self.nonzero] = [x for x in range(len(self.cube[nonzero]))]
        result = self.cube.copy()
        self.cube = save
        return result

    def hdepth(self):
        #returns cube depth under the half turn metric
        if self.length == 2 and self.dim == 3:
            return h_dic[self.ID()]
        else:
            raise Exception('depth method is only available for 2x2x2 cubes')

    def qdepth(self):
        #returns cube depth under the quarter turn metric
        if self.length == 2 and self.dim == 3:
            return q_dic[self.ID()]
        else:
            raise Exception('depth method is only available for 2x2x2 cubes')

    def hless(self):
        #returns the list of rotations that decrease cube depth under the half turn metric 
        depth = self.hdepth()
        result = []
        if self.length == 2 and self.dim == 3:
            for axis in range(self.dim):
                for index in [1]: #Only the first index needs to be checked due to symetry in the 2x2x2 case
                    for k in range(1, 4):
                        self.rotate(axis, index, k=1)
                        if self.hdepth() == depth - 1:
                            result.append((axis, index, k))
                        if k == 3:
                            self.rotate(axis, index, k=1)
            return result

        else:
            raise Exception('depth method is only available for 2x2x2 cubes')

    def hsame(self):
        #returns the list of rotations where cube depth stays the same under the half turn metric 
        depth = self.hdepth()
        result = []
        if self.length == 2 and self.dim == 3:
            for axis in range(self.dim):
                for index in [1]: #Only the first index needs to be checked due to symetry in the 2x2x2 case
                    for k in range(1, 4):
                        self.rotate(axis, index, k=1)
                        if self.hdepth() == depth:
                            result.append((axis, index, k))
                        if k == 3:
                            self.rotate(axis, index, k=1)
            return result

        else:
            raise Exception('depth method is only available for 2x2x2 cubes')

    def hgreater(self):
        #returns the list of rotations that increase cube depth under the half turn metric 
        depth = self.hdepth()
        result = []
        if self.length == 2 and self.dim == 3:
            for axis in range(self.dim):
                for index in [1]: #Only the first index needs to be checked due to symetry in the 2x2x2 case
                    for k in range(1, 4):
                        self.rotate(axis, index, k=1)
                        if self.hdepth() == depth + 1:
                            result.append((axis, index, k))
                        if k == 3:
                            self.rotate(axis, index, k=1)
            return result

        else:
            raise Exception('depth method is only available for 2x2x2 cubes')

    def qless(self):
        #returns the list of rotations that decrease cube depth under the quarter turn metric 
        depth = self.qdepth()
        result = []
        if self.length == 2 and self.dim == 3:
            for axis in range(self.dim):
                for index in [1]: #Only the first index needs to be checked due to symetry in the 2x2x2 case
                    for k in (1, -1):
                        if k == 1:
                            self.rotate(axis, index, 1)
                        if k == -1:
                            self.rotate(axis, index, -2) #must compinsate for offset caused by first rotation
                        if self.qdepth() == depth - 1:
                            result.append((axis, index, k))
                        if k == -1:
                            self.rotate(axis, index, k=1) #return cube to original state
            return result

        else:
            raise Exception('depth method is only available for 2x2x2 cubes')

    def qsame(self):
        #returns the list of rotations of rotations where cube depth stays the same under the quarter turn metric 
        depth = self.qdepth()
        result = []
        if self.length == 2 and self.dim == 3:
            for axis in range(self.dim):
                for index in [1]: #Only the first index needs to be checked due to symetry in the 2x2x2 case
                    for k in (1, -1):
                        if k == 1:
                            self.rotate(axis, index, 1)
                        if k == -1:
                            self.rotate(axis, index, -2) #must compinsate for offset caused by first rotation
                        if self.qdepth() == depth:
                            result.append((axis, index, k))
                        if k == -1:
                            self.rotate(axis, index, k=1) #return cube to original state
            return result

        else:
            raise Exception('depth method is only available for 2x2x2 cubes')

    def qgreater(self):
        #returns the list of rotations of rotations that increase cube depth under the quarter turn metric 
        depth = self.qdepth()
        result = []
        if self.length == 2 and self.dim == 3:
            for axis in range(self.dim):
                for index in [1]: #Only the first index needs to be checked due to symetry in the 2x2x2 case
                    for k in (1, -1):
                        if k == 1:
                            self.rotate(axis, index, 1)
                        if k == -1:
                            self.rotate(axis, index, -2) #must compinsate for offset caused by first rotation
                        if self.qdepth() == depth + 1:
                            result.append((axis, index, k))
                        if k == -1:
                            self.rotate(axis, index, k=1) #return cube to original state
            return result

        else:
            raise Exception('depth method is only available for 2x2x2 cubes')

    def q_num_solutions(self):
        #Returns the number of paths of length self.qdepth() between self.cube and self.init
        if self.length == 2 and self.dim == 3:
            save = self.cube.copy()
            ID = self.ID()
            counters = [Counter(), Counter([ID])]
            while not self.solved():
                counters[0] = counters[1].copy()
                counters[1].clear()
                for ID in counters[0].keys():
                    self.assume_ID(ID)
                    count = counters[0][ID]
                    rotations = self.qless()
                    for rotation in rotations:
                        axis, index, k = rotation
                        self.rotate(axis, index, k)
                        new_ID = self.ID()
                        counters[1][new_ID] += count
                        self.rotate(axis, index, -k)
            self.cube = save 
            return sum(counters[0].values())

        else:
            raise Exception('This method is only available for 2x2x2 cubes')

    def h_num_solutions(self):
        #Returns the number of paths of length self.hdepth() between self.cube and self.init
        if self.length == 2 and self.dim == 3:
            save = self.cube.copy()
            ID = self.ID()
            counters = [Counter(), Counter([ID])]
            while not self.solved():
                counters[0] = counters[1].copy()
                counters[1].clear()
                for ID in counters[0].keys():
                    self.assume_ID(ID)
                    rotations = self.hless()
                    for rotation in rotations:
                        axis, index, k = rotation
                        self.rotate(axis, index, k)
                        new_ID = self.ID()
                        counters[1][new_ID] += counters[0][ID]
                        self.rotate(axis, index, -k) #return cube to original positions
            self.cube = save
            return sum(counters[0].values())

        else:
            raise Exception('This method is only available for 2x2x2 cubes')

    def q_simple_solver(self):
        #Returns a minimal length list of rotations to solve any 2x2x2 cube in the quarter turn metric
        if self.length == 2 and self.dim == 3:
            save = self.cube.copy()
            solution = []
            for _ in range(self.qdepth()):
                new_move = choice(self.qless())
                solution.append(new_move)
                axis, index, k = new_move
                self.rotate(axis, index, k)
            self.cube = save
            return solution

        else:
            raise Exception('This method is only available for 2x2x2 cubes')

    def h_simple_solver(self):
        #Returns a minimal length list of rotations to solve any 2x2x2 cube in the half turn metric
        if self.length == 2 and self.dim == 3:
            save = self.cube.copy()
            solution = []
            for _ in range(self.hdepth()):
                new_move = choice(self.hless())
                solution.append(new_move)
                axis, index, k = new_move
                self.rotate(axis, index, k)
            self.cube = save
            return solution

        else:
            raise Exception('This method is only available for 2x2x2 cubes')

    def qsolve(self):
        #solves the given cube in the quarter turn metric with the best available algorithm
        if self.length == 2 and self.dim == 3:
            return self.q_simple_solver()
        else:
            raise Exception('No method is curruntly available to solve a cube of this shape')

    def hsolve(self):
        #solves the given cube in the half turn metric with the best available algorithm
        if self.length == 2 and self.dim == 3:
            return self.h_simple_solver()
        else:
            raise Exception('No method is curruntly available to solve a cube of this shape')

    def hsolve_to(self, target):
        #returns a set of rotations to bring target to self.cube
        save = self.cube.copy()
        T1 = self.hsolve()
        self.cube = target.copy()
        T2 = self.hsolve()
        T2.reverse()
        for count, rotation in enumerate(T2):
            axis, index, k = rotation
            T2[count] = (axis, index, -k)

        self.cube = self.init.copy()
        for rotation in T1:
            axis, index, k = rotation
            self.rotate(axis, index, k)
        for rotation in T2:
            axis, index, k = rotation
            self.rotate(axis, index, k)
        T3 = self.hsolve()
        self.cube = save
        return T3

    def qsolve_to(self, target):
        #returns a set of rotations to bring target to self.cube
        save = self.cube.copy()
        T1 = self.qsolve()
        self.cube = target.copy()
        T2 = self.qsolve()
        T2.reverse()
        for count, rotation in enumerate(T2):
            axis, index, k = rotation
            T2[count] = (axis, index, -k)

        self.cube = self.init.copy()
        for rotation in T1:
            axis, index, k = rotation
            self.rotate(axis, index, k)
        for rotation in T2:
            axis, index, k = rotation
            self.rotate(axis, index, k)
        T3 = self.qsolve()
        self.cube = save
        return T3

    def hdistance(self, target):
        return len(self.hsolve_to(target))

    def qdistance(self, target):
        return len(self.qsolve_to(target))

    def distance(self, target):
        return len(self.hsolve_to(target))

    def solve_to(self, target):
        return self.hsolve_to(target)

    def qrotations(self):
        #A set containing all rotations under the quarter turn metric
        result = []
        for axis in range(self.dim):
            for index in range(1, self.length+1):
                for k in (-1, 1):
                    result.append((axis, index, k))
        return result

    def hrotations(self):
        #A set containing all rotations under the half turn metric.
        result = []
        for axis in range(self.dim):
            for index in range(1, self.length+1):
                for k in range(1, 4):
                    result.append((axis, index, k))
        return result
