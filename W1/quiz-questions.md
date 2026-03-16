# Weekly Knowledge Check: [Week1-Agile-Git-Python]

## Part 1: Multiple Choice (MCQ)

### 1. What is the primary difference between Agile and Waterfall methodologies?
- [ ] A) Waterfall is iterative and incremental, while Agile is sequential.
- [ ] B) Waterfall requires fixing requirements early, while Agile tolerates evolving requirements.
- [ ] C) Agile is linear with dedicated phases, while Waterfall is cyclical with continuous delivery.
- [ ] D) Waterfall is only used for software, while Agile is used for everything.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Waterfall requires fixing requirements early, while Agile tolerates evolving requirements.

- **Explanation:** Waterfall is sequential where requirements are set early. Agile is iterative and values adapting to changes over following rigid plans.
- **Why others are wrong:**
  - A) Loops are reversed; Agile is iterative.
  - C) Processes are reversed; Agile is continuous workflow cycles.
</details>

---

### 2. In Agile story pointing, what are points estimating?
- [ ] A) The exact amount of hours.
- [ ] B) Relative effort, complexity, and risk.
- [ ] C) Number of lines of code.
- [ ] D) Calendar days until completion.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Relative effort, complexity, and risk.

- **Explanation:** Points provide a relative score representing task size regarding difficulty or uncertainty, rather than absolute time slots.
- **Why others are wrong:**
  - A) Hours are concrete and fluctuate per person.
  - C) Code volumes are poor metrics for complex task logic.
</details>

---

### 3. Which type of Version Control System is Git?
- [ ] A) Centralized (CVCS)
- [ ] B) Distributed (DVCS)
- [ ] C) Local-only
- [ ] D) Serverless

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Distributed (DVCS)

- **Explanation:** Git distributes fully loaded history archives into every single connected local workstation instead of bounding code to a single host.
</details>

---

### 4. What is the result of `type( (1, 2) )` in Python?
- [ ] A) `<class 'list'>`
- [ ] B) `<class 'tuple'>`
- [ ] C) `<class 'set'>`
- [ ] d) `<class 'dict'>`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `<class 'tuple'>`

- **Explanation:** Parentheses `()` containing comma-separated figures initialize standard Immutable lists called Tuples inside Python.
</details>

---

### 5. In Python classes, what does the `__init__` method represent?
- [ ] A) The destructor
- [ ] B) The constructor
- [ ] C) A loop generator
- [ ] D) An instance iterator

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The constructor

- **Explanation:** `__init__` declares logic triggered at instant creation instances initializing specific variable bindings supporting the newly structured class state.
</details>

---

### 6. What happens when you use the `zip()` function on two lists of different lengths in Python?
- [ ] A) It throws a `ValueError`.
- [ ] B) It pads the shorter list with `None` values.
- [ ] C) It stops aggregating tuples once the shortest list is exhausted.
- [ ] D) It cycles items from the shorter list to match the longer list.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It stops aggregating tuples once the shortest list is exhausted.

- **Explanation:** Standard `zip()` terminates aggregation alongside the exhausted boundary of the shortest referenced iterable.
</details>

---

### 7. Which operator is the standard convention for checking if a variable `v` is loaded with `None`?
- [ ] A) `v == None`
- [ ] B) `v is None`
- [ ] C) `not v`
- [ ] D) `type(v) == "None"`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `v is None`

- **Explanation:** Singletons like `None` are addressed inside memory using the identity operator `is` for faster and safer identification.
</details>

---

### 8. What is the correct Set operation to find only the elements common to both sets?
- [ ] A) `set1.union(set2)`
- [ ] B) `set1.difference(set2)`
- [ ] C) `set1.intersection(set2)`
- [ ] D) `set1.symmetric_difference(set2)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `set1.intersection(set2)`

- **Explanation:** Intersections return sets holding values that simultaneously exist across both referenced bounding groups.
</details>

---

### 9. Which method from the `datetime` module formats datetime objects into structured strings?
- [ ] A) `strptime()`
- [ ] B) `strftime()`
- [ ] C) `format()`
- [ ] D) `isoformat()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `strftime()`

- **Explanation:** `strftime` translates date instances to string output. Mnemonic: `f` stands for "Format".
</details>

---

### 10. When a child class inherits from multiple parents and encounters a common method, which rule determines whose method initializes?
- [ ] A) First In First Out (FIFO)
- [ ] B) Method Resolution Order (MRO)
- [ ] C) Local precedence rule
- [ ] D) Reverse lookup tree

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Method Resolution Order (MRO)

