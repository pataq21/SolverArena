import time
from memory_profiler import memory_usage


def track_performance(func):
    """
    Decorator to track the execution time and memory usage of a function.

    Args:
        func (function): The function to be decorated.

    Returns:
        wrapper: A wrapper function that calculates time and memory used.
    """
    def wrapper(*args, **kwargs):

        start_time = time.time()
        mem_usage, result = memory_usage((func, args, kwargs), interval=0.1, retval=True)
        end_time = time.time()
        initial_memory_used = mem_usage[0]
        max_memory_used = max(mem_usage)
        memory_diff = max_memory_used - initial_memory_used
        runtime = end_time - start_time

        # Attach the performance metrics to the result, if it's a dict
        if isinstance(result, dict):
            result.update({
                'runtime': runtime,
                'memory_used_MB': memory_diff,
            })

        return result

    return wrapper
