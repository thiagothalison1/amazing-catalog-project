import random
import string


def gen_random_text(size):
    return ''.join(
        random.choice(
            string.ascii_uppercase +
            string.digits) for x in xrange(size))
