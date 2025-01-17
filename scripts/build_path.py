import os

def buildPath(*segments):
    """Builds a valid path from multiple segments."""
    return os.path.join(*segments)