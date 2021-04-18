import numpy as np

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    return "Hi, you said: {}. Random number = {}".format(str(req),
                                                         np.random.random_sample(10))
