-- Active: 1773160159958@@127.0.0.1@5432@chinook
-- Parking Lot*******
-- *                *
-- *                *
--- *****************

-- SETUP:
-- Connect to the server (Azure Data Studio / Database extension/psql)
-- Create a database (I recommend chinook_pg)
-- Execute the Chinook database (from the Chinook_pg.sql file) to create Chinook resources in your server (I recommend doing this from psql)

-- Comment can be done single line with --
-- Comment can be done multi line with /* */

/*
DQL - Data Query Language
Keywords:

SELECT - retrieve data, select the columns from the resulting set
FROM - the table(s) to retrieve data from
WHERE - a conditional filter of the data
GROUP BY - group the data based on one or more columns
HAVING - a conditional filter of the grouped data
ORDER BY - sort the data
*/

SELECT * FROM actor;
SELECT last_name FROM actor;
SELECT * FROM actor WHERE first_name = 'Morgan';
select * from actor where first_name = 'John';

-- BASIC CHALLENGES
-- List all customers (full name, customer id, and country) who are not in the USA
SELECT first_name || ' ' || last_name AS full_name, customer_id, country FROM customer
WHERE NOT country = 'USA';  

-- List all customers from Brazil
SELECT first_name, last_name, customer_id, country FROM customer
WHERE country = 'Brazil';

-- List all sales agents
-- select concat(first_name, ' ', last_name) as full_name, employee_id, title from employee where title like 'Sales%';
select concat(first_name, ' ', last_name) as full_name, employee_id, title from employee where title = 'Sales Support Agent';

-- Retrieve a list of all countries in billing addresses on invoices
SELECT DISTINCT billing_country -- only showing distinct values! 
FROM invoice;

-- Retrieve how many invoices there were in 2009, and what was the sales total for that year?
SELECT COUNT(*), SUM(total) FROM invoice WHERE invoice_date >= '2009-01-01' AND invoice_date < '2010-01-01';

-- What table has the info i need?
-- What specifically from the table has the data i need?
-- how do we filter out the things I DON'T care about?
-- how do I SELECT/present the data thati have left?

-- SELECT * FROM invoice
-- SELECT * FROM invoice WHERE invoice_date >= '2009-01-01' AND invoice_date < '2010-01-01';
-- SELECT Count(*) FROM ...


-- (challenge: find the invoice count sales total for every year using one query)
SELECT COUNT(*), SUM(total), EXTRACT(YEAR FROM invoice_date) FROM invoice
GROUP BY EXTRACT(YEAR FROM invoice_date);

-- SELECT invoice_date FROM invoice

-- how many line items were there for invoice #37
SELECT SUM(quantity) FROM invoice_line
WHERE invoice_id = 37;

SELECT Count(*) FROM invoice_line
WHERE invoice_id = 37;

SELECT * FROM invoice_line
WHERE invoice_id = 37;

-- how many invoices per country? BillingCountry  # of invoices -
-- Retrieve the total sales per country, ordered by the highest total sales first.
SELECT billing_country, COUNT(billing_country), SUM(total) FROM invoice GROUP BY billing_country ORDER BY SUM(total) DESC;



-- JOINS CHALLENGES
-- Every Album by Artist
SELECT a.title AS album_name, ar.name AS artist_name FROM album AS a JOIN artist ar ON a.artist_id = ar.artist_id;

-- (inner keyword is optional for inner join)
-- All songs of the rock genre
-- SeLect * AS tr
SELECT t.name AS song_name, g.name AS genre_name 
FROM track t 
JOIN genre g ON t.genre_id = g.genre_id 
WHERE g.name = 'Rock';

-- Show all invoices of customers from brazil (mailing address not billing)
SELECT invoice.invoice_id, invoice.customer_id, invoice.invoice_date, invoice.total, customer.country 
FROM customer 
JOIN invoice ON customer.customer_id = invoice.customer_id
WHERE customer.country = 'Brazil';

-- Show all invoices together with the name of the sales agent for each one
SELECT invoice.invoice_id, invoice.customer_id, employee.employee_id, invoice.invoice_date, invoice.total, employee.first_name, employee.last_name 
FROM customer
JOIN invoice ON customer.customer_id = invoice.customer_id
JOIN employee ON customer.support_rep_id = employee.employee_id;

