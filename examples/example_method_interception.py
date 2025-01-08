from objectron import Objectron


def example_method_interception():
    objectron = Objectron()
    a = objectron.transform({"list": [1, 2, 3]})

    # Append using path string
    a["list"].append(4)
    # Output:
    # INFO:__main__:Executing method: append
    # INFO:__main__:Method append executed successfully.

    print(a["list"])  # Output: [1, 2, 3, 4]


if __name__ == "__main__":
    example_method_interception()