- **Explanation:** MRO structures lookup priorities depending on the left-to-right defined order set inside inheritance parent declaration parentheses.
</details>

---

### 11. What is the scope search order for resolving variable names in Python?
- [ ] A) Local, Global, Enclosing, Built-in
- [ ] B) Local, Enclosing, Global, Built-in
- [ ] C) Enclosing, Local, Global, Built-in
- [ ] D) Built-in, Global, Enclosing, Local

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Local, Enclosing, Global, Built-in (LEGB)

- **Explanation:** Python continuously traverses variable checks beginning containing inside loaded local segments, ascending up towards standard Built-in scopes.
</details>

---

### 12. Which exception does a custom Iterator raise to signal there are no further items left to yield?
- [ ] A) `IndexError`
- [ ] B) `StopIteration`
- [ ] C) `StopGenerator`
- [ ] D) `KeyError`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `StopIteration`

- **Explanation:** Python uses the `StopIteration` exception structure specifically built breaking iter conditions cleanly whenever values exhaust.
</details>

---

### 13. Which pillar of OOP shields internal states by forcing interactions via explicitly defined wrapper methods?
- [ ] A) Inheritance
- [ ] B) Encapsulation
- [ ] C) Abstraction
- [ ] D) Polymorphism

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Encapsulation

- **Explanation:** Encapsulation secures boundary control setups ensuring data attributes don't bypass structured valid workflows without accessor method gating.
</details>

---

### 14. What occurs if you double insert similar values inside a standard Python `set()` list?
- [ ] A) It appends values augmenting length coordinates.
- [ ] B) It ignores insertions leaving counts static.
- [ ] C) It throws item replication ValueError logic.
- [ ] D) It strips all inclusive previous archives.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It ignores insertions leaving counts static.

- **Explanation:** Sets strictly demand unique coordinates boundary logs. Replicated value updates automatically trigger silent purges keeping sets distinct continuously.
</details>

---

### 15. Standard dictionary keys in Python are bound regarding which strict specification requirement?
- [ ] A) Must represent string formats exclusively.
- [ ] B) Must represent mutable items like lists or arrays.
- [ ] C) Must represent immutable and hashable items.
- [ ] D) Cannot load integer definitions directly.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Must represent immutable and hashable items.

- **Explanation:** Dictionary hashes locate keys quickly inside memory address pointers. Constant mutability would break index pointers looking up objects.
</details>

---

### 16. In Agile, what is the role of continuous assessment inside the Daily Standup ceremony?
- [ ] A) Present completed functional demos to clients.
- [ ] B) Answer backward targets, forwards execution plans, and address blockers.
- [ ] C) Review story pointing estimation sheets.
- [ ] D) Restructure backlogs loaded via Product Owners.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Answer backward targets, forwards execution plans, and address blockers.

- **Explanation:** The daily sync answers 15-minute quick assessments: "What I did", "What am I doing", and "Any blocker gating".
</details>

---

## Part 2: Code Prediction

### 17. What does this code print?
```python
nums = [1, 2, 3, 4]
nums.append(5)
print(nums[-1])
```
- [ ] A) 1
- [ ] B) 4
- [ ] C) 5
- [ ] D) Error

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 5

- **Explanation:** `append(5)` tacks 5 on the end node. Pointer index `[-1]` reaches backwards fetching that final entry.
</details>

---

### 18. What does this code print?
```python
fruits = ["apple", "banana", "cherry"]
for index, item in enumerate(fruits):
    if index == 1:
        print(item)
```
- [ ] A) apple
- [ ] B) banana
- [ ] C) cherry

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) banana

- **Explanation:** `enumerate()` assigns 0-based counting indices. Index `0` maps to apple, Index `1` maps to banana.
</details>

---

### 19. What results from attempting this explicit casting string conversion?
```python
x = int("3.14")
print(x)
```
- [ ] A) 3
- [ ] B) 3.14
- [ ] C) ValueError
- [ ] D) TypeError

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) ValueError

- **Explanation:** `int()` expects valid integer string representation. Decimals disrupt integer notation inside string variables directly.
</details>

---

### 20. What is the output of this global scoping test?
```python
count = 0
def increment():
    global count
    count += 1

increment()
print(count)
```
- [ ] A) 0
- [ ] B) 1

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 1

- **Explanation:** `global count` instructs functions address outer-context directly inside functional assignments seamlessly.
</details>

---

