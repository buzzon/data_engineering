import os
from os import path
import numpy as np

parent_dir = path.dirname(path.abspath(__file__))


matrix = np.load(path.join(parent_dir, 'data', 'matrix_71_2.npy'))
matrix = matrix.astype(float)

x = list()
y = list()
z = list()

filter_value = 571

for i in range(0, matrix.shape[0]):
    for j in range(0, matrix.shape[1]):
        if matrix[i][j] > filter_value:
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])

filepath = path.join(parent_dir, 'result', '2', 'points.npz')
filepathzip = path.join(parent_dir, 'result', '2', 'points_zip.npz')

np.savez(filepath, x=x, y=y, z=z)
np.savez_compressed(filepathzip, x=x, y=y, z=z)

size = os.path.getsize(filepath)
sizezip = os.path.getsize(filepathzip)

print(f"points = {size}")
print(f"points_zip = {sizezip}")
print(size / sizezip)