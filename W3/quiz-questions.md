# Weekly Knowledge Check: [Week 3 SQL]

## Part 1: Multiple Choice

### 1. What is the primary purpose of an Entity Relationship Diagram (ERD)?
- [ ] A) To compile SQL commands into machine code automatically.
- [ ] B) To visualize the logical layout of tables, columns, and their relationships.
- [ ] C) To run queries against active databases to measure system performance.
- [ ] D) To backup database logs onto external server drives.

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) To visualize the logical layout of tables, columns, and their relationships.

**Explanation:** An ERD acts as a blueprint of the database design, allowing creators to map entities and connections before writing structure.
- **Why others are wrong:**
  - A) ERD is a design visualizer, not a compiler.
  - C) ERDs don't execute performance scripts.
  - D) ERDs don't manage backup procedures.
</details>

---

### 2. In SQL, which data type is generally recommended for handling high-precision financial or currency values?
- [ ] A) FLOAT
- [ ] B) DECIMAL (or NUMERIC)
- [ ] C) VARCHAR
- [ ] D) INTEGER

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) DECIMAL (or NUMERIC)

**Explanation:** DECIMAL stores accurate fractional numbers, avoiding the rounding discrepancies found in floating point types (FLOAT).
- **Why others are wrong:**
  - A) FLOAT introduces minor rounding errors due to binary representation limits.
  - C) VARCHAR is used for text, making mathematical aggregations difficult.
  - D) INTEGER cannot store decimal/cent amounts.
</details>

---

### 3. To which SQL sublanguage classification does the `TRUNCATE` command belong?
- [ ] A) DML (Data Manipulation Language)
- [ ] B) DDL (Data Definition Language)
- [ ] C) DQL (Data Query Language)
- [ ] D) TCL (Transaction Control Language)

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) DDL (Data Definition Language)

**Explanation:** `TRUNCATE` is considered structural maintenance as it resets the table and cannot be safely rolled back in standard transactional contexts like standard DML items.
- **Why others are wrong:**
  - A) DML covers rows editing (INSERT, UPDATE, DELETE).
  - C) DQL is for reading (SELECT).
  - D) TCL manages block states (COMMIT, ROLLBACK).
</details>

---

### 4. What behavior does the SQL `BETWEEN` operator exhibit regarding its specified range boundaries?
- [ ] A) It is strict and excludes both endpoints from listing.
- [ ] B) It is inclusive of both endpoints.
- [ ] C) It only operates on timestamps and rejects numeric keys.
- [ ] D) It returns invalid results if the left value exceeds the right value.

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) It is inclusive of both endpoints.

**Explanation:** Bound `X BETWEEN 10 AND 50` captures rows where X is 10, 50, or any number inside that range.
- **Why others are wrong:**
  - A) Endpoints are contained in output list match triggers.
  - C) Works easily on numbers or characters as well.
  - D) While bad order returns empty, standard behavior inclusive fact remains.
</details>

---

### 5. What is required for a table table to be compliant under First Normal Form (1NF)?
- [ ] A) Must contain zero foreign keys referencing other rows.
- [ ] B) Contains no partial dependencies in composite primary sets.
- [ ] C) All columns must accommodate atomic (indivisible) values with no repeating lists.
- [ ] D) Database triggers should trigger prior check restrictions.

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** C) All columns must accommodate atomic (indivisible) values with no repeating lists.

**Explanation:** 1NF restricts items containing arrays/separate tags bundled in one field cell.
- **Why others are wrong:**
  - A) Foreign keys are normal and allowed in 1NF.
  - B) Dependency requirement is for 2NF.
  - D) Normal forms pertain layout structure, not trigger scripts rules.
</details>

---

### 6. Which feature defines a composite key in a relational database layout?
- [ ] A) A key containing variables from separate tables side by side.
- [ ] B) A single primary key consisting of two or more combined columns together.
- [ ] C) An encrypted signature verifying backup streams.
- [ ] D) A primary key containing duplicate integers to allow repeating lists.

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) A single primary key consisting of two or more combined columns together.

**Explanation:** Composite identifiers combine multiple column tags to create a single rigid uniqueness check.
- **Why others are wrong:**
  - A) Multi-table linking references are Foreign keys, not composites themselves.
  - C) Key concepts in database layouts avoid system encryption tasks.
  - D) Primary elements never tolerate repeating duplicates.
</details>

---

### 7. Which clause should you implement to separate and filter aggregated groups AFTER grouping calculation?
- [ ] A) WHERE
- [ ] B) HAVING
- [ ] C) GROUP BY
- [ ] D) ORDER BY

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) HAVING

**Explanation:** HAVING executes following aggregate aggregation computations, filtering entire row batches based upon totals.
- **Why others are wrong:**
  - A) WHERE operates ahead of clustering, omitting individual rows item by item.
  - C) Clustering is trigger task, not filters triggers.
  - D) Sorts presentation views output rows.
</details>

---

### 8. Which condition describes an `INNER JOIN` operation result behavior?
- [ ] A) Pulls all records regardless of matching status from left set.
- [ ] B) Yields only the rows containing corresponding match values in both target sets.
- [ ] C) Generates missing tags using aggregate counters set beforehand.
- [ ] D) Eliminates table identifiers before output delivery stream starts.

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) Yields only the rows containing corresponding match values in both target sets.

