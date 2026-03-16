# Weekly Knowledge Check: [Week2-Python-Advanced]

## Part 1: Multiple Choice (MCQ)

### 1. What is the primary purpose of the `__init__.py` file in a Python package?
- [ ] A) To define the central entry point for script execution.
- [ ] B) To initialize variables that run prior to `python -m`.
- [ ] C) To mark a directory on disk as a Python package namespace.
- [ ] D) To manage static cache compiles for files.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) To mark a directory on disk as a Python package namespace.

- **Explanation:** The presence of `__init__.py` indicates to Python that the containing directory should be treated as a navigable package support loaded imports.
</details>

---

### 2. In a a `try-except-else-finally` block structure, when does the `else` block execute?
- [ ] A) Only if an exception was raised.
- [ ] B) Every single time the block triggers regardless of outcome.
- [ ] C) Only if the `try` block executes successfully without raising any exceptions.
- [ ] D) Immediately prior to the `finally` execution if an error triggers.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Only if the `try` block executes successfully without raising any exceptions.

- **Explanation:** The `else` block runs strictly alongside successful error-free flows inside code logic.
</details>

---

### 3. Which file opening mode should you select if you intend to write content onto the end of an existing document without Purging previous archives?
- [ ] A) `w`
- [ ] B) `r+`
- [ ] C) `a`
- [ ] D) `x`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `a`

- **Explanation:** Mode `a` stands for "Append". It places the file handle pointer backwards toward the end files.
</details>

---

### 4. What is the standard 2D labeled data structure used inside the `pandas` library?
- [ ] A) Series
- [ ] B) Matrix
- [ ] C) DataFrame
- [ ] D) Panel

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) DataFrame

- **Explanation:** `DataFrames` model tabular records Loaded using rows and labeled column coordinates seamlessly.
</details>

---

### 5. Which `collections` subclass is ideal for counting the frequency of elements loaded from any continuous iterable structure?
- [ ] A) `OrderedDict`
- [ ] B) `defaultdict`
- [ ] C) `Counter`
- [ ] D) `namedtuple`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `Counter`

- **Explanation:** `Counter` builds continuous mapping indexes assessing frequency occurrences flawlessly.
</details>

---

### 6. What keyword forces a standard continuous Python function setup to return outputs using Generator lazy setups?
- [ ] A) `return`
- [ ] B) `yield`
- [ ] C) `generate`
- [ ] D) `next`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `yield`

- **Explanation:** Generator functions load `yield` keywords suspension structures resuming forwards state archives cleanly during iterations continuously.
</details>

---

### 7. What does the `@wraps` decorator from the `functools` module avoid breaking inside custom decorators?
- [ ] A) It speeds up loop recursion structures.
- [ ] B) It preserves the original functions structure name and docstrings.
- [ ] C) It caches functional return outputs.
- [ ] D) It isolates local memory stack trace items.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It preserves the original functions structure name and docstrings.

- **Explanation:** It replicates original metadata loaded backwards over functionally wrapped descriptors safely.
</details>

---

### 8. Which `re` module function tests if a regular expression pattern aligns inside a target loaded string ANYWHERE within?
- [ ] A) `re.match()`
- [ ] B) `re.search()`
- [ ] C) `re.findall()`
- [ ] D) `re.split()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `re.search()`

- **Explanation:** `re.search()` inspects continuous items backwards whereas `re.match()` strictly demands starts aligned sequentially.
</details>

---

### 9. Which `functools` decorator can add simple local caching backwards preventing recursive continuous duplicate loads?
- [ ] A) `partial`
- [ ] B) `wraps`
- [ ] C) `lru_cache`
- [ ] D) `reduce`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `lru_cache`

- **Explanation:** `lru_cache` memoizes calculation outputs storing coordinates tied loaded directly supporting parameter combinations safely.
</details>

---

### 10. What primary dunder method turns objects into clean Context Manager workflows accessible utilizing the `with` statement?
- [ ] A) `__iter__` / `__next__`
- [ ] B) `__enter__` / `__exit__`
- [ ] C) `__call__`
- [ ] D) `__str__`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `__enter__` / `__exit__`

- **Explanation:** Standard triggers loaded alongside initial entry and forwards exits setups loaded with variables seamlessly.
</details>

---

## Part 2: Code Prediction

### 11. What does this regex capture print?
```python
import re
res = re.findall(r"\d+", "Cats: 2, Dogs: 4")
print(res)
```
- [ ] A) `[2]`
- [ ] B) `'24'`
- [ ] C) `['2', '4']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `['2', '4']`

