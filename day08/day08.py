import os.path
from timeit import default_timer as timer
import numpy as np

type Image = np.ndarray


def part1(image: Image) -> int:
    min_zeros_layer = min(image, key=lambda layer: (layer == 0).sum())
    return (min_zeros_layer == 1).sum() * (min_zeros_layer == 2).sum()


def decode_image(image: Image) -> Image:
    decoded = np.ones(image.shape[1:], dtype=int)*2
    for layer in image:
        mask = (decoded == 2) & (layer < 2)
        decoded = np.where(mask, layer, decoded)
    return decoded


def plot_image(image: Image) -> None:
    import matplotlib.pyplot as plt
    plt.imshow(image)
    plt.show()


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

image = np.array([int(x) for x in data])
image = np.reshape(image, (-1, 6, 25))
print("Part 1:", part1(image))
decoded = decode_image(image)

e = timer()
print(f"time: {e-s}")

plot_image(decoded)
