from typing import Tuple
import numpy as np

def get_value(indexes: Tuple[int], array: np.ndarray):

    shape = array.shape
    flattened = array.reshape(-1)
    
    index = indexes[0] * shape[1] * shape[2] + indexes[1] * shape[2] + indexes[2]

    # index = 0

    # for i in range(len(shape)):
    #     add = indexes[i]
    #     for j in range(i + 1, len(shape)):
    #         add = add * shape[j]
        
    #     index = index + add

    return flattened[index]

a = np.zeros((3, 4, 2))

for i in range(3):
    for j in range(4):
        a[i, j, 0] = i * 4 + j
        a[i, j, 1] = - a[i, j, 0]

print(a[:, :, 0])
print(a[:, :, 1])

print('------------------')

print(a[0, 0, 1], get_value((0, 0, 1), a))
print(a[1, 0, 0], get_value((1, 0, 0), a))
print(a[2, 0, 0], get_value((2, 0, 0), a))

print(a[0, 0, 0], get_value((0, 0, 0), a))
print(a[1, 1, 1], get_value((1, 1, 1), a))
print(a[1, 2, 0], get_value((1, 2, 0), a))

print(a[0, 1, 0], get_value((0, 1, 0), a))
print(a[1, 1, 1], get_value((1, 1, 1), a))
print(a[1, 2, 0], get_value((1, 2, 0), a))