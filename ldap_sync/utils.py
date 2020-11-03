import random


def generate_random_string(length=16):
    seed = '23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
    return ''.join(random.sample(seed, length))
