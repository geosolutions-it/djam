import random
import string


def random_string(length=25):
    """Generate a random string of fixed length """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
