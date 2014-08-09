import re
from PIL import Image
import os
import StringIO


def username_valid(username):

    
    """
    Check if username consist of only allowed characters
    >>> username_valid('test')
    True
    >>> username_valid('Test9_')
    True
    >>> username_valid('test*')
    False
    >>> username_valid('test test')
    False
        
    """
    reg = re.compile(r"^[0-9A-Za-z_]+$")

    return bool(reg.match(username))


if __name__ == "__main__":

    import doctest
    doctest.testmod()

