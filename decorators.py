import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"\nFunction '{func.__name__}' took {time.time() - start_time:.6f} seconds to execute.")
        return result
    return wrapper

def validateInput(*valid_args):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for arg, valid_arg in zip(args, valid_args):
                if not isinstance(arg, valid_arg):
                    raise TypeError(f"'{type(arg).__name__}' is not of expected type '{valid_arg.__name__}'")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:            
            memo[x] = f(x)
        return memo[x]
    return helper

def log(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Called '{func.__name__}' with args: {args}, kwargs: {kwargs}, returned: {result}")
        return result
    return wrapper