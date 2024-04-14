import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"Function '{func.__name__}' took {time.time() - start_time:.6f} seconds to execute.")
        return result
    return wrapper