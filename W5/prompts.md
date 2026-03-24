Define the role:
Be direct about the result you want:
Provide context:
Template example:
Constraints:

Zero-Shot:

Write me a BigQuery statement.
- Gemini had the most useful content, Claude provided the best opportunity to refine the request

Write me a BigQuery SQL query to get the top 20 rows of the purchase table. The table has clumns order_id, customer_id, order_date, otder_total? Order results by order_total.
- Claude was direct, Gemini and ChatGPT were about on par with slightly more contextual info.


You are a BigQuery SQL expert developer.
Write me a BigQuery SQL query to get the top 20 rows of the purchase table from the store_data dataset. The table has columns order_id, customer_id, order_date, order_total? Alias each column to be more human-readable. Order results by order_total. Explain your reasoning, and why you wrote the query as you have.



You are a BigQuery SQL expert developer.

Write me a BigQuery SQL query to get the top 20 rows.

Table: store_data.purchase
Columns: order_id (INT64), customer_id (INT64), order_date (DATE), order_total (NUMERIC)

Alias each column to be more human-readable. Order results by order_total. Explain your reasoning, and why you wrote the query as you have.



Show me how to use the BigQuery python client to create a table with row-level security policies and column-level access controls.




Write a BigQuery SQL query that performs RFM 
(Recency, Frequency, Monetary) customer segmentation.

Table: analytics.orders
Columns:
- order_id (INT64)
- customer_id (INT64)  
- order_date (DATE)
- total_amount (NUMERIC)

Requirements:
- Calculate days since last order (Recency)
- Count total orders (Frequency)
- Sum total amount (Monetary)
- Assign 1-5 scores using NTILE for each metric
- Concatenate into a 3-digit RFM segment
- Order by monetary score descending


| Criteria | Gemini | Claude | ChatGPT |
| -------- | ------ | ------ | ------- |
| formatting | 1 | 1 | 1 |
| relevance | 2 | 1 | 1 |
| verbosity | 1 | 2 | 1 |
| duration | 1 | 2 | 1 |
| availability | 1 | 2 | 1 |
| - | - | - | - |
| optimized result | 2 | 1 | 1 |
| accuracy | 1 | 1 | 1 |
| completeness | 1 | 1 | 1 |
| commenting/docs | 1 | 1 | 1 |
| convention | 1 | 1 | 1 |

