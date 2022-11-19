# Rubik's Library

This project provides a library that supports the creation and manipulation of generalized rubiks cubes of arbitrary length and spacial dimension. The cubes are represented as numpy arrays. The library can be used to develop and test new algorithms to solve the cube, and to explore its features. A function that always finds the optimal solution to the 2x2x2 cube is provided.

This project requires two cube datasets which are available for download at [my dropbox](https://www.dropbox.com/sh/ef93m1riegor6i4/AABFlgJUDizUUU3jGxL69o-Da?dl=0).

Some essential terminology:<br />
[half turn metric](https://www.speedsolving.com/wiki/index.php/Metric#HTM)<br />
[quarter turn metric](https://www.speedsolving.com/wiki/index.php/Metric#QTM)

Class **Cube**(length=3, dim=3)<br />
Creates a cube of the specified length and spacial dimention.

**rotate**(axis, index, k=1)<br />
Rotates the cube by k quarter turns along the specified axis and index.<br />
0<=axis<dim<br />
0<=index<len

**scramble**([n]):<br />
Randomly rotates the cube n times. If no argument is passed, the cube is undergoes random rotation 10\*len\*dim times.

**is_same_as**(target):<br />
Returns True if the source cube is identical to the target cube. Returns False if the source cube is not identical to the target cube

**solved**():<br />
Returns a boolean value to indicate if the cube is in the solved position.

**ID**():<br />
Reversibly maps the cube to a string that uniquely identifies it.

**assume_ID**(ID):<br />
The cube assumes the position associated with the passed string. This is the inverse of the ID function.

**hdepth**():<br />
Returns the depth of the cube under the half turn metric. Only works for the 2x2x2 cube.

**qdepth**():<br />
Returns the depth of the cube under the quarter turn metric. Only works for the 2x2x2 cube.

**hless**():<br />
Returns the list of rotations that take the cube nearer to solution the half turn metric. Only works for the 2x2x2 cube. Each rotation takes the form (axis, index, k).

**qless**():<br />
Returns the list of rotations that take the cube nearer to solution the quarter turn metric. Only works for the 2x2x2 cube. Each rotation takes the form (axis, index, k).

**hsame**():<br />
Returns the list of rotations that take the cube to another position of the same depth under the half turn metric. Only works for the 2x2x2 cube. Each rotation takes the form (axis, index, k).

**qsame**():<br />
Returns the list of rotations that take the cube to another position of the same depth under the quarter turn metric. Only works for the 2x2x2 cube. Each rotation takes the form (axis, index, k).

**hgreater**():<br />
Returns the list of rotations that take the cube to another position of a greater depth under the half turn metric. Only works for the 2x2x2 cube. Each rotation takes the form (axis, index, k).

**hgreater**():<br />
Returns the list of rotations that take the cube to another position of a greater depth under the quarter turn metric. Only works for the 2x2x2 cube. Each rotation takes the form (axis, index, k).

**qsolve**():<br />
Returns a list of rotations (*axis, index, k*) which solve the cube under the quarter turn metric in the minimum number of moves. Only works for the 2x2x2 cube. Each rotation takes the form (axis, index, k).

**hsolve**():<br />
Returns a list of rotations (*axis, index, k*) which solve the cube under the half turn metric in the minimum number of moves. Only works for the 2x2x2 cube. Each rotation takes the form (axis, index, k).

**qsolve_to**(target):<br />
Returns a set of rotations to bring the source cube to the target cube in the minimum number of moves under the quarter turn metric. Only works for the 2x2x2 cube. Each rotation takes the form (axis, index, k).

**hsolve_to**(target):<br />
Returns a set of rotations to bring the source cube to the target cube in the minimum number of moves under the half turn metric. Only works for the 2x2x2 cube. Each rotation takes the form (axis, index, k).

**qdistance**(target):<br />
Returns the distance between the source cube and the target cube under the quarter turn metric.

**hdistance**(target):<br />
Returns the distance between the source cube and the target cube under the half turn metric.

**qrotations**(target):<br />
Returns a list of all rotations of the cube under the quarter turn metric.

**hrotations**(target):<br />
Returns a list of all rotations of the cube under the half turn metric.


The source code and readme for this project are released under licensed under [CC00](https://creativecommons.org/share-your-work/public-domain/cc0/) - No rights reserved.
