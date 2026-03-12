-- Active: 1773160159958@@127.0.0.1@5432@procedures
CREATE DATABASE procedures;

-- Create sample tables
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0 CHECK (balance >= 0)
);

CREATE TABLE transactions (
    txn_id SERIAL PRIMARY KEY,
    from_account INTEGER,
    to_account INTEGER,
    amount DECIMAL(10, 2),
    txn_date TIMESTAMP DEFAULT NOW(),
    description VARCHAR(200)
);

-- Insert sample data
INSERT INTO accounts (name, balance) VALUES
('Alice', 1000.00),
('Bob', 500.00),
('Carol', 1500.00);

SELECT * FROM accounts;

CREATE OR REPLACE FUNCTION get_balance(p_account_id INTEGER)
    RETURNS DECIMAL(10, 2) AS $$
BEGIN
    RETURN (
        SELECT balance
        FROM accounts
        WHERE accounts.account_id = p_account_id
    );
END;
$$ LANGUAGE plpgsql;

SELECT get_balance(2);
SELECT get_balance(1);

SELECT name, get_balance(account_id) AS balance
    FROM accounts;  


CREATE OR REPLACE FUNCTION get_accounts_above(p_min_balance DECIMAL)
    RETURNS TABLE (
        account_id INTEGER,
        name VARCHAR,
        balance DECIMAL
    ) AS $$
BEGIN
    RETURN QUERY
        SELECT a.account_id, a.name, a.balance
        FROM accounts AS a
        WHERE a.balance > p_min_balance
        ORDER BY a.balance DESC;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_accounts_above(750);

SELECT * FROM accounts;

CREATE OR REPLACE PROCEDURE transfer_funds (
    p_from_account INTEGER,
    p_to_account INTEGER,
    p_amount DECIMAL,
    p_description VARCHAR DEFAULT 'Transfer'
)
LANGUAGE plpgsql AS $$
DECLARE
    source_balance DECIMAL;
BEGIN
    SELECT balance INTO source_balance
        FROM accounts
        WHERE account_id = p_from_account;

    IF source_balance < p_amount THEN
        RAISE EXCEPTION 'Insufficient funds';
    END IF;

    UPDATE accounts
        SET balance = balance - p_amount
        WHERE account_id = p_from_account;

    UPDATE accounts
        SET balance = balance + p_amount
        WHERE account_id = p_to_account;
    
    INSERT INTO transactions(from_account, to_account, amount, description)
        VALUES (p_from_account, p_to_account, p_amount, p_description);
END;
$$;

SELECT * FROM accounts;
SELECT * FROM transactions;
CALL transfer_funds(3, 2, 500, 'Paid for rent.');