**Explanation:** INNER acts strictly, dropping non-coordinated row logs missing on inner sets coordinate tags.
- **Why others are wrong:**
  - A) Pulls all describe LEFT/RIGHT behaviors.
  - C) Adds no aggregations internally automatically.
  - D) Eliminating refers view hide scripts layers trigger.
</details>

---

### 9. What core guarantee does 'Consistency' provide inside the ACID transaction standard?
- [ ] A) Prevents write corruption during continuous memory failures.
- [ ] B) Ensures database transitions strictly into valid states keeping all rules satisfied.
- [ ] C) Locks tables allowing read actions simultaneously only.
- [ ] D) Guarantees task batch operations finish completely or don't operate at all.

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) Ensures database transitions strictly into valid states keeping all rules satisfied.

**Explanation:** Ensures prior restrictions, triggers, and values rules remain integrity valid during saves.
- **Why others are wrong:**
  - A) Durability manages memory fail state scripts triggers.
  - C) Isolation governs read locks.
  - D) Atomicity supports 'all or nothing' guarantees.
</details>

---

### 10. Which SQL statement lets creators observe the query plans and performance costs calculated ahead of run tasks?
- [ ] A) ANALYZE TABLE
- [ ] B) EXPLAIN
- [ ] C) SHOW PLANNER
- [ ] D) VIEW LOGS

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) EXPLAIN

**Explanation:** Putting `EXPLAIN` ahead reveals optimizer cost scores and index search paths proposed.
- **Why others are wrong:**
  - A) Updates row statistics instead of showing layouts ahead.
  - C) Usually invalid syntax in PostgreSQL frameworks.
  - D) Loads general error buffer feeds rather cost projections.
</details>

---

## Part 2: True/False

### 11. `TRUNCATE TABLE` can be easily undone using a standard DQL `ROLLBACK` command at any time because it targets row editing data exclusively.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `TRUNCATE` is DDL (structure), which is typically auto-committed and cannot be reverted with TCL rollback blocks easily.
</details>

---

### 12. Aggregate functions like `COUNT(column_name)` ignore `NULL` fields in computation calculation.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** When targeting specific columns, aggregates compute only cells containing actual populated identifiers. `COUNT(*)` counts rows.
</details>

---

### 13. To look up missing or unpopulated fields, creators must implement equality using standard codes like `= NULL`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Standard match equations fail against unspecified null concepts. Correct syntax requires implementing `IS NULL` keywords.
</details>

---

### 14. Setting index keys can increase reading fetching rates, but generally incurs insertion slowing penalties during modifications.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Writing triggers extra update overhead tasks keeping indexing indexes accurately coordinated after new item rows append.
</details>

---

### 15. Standard VIEWS physical replicate raw datasets onto disk drive sectors with updated logs automatically.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Standard Views serve as virtual pointers carrying pre-saved query scripts runners yielding fresh retrieval every call. No physical saves happen on view pointers unless materialized sets get created.
</details>

---

## Part 3: Code Prediction

### 16. What does this SQL query evaluate returning output log count results?
```sql
-- Inventory table has 3 rows: values [10, 20, NULL]
SELECT COUNT(*) FROM inventory;
```
- [ ] A) 2
- [ ] B) 3
- [ ] C) 0
- [ ] D) Error

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) 3

**Explanation:** `COUNT(*)` outputs the absolute row row counts ignoring column variables content.
</details>

---

### 17. What does this check evaluate returning?
```sql
-- Under case-sensitive engine limits
SELECT 'apple' LIKE 'A%';
```
- [ ] A) True (1)
- [ ] B) False (0)
- [ ] C) Error syntax

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) False (0)

**Explanation:** `LIKE` applies case-aware searching coordinate constraints. For case-ignoring results practitioners must use `ILIKE` (Postgres specific) or adjust casing setups.
</details>

---

### 18. Determine final row counts results based upon joining coordinates below:
```sql
-- tableA contains 3 rows: [A, B, C]
-- tableB contains 1 row: [A]
SELECT * FROM tableA LEFT JOIN tableB ON tableA.id = tableB.id;
```
- [ ] A) 1
- [ ] B) 2
- [ ] C) 3
- [ ] D) 4

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** C) 3

**Explanation:** LEFT JOIN yields everything from primary left lists coordination including coordinates failing coordinate matching coordinates.
</details>

---

## Part 4: Fill-in-the-Blank

### 19. The sublanguage ensuring access lock states, backup feeds, or rolling back data grouped atomic frames is called Transaction _____ Language.
- [ ] A) Data
- [ ] B) Control
- [ ] C) Modification
- [ ] D) Query

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) Control (TCL)

**Explanation:** TCL manages locks, commits edits to disk drive sectors or resets failed setups securely correctly.
</details>

---

### 20. The wildcard tags used inside pattern matching `LIKE` standing precisely for ONE single character representation placeholder is the _____ character symbol.
- [ ] A) %
- [ ] B) _
- [ ] C) *
- [ ] D) ?

<details>
<summary><b>Click for Solution</b></summary>

**Correct Answer:** B) _ (Underscore)

**Explanation:** Underscore marks exact slot placeholder triggers, while Percent denotes any string length slot match streams.
</details>