-- Which sales agent made the most sales in 2009?
SELECT e.first_name
FROM invoice i
    JOIN customer c ON i.customer_id = c.customer_id
        JOIN employee e ON e.employee_id = c.support_rep_id
WHERE EXTRACT(YEAR FROM i.invoice_date) = 2009
GROUP BY e.employee_id
LIMIT 1;

-- How many customers are assigned to each sales agent?
SELECT COUNT(*) AS customer_count, e.first_name || ' ' || e.last_name AS agent_name, e.employee_id AS agent_emp_id
FROM customer c
JOIN employee e ON e.employee_id = c.support_rep_id
GROUP BY e.employee_id;

-- A | B   
-- 1 | 1
-- 1 | 2
-- 1 | 3
-- 2 | 3

-- B | C
-- 1 | 1
-- 1 | 2
-- 1 | 3
-- 2 | 3

-- A | B | C
-- 1 | 1 | 1
-- 1 | 1 | 2
-- 1 | 1 | 3
-- 1 | 2 | 3
-- 1 | 3 |
-- 2 | 3 | 



-- Which track was purchased the most in 2010?
SELECT track.name, SUM(invoice_line.quantity) AS total_sold
    FROM track
    JOIN invoice_line on track.track_id = invoice_line.track_id
    JOIN invoice ON invoice.invoice_id = invoice_line.invoice_id
    WHERE EXTRACT(YEAR FROM invoice.invoice_date) = 2010
    GROUP BY track.name
    ORDER BY SUM(invoice_line.quantity) DESC, track.name ASC
    LIMIT 1;
  

-- QUANTITY of the track purchased in 2010

-- Show the top three best selling artists.


-- Which customers have the same initials as at least one other customer?
select concat(c.first_name, ' ', c.last_name) as full_name, concat(c1.first_name, ' ', c1.last_name) as other_name 
    from customer as c 
        join customer as c1 
            on left(c.first_name, 1) || left(c.last_name, 1) = left(c1.first_name, 1) || left(c1.last_name, 1) 
            -- and c.first_name || c.last_name <> c1.first_name || c1.last_name; -- != <> means not equal
            and c.customer_id <> c1.customer.id;
A                   B
id | customer       id | customer

AB
A.id | A.customer | B.id | B.customer
1 | John Smith | 1 | John Smith
1 | John Smith | 3 | John Smith
1 | John Smith | 2 | Jane Smithe


-- Which countries have the most invoices?


-- Which city has the customer with the highest sales total?


-- Who is the highest spending customer?


-- Return the email and full name of of all customers who listen to Rock.


-- Which artist has written the most Rock songs?


-- Which artist has generated the most revenue?




-- ADVANCED CHALLENGES
-- solve these with a mixture of joins, subqueries, CTE, and set operators.
-- solve at least one of them in two different ways, and see if the execution
-- plan for them is the same, or different.

-- 1. which artists did not make any albums at all?

SELECT a.name from artist ar left join album al oN ar.artist_id = al.artist_id WHERE al.album_id IS NULL;
--could do outer join too

-- 2. which artists did not record any tracks of the Latin genre?
SELECT DISTINCT a.name 
    from artist a WHERE a.artist_id NOT IN(
    -- gets everything that is latin
        SELECT DISTINCT a.artist_id 
        FROM artist ar
            join album al on ar.artist_id = al.artist_id
            JOIN track t on t.album_id = al.album_id
            JOin genre g ON t.genre_id = g.genre_id 
        WHERE g.name == 'Latin'
);

SELECT invoice.invoice_count, invoice.customer_id, customer.first_name
    FROM (
        SELECT count(invoice_id) AS invoice_count, customer_id
            FROM invoice
            GROUP BY (customer_id)
    ) AS invoice
    JOIN customer ON customer.customer_id = invoice.customer_id;

-- 3. which video track has the longest length? (use media type table)


-- 4. boss employee (the one who reports to nobody)
SELECT 'Boss ' || first_name || ' ' || last_name big_boss_name
FROM employee
WHERE reports_to IS NULL;

-- 5. how many audio tracks were bought by German customers, and what was
--    the total price paid for them?


-- 6. list the names and countries of the customers supported by an employee
--    who was hired younger than 35.


-- DML exercises

-- 1. insert two new records into the employee table.


-- 2. insert two new records into the tracks table.


-- 3. update customer Aaron Mitchell's name to Robert Walter


-- 4. delete one of the employees you inserted.


-- 5. delete customer Robert Walter.
