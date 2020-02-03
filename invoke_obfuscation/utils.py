import random

def is_good_luck():
    return 0.5 > random.random()

def make_str_to_lower_or_upper(text):
    return "".join([c.upper() if is_good_luck() else c for c in text])

def make_random_space():
    return " "*random.choice([0, 1])

