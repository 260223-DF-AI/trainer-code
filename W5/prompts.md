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