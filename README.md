<div align="center">

<h1>Objectron</h1>
<img src="https://github.com/kairos-xx/objectron/raw/main/resources/icon_raster.png" alt="Objectron Logo" width="150"/>
<p><em>Advanced Python object transformation system with dynamic monitoring and deep reference management.</em></p>

  <a href="https://replit.com/@kairos/objectron">
    <img src="https://github.com/kairos-xx/objectron/raw/main/resources/replit.png" alt="Try it on Replit" width="150"/>
  </a>
</div>

## ✨ Features

- 🎯 **Smart Access** - Transparent attribute access, dynamic creation, and path-based traversal
- 🔄 **Deep Monitoring** - Comprehensive method and attribute tracking
- 🛠 **Type Coverage** - Full support for built-in and custom types
- 🔍 **Reference Control** - Automatic tracking with circular reference handling
- 🎨 **Flexible Syntax** - Mix attribute and path-based access patterns

## 📦 Quick Start

```python
from objectron import Objectron

# Transform objects
objectron = Objectron()
config = objectron.transform({})

# Dynamic attribute creation
config.database.host = "0.0.0.0"
config.database.port = 5432

# Path-based access
config["database.credentials.user"] = "admin"

print(config.database.host)          # "0.0.0.0"
print(config["database.port"])       # 5432
```

## 📦 Installation

```bash
pip install tree-interval
```

## 📖 Documentation

See our [Documentation Wiki](https://github.com/kairos-xx/objectron/wiki) for:
- Complete API Reference
- Usage Examples
- Implementation Details
- Best Practices

## 🤝 Contributing

Contributions welcome! Please submit a Pull Request.

## 📄 License

MIT License - see [LICENSE](LICENSE) file
