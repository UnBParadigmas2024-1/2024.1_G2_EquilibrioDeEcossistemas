from functools import wraps

def check_pos(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.pos is not None:
            return func(*args, **kwargs)
        return
    return wrapper
