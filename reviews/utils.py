import string 
import random  


def slug_generator():
    return ''.join(random.choises(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))
