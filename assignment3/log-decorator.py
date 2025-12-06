#Task 1
import logging

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    def wrapper(*args, **kwargs):
        # Prepare readable args/kwargs
        pos = list(args) if args else "none"
        kw = kwargs if kwargs else "none"

        # Call the actual function
        result = func(*args, **kwargs)

        # Write log entry
        logger.log(
            logging.INFO,
            f"function: {func.__name__}\n"
            f"positional parameters: {pos}\n"
            f"keyword parameters: {kw}\n"
            f"return: {result}\n"
            "-----------------------------"
        )
        return result
    return wrapper

@logger_decorator
def no_params():
    print("Hello, World!")

@logger_decorator
def any_pos_args (*args):
    return True

@logger_decorator
def any_kwargs(**kwargs):
    return logger_decorator

if __name__ == "__main__":
    no_params()
    any_pos_args(1,2,3,4)
    any_kwargs(a=1, b=2, c=3, d=4)