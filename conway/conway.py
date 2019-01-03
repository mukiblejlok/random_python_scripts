import numpy as np
import os
import time
from numbers import Number
from scipy.signal import convolve2d


class ConwayGameOfLife():
    k = np.ones((3, 3))
    k[1, 1] = 0

    def __init__(self, n, **kwargs):
        self.n = n
        self.i = 0
        self.t = 0.0
        self.X = self.initialize_X(self.n, **kwargs)

    @staticmethod
    def initialize_X(n, **kwargs):
        mode = kwargs.get('mode', 'random')
        if mode.lower() == 'random':
            coverage = kwargs.get('coverage', 0.5)
            m = n**2 * coverage
            X = np.random.randint(0, (n**2) + 1, n * n)
            X = (X.reshape(n, n) <= m).astype(int)
        else:
            raise ValueError("Unknown Mode")
        return X

    def get_neigbours(self, i, j):
        zn = np.array((-1,  0,  1, -1, 1, -1, 0, 1)) + i
        zm = np.array((-1, -1, -1,  0, 0,  1, 1, 1)) + j
        i_n = np.clip(zn, 0, self.n - 1)
        i_m = np.clip(zm, 0, self.n - 1)
        return self.X[i_n, i_m]

    def sum_of_neighbours(self, i, j):
        return np.sum(self.get_neigbours(i, j))

    @staticmethod
    def rule_of_life(cv, cn):
        '''
        cv - status of cell
        cn - sum of cell's neighbours statuses
        it can be both single value or arrays

        The rules are:
            For a space that is 'populated':
                - Each cell with one or no neighbors dies,
                  as if by solitude.
                - Each cell with four or more neighbors dies,
                  as if by overpopulation.
                - Each cell with two or three neighbors survives.
            For a space that is 'empty' or 'unpopulated'
                Each cell with three neighbors becomes populated.
        '''
        if isinstance(cv, Number) and isinstance(cn, Number):
            return int(cn == 3 or (cv == 1 and cn == 2))
        elif isinstance(cv, np.ndarray) and isinstance(cn, np.ndarray):
            return ((cn == 3) | ((cv == 1) & (cn == 2))).astype(int)

    def update(self, method='convolve'):
        self.i += 1
        start = time.time()
        if method.lower() == 'convolve':
            self.X = self.convolve_update(self.X)
        elif method.lower() == 'iter':
            self.X = self.array_update(self.X)
        else:
            raise ValueError("Unknown update method")
        end = time.time()
        self.t = end - start

    def array_update(self, X):
        Xn = np.zeros_like(X)
        for i, row in enumerate(X):
            for j, c in enumerate(row):
                cn = self.sum_of_neighbours(i, j)
                Xn[i, j] = self.rule_of_life(X[i, j], cn)
        return self.Xn

    def convolve_update(self, X):
        '''
        Calculate number of neighbours by doing convolution
        with array:   1 1 1
                     [1 0 1]
                      1 1 1
        '''
        cn = convolve2d(X, self.k, mode='same',
                        boundary='fill', fillvalue=0)
        return self.rule_of_life(X, cn)

    def print_state(self, clear=True, iteration_row=True):
        if clear:
            os.system('cls')
        if iteration_row:
            print("====\ni={:4d} t={:.6f}s\n====".format(self.i, self.t))
        state = ""
        for row in self.X:
            for c in row:
                if c == 0:
                    state += "·"
                else:
                    state += "█"
            state += "\n"
        print(state)


if __name__ == '__main__':
    # Initialization
    N = 40  # size
    s = 0.1  # sleep time [s]
    con = ConwayGameOfLife(N, coverage=0.2)
    while 1:
        try:
            # Presentation
            con.print_state()
            # Update
            con.update(method='convolve')
        except KeyboardInterrupt:
            break
