import numpy as np
from operator import itemgetter



def bw_transform(s):
    n = len(s)
    m = sorted([s[i:n]+s[0:i] for i in range(n)])
    I = m.index(s)
    L = []
    L += ([q[-1] for q in m])
    return I, L


def bw_restore(I, L):
    n = len(L)
    X = sorted([(i, x) for i, x in enumerate(L)], key=itemgetter(1))

    T = [None for i in range(n)]
    for i, y in enumerate(X):
        j, _ = y
        T[j] = i

    Tx = [I]
    for i in range(1, n):
        Tx.append(T[Tx[i-1]])

    S = [L[i] for i in Tx]
    S.reverse()
    return S


########################################################################################################################

if __name__ == "__main__":
    original = [7,5,4,7,5,6,6,8,8,7,8,8,8,4]
    pos, transformed = bw_transform(original)

    print("Original: %s" %original)
    print("Transformada: (%s, %s)" %(pos, transformed))

    restore = np.array(list(bw_restore(pos, transformed)))
    if restore.all() == np.array(original).all():
        print("Lossless: True")
    else:
        print("Lossless: False")