# Virtual Environments

## Learning Objectives

- Understand why virtual environments are essential
- Create and activate virtual environments using venv
- Manage dependencies with requirements.txt
- Work with multiple Python projects independently

## Why This Matters

Different projects often require different versions of the same package. Without isolation, installing packages for one project can break another. Virtual environments solve this by creating isolated Python installations for each project. This is a fundamental skill that every professional Python developer uses daily.

## Concept

### The Problem Virtual Environments Solve

Consider this scenario:

- Project A needs Django 3.2
- Project B needs Django 4.0
- Both projects are on the same computer

Without virtual environments, you can only have one version of Django installed globally. Installing Django 4.0 for Project B would break Project A.

### What Is a Virtual Environment?

A virtual environment is an isolated directory containing:

- A copy of the Python interpreter
- Its own pip installer
- Its own site-packages directory for installed packages

Packages installed in one environment don't affect other environments or the system Python.

### Creating Virtual Environments with venv

Python includes the `venv` module for creating virtual environments:

```bash
# Create a virtual environment named "venv"
python -m venv venv

# Or give it a descriptive name
python -m venv my_project_env
```

This creates a directory structure:

```
venv/
    bin/           # Scripts (activate, pip, python) - Linux/Mac
    Scripts/       # Scripts - Windows
    lib/           # Installed packages
    include/       # C headers (for building packages)
    pyvenv.cfg     # Configuration file
```

### Activating the Environment

**Windows (Command Prompt):**

```bash
venv\Scripts\activate
```

**Windows (PowerShell):**

```bash
venv\Scripts\Activate.ps1
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

When activated, your prompt changes:

```bash
(venv) C:\my_project>
```

### Deactivating the Environment

```bash
deactivate
```

### Installing Packages in the Environment

With the environment activated, use pip normally:

```bash
# Install packages
pip install requests
pip install pandas numpy matplotlib

# Check installed packages
pip list

# Show package details
pip show requests
```

Packages are installed only in the active environment, not globally.

### The requirements.txt File

Record your project's dependencies in a `requirements.txt` file:

**Creating requirements.txt:**

```bash
# Capture current environment's packages
pip freeze > requirements.txt
```

This creates a file like:

```
certifi==2023.7.22
charset-normalizer==3.3.0
idna==3.4
numpy==1.26.0
pandas==2.1.1
requests==2.31.0
urllib3==2.0.6
```

**Installing from requirements.txt:**

```bash
# Install all listed packages
pip install -r requirements.txt
```

### Best Practices for requirements.txt

**Pin exact versions for production:**

```
Django==4.2.5
requests==2.31.0
```

**Use version ranges for flexibility:**

```
Django>=4.0,<5.0
requests>=2.20
```

**Separate development dependencies:**

```
# requirements.txt (production)
Django==4.2.5
psycopg2==2.9.7

# requirements-dev.txt (development)
-r requirements.txt
pytest==7.4.2
black==23.9.1
```

### Workflow Example

```bash
# 1. Create project directory
mkdir my_project
cd my_project

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\activate  # Windows

# 4. Install dependencies
pip install flask requests

# 5. Save dependencies
pip freeze > requirements.txt

# 6. Write your code
# ... develop your application ...

# 7. Deactivate when done
deactivate
```

### Sharing Your Project

When sharing your project:

1. **Do NOT include the venv folder** - add it to `.gitignore`
2. **Do include requirements.txt**

```
# .gitignore
venv/
__pycache__/
*.pyc
```

Others can recreate your environment:

```bash
# Clone the project
git clone https://github.com/user/project.git
cd project

# Create and activate new environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

### Virtual Environment Alternatives

While `venv` is built-in, other tools exist:

- **virtualenv** - Third-party, more features than venv
- **conda** - Popular for data science, manages non-Python dependencies
- **pipenv** - Combines pip and virtualenv with Pipfile
- **poetry** - Modern dependency management and packaging

For now, `venv` is sufficient and comes with Python.

## Summary

Virtual environments isolate project dependencies from each other and the system Python. Create them with `python -m venv venv`, activate with platform-specific scripts, and deactivate when done. Use `requirements.txt` to record and share dependencies. Always add the virtual environment directory to `.gitignore` and never commit it to version control.

## Resources

- [Python Docs: venv](https://docs.python.org/3/library/venv.html)
- [Real Python: Virtual Environments Primer](https://realpython.com/python-virtual-environments-a-primer/)
- [pip Documentation](https://pip.pypa.io/en/stable/)
