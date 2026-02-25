# REPL and Jupyter

## Learning Objectives

- Understand what a REPL is and how to use it
- Recognize the benefits of interactive Python development
- Get introduced to Jupyter notebooks as an interactive coding environment

## Why This Matters

Interactive tools like the Python REPL and Jupyter notebooks let you experiment with code immediately, see results in real-time, and iterate quickly. These are essential skills for learning Python and for data exploration tasks you will encounter throughout this program.

## The Concept

### What is a REPL?

REPL stands for **Read-Eval-Print Loop**. It is an interactive programming environment that:

1. **Reads** your input (a line of code)
2. **Evaluates** (executes) the code
3. **Prints** the result
4. **Loops** back to wait for more input

### Using the Python REPL

To start the Python REPL, open your terminal and type:

```bash
python
```

You will see a prompt like this:

```
Python 3.11.0 (default, Oct 24 2022, 18:26:48)
>>> 
```

Now you can type Python code and see results immediately:

```python
>>> 2 + 3
5
>>> name = "Alice"
>>> print(f"Hello, {name}")
Hello, Alice
>>> len("Python")
6
```

To exit the REPL, type `exit()` or press `Ctrl+D` (Linux/Mac) or `Ctrl+Z` then Enter (Windows).

### Benefits of the REPL

- **Immediate feedback:** See results as you type
- **Experimentation:** Test ideas without creating files
- **Learning:** Explore language features interactively
- **Debugging:** Quickly check how functions or expressions behave

### Introduction to Jupyter Notebooks

Jupyter notebooks provide a richer interactive environment that combines:

- Code cells you can execute independently
- Markdown cells for documentation and notes
- Inline output including text, tables, and visualizations

Jupyter is especially popular in data science and analytics because you can mix explanations with executable code.

### Jupyter Basics

A Jupyter notebook is a `.ipynb` file opened in a browser-based interface. Each **cell** can contain:

- **Code:** Python statements that run when you execute the cell
- **Markdown:** Formatted text for documentation

**Example Code Cell:**

```python
# This is a code cell
x = 10
y = 20
x + y
```

*Output: 30*

**Example Markdown Cell:**

```markdown
## Data Analysis
This section explores the dataset using Python.
```

### Running Jupyter

To start Jupyter, run this command in your terminal:

```bash
jupyter notebook
```

This opens a file browser in your web browser. From there, you can create new notebooks or open existing ones.

### When to Use Each Tool

| Tool | Best For |
|------|----------|
| Python REPL | Quick tests, simple calculations, learning syntax |
| Jupyter Notebook | Data exploration, documentation, sharing analysis |
| Python Scripts (.py) | Production code, automation, larger programs |

## Summary

- The REPL provides instant feedback for testing Python code interactively
- Jupyter notebooks combine code, output, and documentation in one place
- Both tools accelerate learning and experimentation

## Additional Resources

- [Python Documentation: Using the Interpreter](https://docs.python.org/3/tutorial/interpreter.html)
- [Jupyter Official Documentation](https://jupyter.org/documentation)
- [Real Python: Jupyter Notebook Introduction](https://realpython.com/jupyter-notebook-introduction/)
