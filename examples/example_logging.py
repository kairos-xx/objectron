from objectron import Objectron
from objectron.wrappers import method_wrapper


class Calculator:
    @method_wrapper
    def add(self, a: int, b: int) -> int:
        return a + b

    @method_wrapper
    def multiply(self, a, b):
        return a * b


def example_logging():
    objectron = Objectron()
    calc = objectron.transform(Calculator())

    result_add = calc.add(5, 7)
    print(f"Addition Result: {result_add}")  # Output: 12

    result_mul = calc.multiply(3, 4)
    print(f"Multiplication Result: {result_mul}")  # Output: 12


if __name__ == "__main__":
    example_logging()
