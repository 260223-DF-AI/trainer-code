# Exercise: Database Design Challenge

## Overview

In this exercise, you will design an Entity-Relationship Diagram (ERD) for a given business scenario. This is a **Conceptual** exercise focusing on data modeling skills.

**Estimated Time:** 2-3 hours

---

## The Scenario

You have been hired as a database architect for **BookBuddy**, a new online bookstore. The business has provided you with the following requirements:

### Business Requirements

1. **Customers** can register with their name, email, phone, and address
2. **Books** have a title, ISBN, price, publication date, and page count
3. Each book belongs to exactly one **Publisher** (with name and contact info)
4. Each book can have multiple **Authors** (with name and bio)
5. An author can write multiple books
6. Customers can place **Orders**
7. Each order can contain multiple books with different quantities
8. Orders have a status (pending, shipped, delivered, cancelled)
9. Customers can write **Reviews** for books they've purchased
10. Reviews have a rating (1-5) and optional text

---

## Deliverables

### Part 1: Entity Identification (30 minutes)

Create a table listing all entities and their attributes:

| Entity | Attributes | Primary Key |
|--------|------------|-------------|
| ? | ? | ? |

**Hint:** You should identify at least 6-7 entities.

### Part 2: Relationship Mapping (30 minutes)

For each relationship between entities, identify:

1. The two entities involved
2. The relationship type (1:1, 1:M, M:N)
3. Whether a junction table is needed
4. Participation constraints (optional vs mandatory)

Example format:

```
Publisher → Books: ONE-TO-MANY (1:M)
- One publisher has many books
- A book must have one publisher
- No junction table needed
```

### Part 3: ERD Diagram (45 minutes)

Create a visual ERD diagram using one of these methods:

1. **Hand-drawn** on paper (take a photo to submit)
2. **Mermaid notation** using the template in `templates/erd-template.mermaid`
3. **Draw.io/Lucidchart** or similar tool

Your diagram must include:

- [ ] All entities as boxes/rectangles
- [ ] Primary keys marked (PK)
- [ ] Foreign keys marked (FK)
- [ ] Relationship lines with cardinality notation
- [ ] Junction tables for M:N relationships

### Part 4: SQL Schema Preview (30 minutes)

Write CREATE TABLE statements for **3 of your entities** (your choice), including:

- Appropriate data types
- PRIMARY KEY constraints
- FOREIGN KEY references
- NOT NULL where appropriate

```sql
-- Your SQL here
CREATE TABLE ...
```

---

## Evaluation Criteria

Your design will be evaluated on:

| Criterion | Points |
|-----------|--------|
| Correct entity identification | 20 |
| Accurate relationship mapping | 25 |
| Complete ERD with all elements | 30 |
| Valid SQL syntax | 15 |
| Clear documentation | 10 |
| **Total** | **100** |

---

## Submission

1. Complete the deliverables in a document or markdown file
2. If using paper, include clear photos of your diagrams
3. Submit to the designated folder by end of day

---

## Hints

<details>
<summary>Click for hints (try first without!)</summary>

**Entity Hints:**

- Don't forget about junction tables for many-to-many relationships
- Think about what links Orders to Books

**Common Mistakes:**

- Putting author directly in the Books table (wrong for M:N)
- Missing the junction table for order items
- Forgetting reviews need to reference both customer AND book

</details>

---

## Bonus Challenge

If you finish early, consider:

1. How would you handle book categories/genres?
2. What indexes would improve performance?
3. How would you track inventory levels?
