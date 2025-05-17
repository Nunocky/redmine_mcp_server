import random
import string


def random_identifier(prefix="testproj"):
    """Generate a unique identifier"""
    return prefix + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
