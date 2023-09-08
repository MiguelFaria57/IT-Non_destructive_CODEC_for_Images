import bz2
import matplotlib.image as mpimg
import numpy as np
import pickle
import os
import time


# escreve bytrarray para ficheiro
def write_file(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
        f.close()

# le bytearray do ficheiro
def read_file(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
        f.close()
        return data



def main():
    start_time = time.time()

    imagem = "pattern.bmp"
    img = mpimg.imread(imagem)
    img = img.flatten()

    img_compressed = bz2.compress(img)
    write_file('compressedBzip2.dat', img_compressed)

    size = os.path.getsize('compressedBzip2.dat')
    size_PNG = os.path.getsize(imagem[:-4] + ".png")

    print("Imagem: %s" %imagem)
    print("Tamanho da imagem original: %d" %len(img))
    print("Tamanho da imagem PNG fornecido: %d" %size_PNG)
    print("Taxa de compressão PNG fornecido: %.2f%%" %(100 - (size_PNG / len(img)) * 100))
    print("Tamanho da imagem comprimida: %d" %size)
    print("Taxa de compressão: %.2f%%" %(100 - (size / len(img)) * 100))
    print("Rácio de compressão: %.2f:1" %(len(img) / size))
    print("Tempo de execução: %.3fs" %(time.time() - start_time))

    img_decompressed = np.array(list(bz2.decompress(read_file('compressedBzip2.dat'))))
    if img_decompressed.all() == img.all():
        print("Lossless: True")
    else:
        print("Lossless: False")


if __name__ == '__main__':
    main()