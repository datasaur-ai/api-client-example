import random


def random_color(seed: str) -> str:
    random.seed(seed)
    r = lambda: random.randint(0, 255)
    return "#%02X%02X%02X" % (r(), r(), r())
