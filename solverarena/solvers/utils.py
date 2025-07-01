import time
from memory_profiler import memory_usage


def track_performance(func):
    """
    Decorator to track the execution time and memory usage of a function.
    It returns a tuple: (performance_data, original_result).
    """
    def wrapper(*args, **kwargs):

        start_time = time.time()
        initial_memory_used = memory_usage(max_usage=True)
        max_memory_during_run, result = memory_usage((func, args, kwargs), interval=0.1, retval=True, max_usage=True)
        end_time = time.time()
        memory_diff = max_memory_during_run - initial_memory_used
        runtime = end_time - start_time

        performance_data = {
            'runtime': runtime,
            'memory_used_MB': memory_diff,
        }
        return performance_data, result

    return wrapper
