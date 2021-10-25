import numpy as np
from PIL import Image


def create_gray_scale_image(address):
    # opening the image in store in numpy array
    image = np.array(Image.open(address))
    print('Here is first row of image (each row is a set of pixels showed by R G B values)\n')
    print(image[0])
    print('Processing ...\n')

    # converting image to gray-scale (transform each pixel to one number in range (0,255))
    # Y' = 0.2989 R + 0.5870 G + 0.1140 B (formula in stackOverflow)
    image_array = [[(j[0] * 299 / 1000) + (j[1] * 587 / 1000) + (j[2] * 114 / 1000) for j in r] for r in image]

    # storing the gray-scale image in numpy array
    gray_scale_image = np.array(image_array)

    # saving the gray-level image
    Image.fromarray(gray_scale_image).convert('L').save('GrayScale Of Your Image.png')

    # normalizing matrix (each element should be between (0 , 1))
    return gray_scale_image * (1 / 255)

# matrix created recursively in a way https://en.wikipedia.org/wiki/Ordered_dithering says.
def create_dither_matrix(window_size):
    if window_size == 1:
        return np.array([[0]])
    else:
        element_0_0 = (window_size ** 2) * create_dither_matrix(int(window_size / 2))
        element_0_1 = (window_size ** 2) * create_dither_matrix(int(window_size / 2)) + 2
        element_1_0 = (window_size ** 2) * create_dither_matrix(int(window_size / 2)) + 3
        element_1_1 = (window_size ** 2) * create_dither_matrix(int(window_size / 2)) + 1
        column1 = np.concatenate((element_0_0, element_1_0), axis=0)
        column2 = np.concatenate((element_0_1, element_1_1), axis=0)
        result_matrix = (1 / window_size ** 2) * np.concatenate((column1, column2), axis=1)
        return result_matrix


def ordered_dithering_algorithem(normalized_grayScale_image, dithering_matrix):
    n = np.size(dithering_matrix, axis=0)
    maxX = np.size(normalized_grayScale_image, axis=1)
    maxY = np.size(normalized_grayScale_image, axis=0)
    for x in range(maxX):
        for y in range(maxY):
            i = x % n
            j = y % n
            if normalized_grayScale_image[y][x] > dithering_matrix[i][j]:
                normalized_grayScale_image[y][x] = 255
            else:
                normalized_grayScale_image[y][x] = 0
    print('Dithered image row example')
    print(normalized_grayScale_image[0])
    print()
    Image.fromarray(normalized_grayScale_image).convert('L').save('dithered version of your image.png', bit=1)


# Reading inputs
address = input('Image name or Address:')
window_size = int(input('Dithering window size:'))

dither_matrix = create_dither_matrix(window_size)
print('Dithering-matrix:\n')
print(dither_matrix)
print()

image = create_gray_scale_image(address)
print('grayscale of image was created successfully.\n')

ordered_dithering_algorithem(image, dither_matrix)
print('dithered version of your image was created successfully.')
