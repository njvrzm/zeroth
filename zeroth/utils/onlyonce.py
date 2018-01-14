from functools import wraps

def onlyonce(fn):
    """Wraps a function to run once and return the same result thereafter."""
    result = []
    @wraps(fn)
    def doit(*a, **k):
        if not result:
            result.append(fn(*a, **k))
        return result[0]
    return doit
