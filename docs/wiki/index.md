
# Objectron Documentation

## Overview
Objectron is an advanced Python object transformation system that enables dynamic monitoring, attribute tracking, and deep reference management through a powerful proxy-based architecture.

## Quick Navigation
- [Installation](Installation.md)
- [Getting Started](Getting_Started.md)
- [Core Concepts](Core-Concepts.md)
- [Advanced Usage](Advanced-Usage.md)
- [API Reference](API-Reference.md)
- [Examples](Examples.md)

## Key Features
- Smart Access - Transparent attribute access and path-based traversal
- Deep Monitoring - Method and attribute tracking with reference control  
- Type Coverage - Support for built-in and custom types
- Reference Control - Global tracking with circular reference handling
- Decorators - Easy class and method transformations

## Quick Start
```python
from objectron import Objectron

# Transform objects
objectron = Objectron() 
config = objectron.transform({})

# Dynamic attributes
config.database.host = "0.0.0.0"
config.database.port = 5432

# Path-based access
config["database.credentials.user"] = "admin"
```

## Installation
```bash
pip install objectron
```

## Core Components
- Objectron - Main transformation engine
- DynamicProxy - Base proxy implementation 
- Specialized Proxies - Type-specific proxies
- Decorators - Class and method transformations
