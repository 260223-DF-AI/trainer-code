# pip

## Learning Objectives

- Understand pip as Python's package manager
- Install, upgrade, and remove packages
- Work with PyPI (Python Package Index)
- Manage package versions effectively

## Why This Matters

Python's strength lies in its ecosystem of third-party packages. pip is the tool that connects you to over 400,000 packages on PyPI, from web frameworks like Django to data science libraries like pandas. Mastering pip is essential for leveraging Python's full potential and building real-world applications.

## Concept

### What Is pip?

pip stands for "Pip Installs Packages" (a recursive acronym). It's Python's default package manager, included with Python 3.4 and later. pip downloads packages from PyPI (Python Package Index) and installs them into your Python environment.

### Checking pip Installation

```bash
# Check if pip is installed
pip --version
# pip 23.2.1 from /path/to/pip (python 3.11)

# Alternative (useful if multiple Python versions)
python -m pip --version
```

### Installing Packages

**Basic installation:**

```bash
pip install requests
```

**Install specific version:**

```bash
pip install requests==2.28.0
```

**Install minimum version:**

```bash
pip install "requests>=2.25.0"
```

**Install from requirements file:**

```bash
pip install -r requirements.txt
```

**Install in development mode (editable):**

```bash
pip install -e .
```

### Upgrading Packages

```bash
# Upgrade a specific package
pip install --upgrade requests

# Upgrade pip itself
pip install --upgrade pip

# Alternative
python -m pip install --upgrade pip
```

### Removing Packages

```bash
# Uninstall a package
pip uninstall requests

# Uninstall without confirmation
pip uninstall -y requests
```

### Listing Installed Packages

```bash
# List all installed packages
pip list

# List outdated packages
pip list --outdated

# Show package details
pip show requests
```

Example output of `pip show`:

```
Name: requests
Version: 2.31.0
Summary: Python HTTP for Humans.
Home-page: https://requests.readthedocs.io
Author: Kenneth Reitz
License: Apache 2.0
Location: /path/to/site-packages
Requires: certifi, charset-normalizer, idna, urllib3
Required-by: some-other-package
```

### Freezing Dependencies

```bash
# Output installed packages in requirements format
pip freeze

# Save to file
pip freeze > requirements.txt
```

### Searching for Packages

While `pip search` is deprecated due to server load, you can:

1. Search on [PyPI website](https://pypi.org/)
2. Use `pip index versions package_name` to see available versions

```bash
pip index versions requests
```

### Understanding PyPI

PyPI (Python Package Index) is the official repository for Python packages. When you run `pip install package_name`, pip:

1. Connects to PyPI
2. Downloads the package and its dependencies
3. Installs everything into your environment

### Version Specifiers

Control exactly which versions pip installs:

```
package==1.0.0    # Exact version
package>=1.0.0    # Minimum version
package<=2.0.0    # Maximum version
package>=1.0,<2.0 # Version range
package~=1.4.2    # Compatible release (>=1.4.2, <1.5.0)
package!=1.5.0    # Exclude version
```

### Common pip Commands Reference

| Command | Description |
|---------|-------------|
| `pip install package` | Install a package |
| `pip install package==1.0` | Install specific version |
| `pip install -r requirements.txt` | Install from file |
| `pip install --upgrade package` | Upgrade package |
| `pip uninstall package` | Remove package |
| `pip list` | Show installed packages |
| `pip list --outdated` | Show outdated packages |
| `pip show package` | Show package info |
| `pip freeze` | Output installed packages |
| `pip cache purge` | Clear pip cache |

### Installing from Different Sources

```bash
# From PyPI (default)
pip install requests

# From a Git repository
pip install git+https://github.com/user/repo.git

# From a local directory
pip install /path/to/package

# From a wheel file
pip install package-1.0-py3-none-any.whl

# From a tarball
pip install package-1.0.tar.gz
```

### pip Configuration

Create a pip configuration file for custom settings:

**Windows:** `%APPDATA%\pip\pip.ini`
**Linux/Mac:** `~/.pip/pip.conf`

```ini
[global]
timeout = 60
index-url = https://pypi.org/simple

[install]
trusted-host = pypi.org
```

## Summary

pip is Python's package manager for installing, upgrading, and removing packages from PyPI. Use `pip install package` to install, `pip list` to see installed packages, and `pip freeze > requirements.txt` to save dependencies. Version specifiers like `==`, `>=`, and `<` control which versions are installed. Always use pip within a virtual environment to keep projects isolated.

## Resources

- [pip Documentation](https://pip.pypa.io/en/stable/)
- [PyPI - Python Package Index](https://pypi.org/)
- [Python Packaging User Guide](https://packaging.python.org/)
