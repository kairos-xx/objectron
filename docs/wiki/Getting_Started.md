# Getting Started

Welcome to the **Objectron** package! This guide will help you get started with transforming and tracking Python objects.

## Installation

You can install Objectron using `pip`:

```bash
pip install Objectron

Or install it manually:

git clone https://github.com/kairos-xx/objectron.git
cd objectron
pip install .
```

## Basic Usage

Here's a simple example to demonstrate how to use Objectron:
```python
from objectron import Objectron


def main():
    objectron = Objectron()
    a = objectron.transform({})

    # Chained Attribute Assignment
    a.b.c.d.e.f = 3
    print(a)  # Output: DictProxy({'b': {'c': {'d': {'e': {'f': 3}}}}}})
    print(a.b.c.d.e.f)  # Output: 3


if __name__ == "__main__":
    main()
```

## Exploring Proxies

Objectron uses proxy classes to wrap original objects. Here's how different types are handled:

- **Mutable Types**: dict, list, set
- **Immutable Types**: int, float, str, tuple, frozenset, complex

*Each proxy allows dynamic attribute assignments and method interceptions.*

# Advanced Usage

*For more complex scenarios, Objectron supports path-based access and method interception.*

```python
from objectron import Objectron


def advanced_example():
    objectron = Objectron()
    a = objectron.transform({"numbers": [1, 2, 3]})

    # Path-Based Access
    a["numbers"].append(4)
    print(a["numbers"])  # Output: [1, 2, 3, 4]

    # Chained Attribute Access
    a.new_attr.sub_attr = "Hello"
    print(a.new_attr.sub_attr)  # Output: Hello


if __name__ == "__main__":
    advanced_example()
```
# API Reference

See [API Reference](api_reference.md) for detailed documentation of all classes and methods.

# FAQs

**Q1:** What types of objects can be transformed?

**A1:** Objectron supports both mutable and immutable types, including dict, list, set, int, float, str, tuple, frozenset, and complex.

**Q2:** How does method interception work?

**A2:** Objectron wraps methods to log calls and transform their results into proxies, allowing you to monitor method executions.

# License

Objectron is licensed under the MIT License.