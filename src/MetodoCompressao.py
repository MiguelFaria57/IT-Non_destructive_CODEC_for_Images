import matplotlib.image as mpimg
import numpy as np
from operator import itemgetter
import os
import time



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


def RLE_compress(data):
    f = open("compressed.dat", 'ab')
    compressed = []
    prev_number = data[0]
    counter = 1
    for i in data[1:]:
        if i != prev_number:
            compressed += [counter, prev_number]
            counter = 1
            prev_number = i
        else:
            counter += 1
    compressed += [counter, prev_number]
    compressed = np.array(compressed, dtype='uint8').tobytes()
    f.write(compressed)
    f.close()


def RLE_decompress():
    decompressed = []
    f = open("compressed.dat", 'rb')
    linhas = int.from_bytes(f.read(2), 'little')
    lista_BWPos = []
    for i in range(linhas):
        lista_BWPos += [int.from_bytes(f.read(1), 'little')]
    byte1 = f.read(1)
    byte2 = f.read(1)
    while byte1:
        #print(byte)
        decompressed += int.from_bytes(byte1, 'little') * [int.from_bytes(byte2, 'little')]
        byte1 = f.read(1)
        byte2 = f.read(1)
    f.close()
    return decompressed, lista_BWPos


def compress(c, inf):
    linhas = int(len(inf)/c)
    data = []
    for i in range(linhas):
        data += [list(inf[i*c:i*c+c])]
    lista_BWPos = []
    lista_BWData = []
    for i in data:
        i, l = bw_transform(i)
        lista_BWPos += [i]
        lista_BWData += l
    f = open("compressed.dat", 'wb')
    f.write(linhas.to_bytes(2, 'little') + np.array(lista_BWPos, dtype='uint8').tobytes())
    f.close()
    RLE_compress(lista_BWData)


def decompress():
    data = []
    decompressed, lista_BWPos = RLE_decompress()
    c = int(len(decompressed)/len(lista_BWPos))
    for i in range(len(lista_BWPos)):
        data += bw_restore(lista_BWPos[i], list(decompressed[i*c:i*c+c]))
    return data


def main():
    start_time = time.time()

    imagem = "pattern.bmp"
    img = mpimg.imread(imagem)
    c = len(img[0])
    img = img.flatten()

    compress(c, img)

    size = os.path.getsize('compressed.dat')
    size_PNG = os.path.getsize(imagem[:-4] + ".png")

    print("Imagem: %s" % imagem)
    print("Tamanho da imagem original: %d" % len(img))
    print("Tamanho da imagem PNG fornecido: %d" % size_PNG)
    print("Taxa de compressão PNG fornecido: %.2f%%" % (100 - (size_PNG / len(img)) * 100))
    print("Tamanho da imagem comprimida: %d" % size)
    print("Taxa de compressão: %.2f%%" % (100 - (size / len(img)) * 100))
    print("Rácio de compressão: %.2f:1" % (len(img) / size))
    print("Tempo de execução: %.3fs" % (time.time() - start_time))

    img_decompressed = np.array(decompress())
    if img_decompressed.all() == img.all():
        print("Lossless: True")
    else:
        print("Lossless: False")


if __name__ == '__main__':
    main()