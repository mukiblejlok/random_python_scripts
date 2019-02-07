import random
import matplotlib.pyplot as plt


def full_quicksort(L):
    return quicksort(L, 0, len(L) - 1)

def quicksort(L, lo, hi):
    if lo < hi:
        p = partition(L, lo, hi)
        quicksort(L, lo, p - 1)
        quicksort(L, p + 1, hi)
    return L

def partition(L, lo, hi):
    p = L[hi]
    i = lo
    for j in range(lo, hi):
        if L[j] < p:
            L[j], L[i] = L[i], L[j]
            i += 1
    L[i], L[hi] = L[hi], L[i]
    return i


if __name__ == '__main__':
    N = 200
    unsorted_list = [random.randint(0, 1000) for _ in range(N)]

    plt.plot(unsorted_list, linestyle='none', marker='.', color='blue')
    plt.plot(full_quicksort(unsorted_list), marker='.', color='red')
    plt.show()
