from os import path
import numpy as np
import json

parent_dir = path.dirname(path.abspath(__file__))

matrix = np.load(path.join(parent_dir, 'data', 'matrix_71.npy'))
matrix = matrix.astype('float')

size = len(matrix)

matrix_stat = dict()
matrix_stat['sum'] = np.sum(matrix)
matrix_stat['avr'] = matrix_stat['sum'] / (size * size)
matrix_stat['sumMD'] = np.trace(matrix)
matrix_stat['avrMD'] = matrix_stat['sumMD'] / matrix.shape[0]
matrix_stat['sumSD'] = np.trace(matrix, offset=1)
matrix_stat['avrSD'] = matrix_stat['sumSD'] / matrix.shape[0]
matrix_stat['max'] = matrix.max()
matrix_stat['min'] = matrix.min()

with open(path.join(parent_dir, 'result', '1', 'matrix_stat_71.json'), 'w') as result:
    result.write(json.dumps(matrix_stat))

norm_matrix = np.ndarray((size, size), dtype=float)

for i in range(0, size):
    for j in range(0, size):
        norm_matrix[i][j] = matrix[i][j] / matrix_stat['sum']

np.save(path.join(parent_dir, 'result', '1', 'norm_matrix_71.npy'), norm_matrix)