- **Explanation:** `findall()` retrieves continuous numeric patterns matching sequences loaded supported backwards safely inside lists.
</details>

---

### 12. What structure outputs from this Try-Except-Finally test?
```python
try:
    x = 1 / 0
except ZeroDivisionError:
    print("Error")
finally:
    print("Finally")
```
- [ ] A) `Error`
- [ ] B) `Finally`
- [ ] C) `Error` followed by `Finally`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `Error` followed by `Finally`

- **Explanation:** Error block resolves due forwards division triggers; forwards exit standard outputs resolve fully regardless continuous triggers backward.
</details>

---

### 13. What is outputted looking at counter frequency triggers?
```python
from collections import Counter
c = Counter("abcac")
print(c["a"])
```
- [ ] A) 1
- [ ] B) 2

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 2

- **Explanation:** Frequencies increment count loaded variables continuous address backwards correctly.
</details>

---

### 14. What results from using this partial trigger setup?
```python
from functools import partial
def add(a, b): return a + b
add_five = partial(add, 5)
print(add_five(3))
```
- [ ] A) 5
- [ ] B) 8

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 8

- **Explanation:** `partial` freezes the first bound parameter with 5. Appending 3 loaded forwards yields 5 + 3 total.
</details>

---

### 15. What is the list comprehension lazy-evaluated generator equivalent output?
```python
gen = (x for x in [1, 10])
print(next(gen))
```
- [ ] A) 10
- [ ] B) 1

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 1

- **Explanation:** Generator expressions continuous compute lazy loads resolving exactly upon next fetches.
</details>

---

## Part 3: True / False

### 16. running `pip freeze > requirements.txt` automatically triggers forwards installers installing packages insideisolated nodes.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

- **Explanation:** `pip freeze` exports loaded names list, demands `pip install -r` to trigger installers backwards.
</details>

---

### 17. All built-in exceptions inside Python inherit loaded backwards forwards setups deriving fully from standard `BaseException`.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

- **Explanation:** standard hierarchy roots fully address absolute root triggers flawlessly.
</details>

---

### 18. Counters act exactly like regular dictionaries but return fallback coefficients setup returning `0` instead of triggering `KeyError`.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

- **Explanation:** Setup structures avoid crashes addressing items missing perfectly.
</details>

---

### 19. Generators store continuous full coefficient arrays loaded inside active RAM workloads sequentially.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

- **Explanation:** Generators avoid storing full archives loaded calculates elements fully on the fly.
</details>

---

## Part 4: Fill-in-the-Blank

### 21. FILL-IN-THE-BLANK
To allow direct terminal packaging execution loaded forwards triggers `python -m <package>`, package entry point setups demand files named `_____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `__main__.py` or `main.py`

- **Explanation:** Entry point layouts declare executable boundaries supporting packaging executions.
</details>

---

### 23. FILL-IN-THE-BLANK
Raising custom exception structures demand building template classes loaded deriving from `_____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `Exception`

- **Explanation:** Standard errors backwards inherit safely using explicit exception.
</details>

---

### 24. FILL-IN-THE-BLANK
To load data safely utilizing automatic closing hooks, Python uses the keyword `_____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `with`

- **Explanation:** with statement cleanup addresses Continuous handles safety seamlessly continuously.
</details>
