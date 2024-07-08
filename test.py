import numpy as np


def convolve2d(image, kernel):
    # Get dimensions
    i_height, i_width = image.shape
    k_height, k_width = kernel.shape

    # Calculate output dimensions
    out_height = i_height - k_height + 1
    out_width = i_width - k_width + 1

    # Initialize output
    output = np.zeros((out_height, out_width))

    # Perform convolution
    for y in range(out_height):
        for x in range(out_width):
            output[y, x] = np.sum(image[y:y + k_height, x:x + k_width] * kernel)

    return output


# Example usage
image = np.random.rand(10, 10)
sharpen = np.array([[0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0]])

result = convolve2d(image, kernel)
print(result)