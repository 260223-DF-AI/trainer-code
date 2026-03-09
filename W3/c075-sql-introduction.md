# SQL Introduction

## Learning Objectives

- Understand what SQL is and its role in data management
- Learn the history and evolution of SQL
- Recognize why SQL remains essential for modern data work
- Identify common use cases for SQL in industry

## Why This Matters

As you begin your journey into relational databases, SQL (Structured Query Language) becomes your primary tool for communicating with data. In the world of Data Foundations, nearly every data-related role requires SQL proficiency. Whether you are analyzing business metrics, building data pipelines, or developing applications, SQL provides the universal language for accessing and manipulating structured data.

## The Concept

### What is SQL?

SQL stands for **Structured Query Language**. It is a standardized programming language designed specifically for managing and manipulating relational databases. Unlike general-purpose programming languages like Python (which you learned in Weeks 1 and 2), SQL is a **domain-specific language** focused entirely on database operations.

SQL allows you to:

- **Create** database structures (tables, schemas, views)
- **Insert** new data into databases
- **Query** and retrieve specific data
- **Update** existing records
- **Delete** data when needed
- **Control** access permissions

### A Brief History

SQL was developed at IBM in the early 1970s by Donald D. Chamberlin and Raymond F. Boyce. Originally called SEQUEL (Structured English Query Language), it was designed to manipulate and retrieve data stored in IBM's System R, one of the first relational database prototypes.

Key milestones:

- **1970**: Edgar F. Codd publishes the relational model theory
- **1974**: SEQUEL developed at IBM
- **1979**: Oracle releases first commercial SQL database
- **1986**: SQL becomes ANSI standard
- **1987**: SQL becomes ISO standard
- **Present**: SQL continues evolving with SQL:2016, SQL:2023 standards

### Why SQL Endures

Despite being over 50 years old, SQL remains the industry standard because:

1. **Declarative Nature**: You describe *what* you want, not *how* to get it
2. **Standardization**: Core syntax works across different database systems
3. **Optimization**: Database engines optimize query execution automatically
4. **Widespread Adoption**: Every major company uses SQL databases
5. **Integration**: Works with virtually every programming language

### SQL in the Data Ecosystem

```
+-------------------+       +-------------------+       +-------------------+
|   Applications    | <---> |   SQL Database    | <---> |   Data Analysis   |
|   (Python, Java)  |       |   (PostgreSQL)    |       |   (Reports, BI)   |
+-------------------+       +-------------------+       +-------------------+
                                     ^
                                     |
                                     v
                            +-------------------+
                            |   Data Pipelines  |
                            |   (ETL/ELT)       |
                            +-------------------+
```

SQL serves as the common interface between applications, analytics tools, and data pipelines.

## Code Example

Here is a simple SQL query that retrieves data from a table:

```sql
-- Select all employees from the employees table
SELECT first_name, last_name, department
FROM employees
WHERE department = 'Engineering'
ORDER BY last_name;
```

This query demonstrates SQL's readable, English-like syntax:

- `SELECT`: Specify which columns to retrieve
- `FROM`: Identify the table
- `WHERE`: Filter the results
- `ORDER BY`: Sort the output

## Key Takeaways

- SQL is the standard language for relational database management
- It is declarative: you describe results, not procedures
- SQL has been an ANSI/ISO standard since the 1980s
- Core SQL skills transfer across different database systems
- SQL remains essential for data engineering, analysis, and development

## Additional Resources

- [W3Schools SQL Tutorial](https://www.w3schools.com/sql/) - Interactive beginner tutorials
- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/) - Comprehensive reference
- [SQL Standard Wikipedia](https://en.wikipedia.org/wiki/SQL) - History and evolution