### 21. What is outputted using early break loops execution?
```python
r = []
for i in range(5):
    if i == 2:
        break
    r.append(i)
print(r)
```
- [ ] A) `[0, 1, 2]`
- [ ] B) `[0, 1]`
- [ ] C) `[0]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `[0, 1]`

- **Explanation:** Loop appends 0 then 1. When hitting `i=2`, break instantly triggers exiting forwards continuous loop setups safely.
</details>

---

### 22. What results from continuous Tuple unpacking swap?
```python
x, y = (100, 200)
x, y = y, x
print(x)
```
- [ ] A) 100
- [ ] B) 200

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 200

- **Explanation:** Python loads inline packing setups enabling direct value offsets swapping continuous variable assignments flawlessly.
</details>

---

### 23. What does this membership operator code print?
```python
box = {1, 2, 3}
print(4 not in box)
```
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

- **Explanation:** Number 4 does not live inside loaded sets; asserting `not in` perfectly returns true coefficients quickly.
</details>

---

### 24. What is the list comprehension output?
```python
double = [x*2 for x in [1, 2]]
print(double)
```
- [ ] A) `[11, 22]`
- [ ] B) `[2, 4]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `[2, 4]`

- **Explanation:** Inline comprehension iterates through values 1 and 2 multiplying each directly continuous coefficients.
</details>

---

### 25. What is the dictionary get retrieval output?
```python
m = {"a": 1}
print(m.get("b", 10))
```
- [ ] A) None
- [ ] B) 10
- [ ] C) KeyError

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 10

- **Explanation:** `.get()` takes defaults loaded safe-fallbacks if targets don't maintain valid references inside hashes.
</details>

---

### 26. Output of standard list reference pointer shifts?
```python
x = [1, 2]
y = x
y.append(3)
print(len(x))
```
- [ ] A) 2
- [ ] B) 3

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 3

- **Explanation:** List updates directly propagate throughout all bound variable alias names addressing continuous memory allocations.
</details>

---

## Part 3: True / False

### 27. Story points equate exact hourly capacities.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

- **Explanation:** Story points strictly measure relative estimation coefficients only.
</details>

---

### 28. Python lists are highly mutable arrays perfectly adapting additions/manipulation continuously.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

- **Explanation:** Lists provide appending and purging frameworks easily triggered correctly.
</details>

---

### 29. A Python docstring is declared utilizing triple quotes `""" """` bound directly onto `__doc__`.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

- **Explanation:** Accessible using direct bindings loading descriptive archives quickly.
</details>

---

### 30. Standard comparison operators like `>` or membership triggers like `in` strictly resolve backwards directly as Boolean types (`True`/`False`).
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

- **Explanation:** Continuous reduction Assert logic yields strict absolute binary Assert metrics correctly.
</details>

---

### 31. In Git, performing `git commit` automatically saves changes instantly to your remote GitHub branch repository records.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

- **Explanation:** Committing strictly isolates files bound locally on users hardware. Uploads demand `git push` triggers explicitly backwards.
</details>

---

### 32. In Python, an anonymous function defined using lambda is limited to running only one single expression template.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

- **Explanation:** Lambdas strictly avoid loading continuous continuous statements inside single line functions correctly.
</details>

---

### 33. Sets maintain ordered indices coordinates, making indexing operations like `s[0]` perfectly valid.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

- **Explanation:** Sets preserve unordered bounds containing strictly unique objects avoiding bound index locations entirely.
</details>

---

## Part 4: Fill-in-the-Blank

### 34. FILL-IN-THE-BLANK
To join a branch index backwards into continuous main history nodes using Git, developers trigger `git _____ <branch-name>`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `merge`

- **Explanation:** Synthesizes parallel branches seamlessly.
</details>

---

### 35. FILL-IN-THE-BLANK
Custom iteration workflows demand attached classes support defining both `__next__` and `_____` methods.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `__iter__`

- **Explanation:** Iter object setup setups continuous consecutive values sequentially.
</details>

---

### 36. FILL-IN-THE-BLANK
The Git setup used for creating empty repositories or loading reinitializations templates focuses on `git _____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `init`

- **Explanation:** Generates `.git` configuration folders initial workspace tracks easily loaded initially.
</details>

---

### 37. FILL-IN-THE-BLANK
To explicitly cast float coefficients down towards exact integers purging decimal accuracy coordinates, use `_____()`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `int`

- **Explanation:** Truncation strips floating coordinates keeping whole digits flawlessly.
</details>

---

### 38. FILL-IN-THE-BLANK
The OOP pillar allowing child classes acquire attributes loaded via parents classes is `_____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `Inheritance`

- **Explanation:** Shares descriptive structure architectures reusing dryer blueprints without replication.
</details>
