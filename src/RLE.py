import matplotlib.image as mpimg
import numpy as np
import os
import time


def RLE_compress(data):
    f = open("compressedRLE.dat", 'wb')
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
    f = open("compressedRLE.dat", 'rb')
    byte1 = f.read(1)
    byte2 = f.read(1)
    while byte1:
        decompressed += int.from_bytes(byte1, 'little') * [int.from_bytes(byte2, 'little')]
        byte1 = f.read(1)
        byte2 = f.read(1)
    f.close()
    return decompressed


# RLE sem decodificação e mais eficiente, em que apenas aparece o símbolo (sem contador) quando ocorre apenas 1 vez
def RLE_compress2(data):
    f = open("compressedRLE.dat", 'wb')
    compressed = []
    prev_number = data[0]
    counter = 1
    for i in data[1:]:
        if i != prev_number:
            if counter > 1:
                compressed += [counter, prev_number]
            else:
                compressed += [prev_number]
            counter = 1
            prev_number = i
        else:
            counter += 1
    if counter > 1:
        compressed += [counter, prev_number]
    else:
        compressed += [prev_number]
    compressed = np.array(compressed, dtype='uint8').tobytes()
    f.write(compressed)
    f.close()


########################################################################################################################

def main():
    start_time = time.time()

    imagem = "zebra.bmp"
    img = mpimg.imread(imagem)
    img = img.astype(int)
    img = img.flatten()

    RLE_compress(img)

    size = os.path.getsize('compressedRLE.dat')
    size_PNG = os.path.getsize(imagem[:-4] + ".png")

    print("Imagem: %s" % imagem)
    print("Tamanho da imagem original: %d" %len(img))
    print("Tamanho da imagem PNG fornecido: %d" %size_PNG)
    print("Taxa de compressão PNG fornecido: %.2f%%" %(100 - (size_PNG / len(img)) * 100))
    print("Tamanho da imagem comprimida: %d" %size)
    print("Taxa de compressão: %.2f%%" %(100 - (size / len(img)) * 100))
    print("Rácio de compressão: %.2f:1" %(len(img) / size))
    print("Tempo de execução: %.3fs" %(time.time() - start_time))

    img_decompressed = np.array(RLE_decompress())
    if img_decompressed.all() == img.all():
        print("Lossless: True")
    else:
        print("Lossless: False")


if __name__ == '__main__':
    main()