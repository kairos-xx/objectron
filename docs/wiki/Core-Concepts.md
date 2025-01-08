
# Core Concepts

## Object Transformation
Objectron transforms Python objects into proxy objects that enable monitoring and enhanced functionality while maintaining the original interface.

## Proxy System
The proxy system provides:
- Transparent attribute access
- Method call interception
- Reference tracking
- Dynamic attribute creation

## Type Support
Objectron includes specialized proxies for:
- Dictionaries (DictProxy)
- Lists (ListProxy)
- Numbers (IntProxy, FloatProxy)
- Strings (StrProxy)
- Tuples (TupleProxy)
- Sets (SetProxy)
- Custom objects (DynamicProxy)

## Reference Management
The DeepObjectReplacer handles:
- Global reference tracking
- Circular reference detection
- Safe reference updates
- Thread-safe operations

## Dynamic Access Patterns
Two main access patterns:
1. Attribute-style: `config.database.host`
2. Path-based: `config["database.host"]`
