import numpy
from random import randint
from PIL import Image


def __random_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))


def __random_coord(image_size: int):
    dived_size = image_size // 2
    return randint(0, dived_size), randint(dived_size, image_size)


def generate_image(
    file_path: str, image_size: int = 128, max_amount_of_boxes: int = 10
):
    """
    Simple image generator

    Gets random amount of boxes with random size and paints them.
    """

    data = numpy.zeros((image_size, image_size, 3), dtype=numpy.uint8)

    amount_of_boxes = randint(1, max_amount_of_boxes)
    for _ in range(amount_of_boxes):
        frm1, to1 = __random_coord(image_size)
        frm2, to2 = __random_coord(image_size)
        data[frm1:to1, frm2:to2] = __random_color()

    Image.fromarray(data).save(file_path)
