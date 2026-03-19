USERS

|user_id (PK)|user_fName|user_lname|phone_num|email|city|state|  
|----|----|----|----|----|----|----|
| 1 | dylan | parrott | 5550u812 | no@gmail.com | Chicago | IL |



TRANSACTIONS
| trans_id (PK)| user_id (FK) | trans_date | trans_location | trans_total |
|----|----|----|----|----|
| 1 | 1 | 2026-03-19 | Chicago, IL | $59.99 |


```sql
IF NOT EXISTS (SELECT 1 FROM USERS WHERE user_id = <incoming_user>)

BEGIN
    INSERT INTO USERS (user_fname, user_lname, phone_num, email, city, state)
    VALUE (.........)
END

tmp_userID = SELECT user_id FROM USERS WHERE user = incoming_user

INSERT INTO TRANSACTIONS (trans_id, user_id, trans_date, trans_locaion, trans_total)
VALUE( ....... )
```
