"""
Unit Test helpers
"""


def p(*args):
    """Test Helper function
    Converts a board layout line-by-line as 8 parameters
    to a single string.

    Used for checking if two board layouts are identical (reduced to string comparison)
    """
    assert len(args) == 8
    return "\\\\".join(args)