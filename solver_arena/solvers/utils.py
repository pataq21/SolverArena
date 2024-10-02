import time
import psutil


def track_performance(func):
    """
    Decorator to track the execution time and memory usage of a function.

    Args:
        func (function): The function to be decorated.

    Returns:
        wrapper: A wrapper function that calculates time and memory used.
    """
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        memory_before = process.memory_info().rss / (1024 * 1024)  # Memory in MB
        start_time = time.time()

        result = func(*args, **kwargs)  # Call the original function

        end_time = time.time()
        memory_after = process.memory_info().rss / (1024 * 1024)  # Memory in MB

        runtime = end_time - start_time
        memory_used = memory_after - memory_before

        # Attach the performance metrics to the result, if it's a dict
        if isinstance(result, dict):
            result.update({
                'runtime': runtime,
                'memory_before_MB': memory_before,
                'memory_after_MB': memory_after,
                'memory_used_MB': memory_used,
            })

        return result

    return wrapper
