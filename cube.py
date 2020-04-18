import numpy as np

def empty(length, dim):
    input = [(length+2) for x in range(dim)]
    return np.zeros(input, dtype=int)

def first_face(length, dim):
    if dim == 2:
        return np.array([0]+[1 for x in range(length)]+[0])
    else:
        input = np.array([first_face(length, dim-1) for x in range(length)])
        buff = np.expand_dims(empty(length, dim-2), axis=0)
        return np.vstack((buff, input, buff))

def cube_builder(length, dim):
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
    sides = [[0 for x in range(cube.shape[1])] for x in range(cube.ndim)]
    for i in range(cube.ndim):
        for j in range(cube.shape[1]):
            obj = tuple([slice(None) for x in range(i)] + [j])
            sides[i][j] = obj
    return sides

def sides(cube):
    sides = [[0 for x in range(cube.shape[1])] for x in range(cube.ndim)]
    for i in range(cube.ndim):
        for j in range(cube.shape[1]):
            obj = tuple([slice(None) for x in range(i)] + [j])
            sides[i][j] = cube[obj]
    return sides

class Cube:
    def __init__(self, length=3, dim=3):
        self.length = length
        self.dim = dim
        self.tensor = cube_builder(length, dim)
        self.sides = sides(self.tensor)
        self.side_obj = sides_obj(self.tensor)

    def rotate(self, axis, index, k=1):
        # side is an int between 1 and length
        # axes is a tuple of dimension "dim-1" containing all axes not rotated over.
        self.tensor[self.side_obj[axis][index]] = np.rot90(self.tensor[self.side_obj[axis][index]], k)
        if index == 1:
            self.tensor[self.side_obj[axis][0]] = np.rot90(self.tensor[self.side_obj[axis][0]], k)
        if index == self.length:
            self.tensor[self.side_obj[axis][self.length+1]] = np.rot90(self.tensor[self.side_obj[axis][self.length+1]], k)
    
        def scramble(self, n=None):
            if n == None:
                n = 10 * self.length * self.dim
            for x in range(n):
                axis = randint(0, self.dim - 1)
                index = randint(1, self.length)
                k = randint(1, 3)
                self.rotate(axis, index, k)
