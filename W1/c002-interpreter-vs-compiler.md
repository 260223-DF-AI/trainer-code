# Interpreter vs Compiler

## Learning Objectives

- Explain the difference between interpreted and compiled languages
- Understand how Python executes code as an interpreted language
- Recognize the trade-offs between interpretation and compilation

## Why This Matters

Understanding how your code is executed helps you debug issues, optimize performance, and choose the right tools for different tasks. Python, the language you will use throughout this program, is an interpreted language. Knowing what that means will help you understand its behavior and strengths.

## The Concept

### What is a Compiler?

A **compiler** translates an entire program from source code (human-readable) into machine code (binary instructions) before the program runs. The compiled output is an executable file that can run independently.

**Compilation Process:**

```
Source Code (.c, .java) --> Compiler --> Executable/Bytecode --> Run
```

**Examples of Compiled Languages:**

- C
- C++
- Go
- Rust

**Characteristics:**

- Errors are caught at compile time (before running)
- Faster execution since translation happens once
- Produces platform-specific executables (unless using bytecode like Java)

### What is an Interpreter?

An **interpreter** translates and executes code line by line at runtime. There is no separate compilation step that produces an executable file.

**Interpretation Process:**

```
Source Code (.py) --> Interpreter --> Executes line by line
```

**Examples of Interpreted Languages:**

- Python
- JavaScript
- Ruby
- PHP

**Characteristics:**

- Errors appear at runtime when the problematic line is reached
- Easier to test and debug interactively
- Slower execution compared to compiled code (translation happens each time)

### Python: An Interpreted Language

Python uses an interpreter to execute your scripts. When you run a Python file:

1. The interpreter reads your `.py` file
2. It parses and executes each statement in order
3. If an error occurs, execution stops at that line

```python
# example.py
print("This line runs first")
print("This line runs second")
print(undefined_variable)  # Error occurs here
print("This line never runs")
```

Running the above script would print the first two messages, then raise a `NameError` on the third line.

### Hybrid Approaches

Some languages use both techniques:

- **Java** compiles to bytecode, which the JVM interprets
- **Python** internally compiles to bytecode (`.pyc` files) for efficiency, but this is transparent to the developer

## Trade-offs Summary

| Aspect | Compiled | Interpreted |
|--------|----------|-------------|
| Speed | Faster at runtime | Slower at runtime |
| Error Detection | At compile time | At runtime |
| Development Cycle | Edit, compile, run | Edit, run |
| Portability | Platform-specific (often) | Platform-independent |

## Summary

- Compilers translate entire programs before execution; interpreters translate line by line at runtime
- Python is an interpreted language, making it flexible and easy to test interactively
- Understanding this distinction helps you anticipate how errors appear and how performance differs across languages

## Additional Resources

- [Python Documentation: Execution Model](https://docs.python.org/3/reference/executionmodel.html)
- [GeeksforGeeks: Compiler vs Interpreter](https://www.geeksforgeeks.org/compiler-vs-interpreter-2/)
- [Real Python: How Python Runs](https://realpython.com/cpython-source-code-guide/)
