SELECT
    c.customer_name,
    c.email,
    c.city,
    o.order_id,
    o.order_date,
    o.total_amount,
    p.product_name,
    p.category,
    p.unit_price
FROM `project.analytics.orders` o
INNER JOIN `project.analytics.customers` c ON o.customer_id = c.customer_id
INNER JOIN `project.analytics.products` p ON o.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
AND o.order_date <= '2024-12-31'
AND p.category = 'Electronics'
ORDER BY o.total_amount DESC









def get_customer_summary(file_path):
    """
    Reads a CSV file and returns a list of dictionaries summarizing customer
    orders.

    The CSV file is expected to have the following columns:
    - customer_id
    - order_date
    - total_amount

    The function returns a list of dictionaries, each containing the following
    fields:
    - customer_id
    - total (the total amount of all orders for the customer)
    - count (the number of orders for the customer)
    - last_date (the date of the latest order for the customer)

    :param file_path: The path to the CSV file
    :return: A list of dictionaries summarizing customer orders
    """
    import csv
    try:
        results = {}
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            # Skip the header row
            header = next(reader)
            for row in reader:
                customer_id = row[0]
                if customer_id is None:
                    raise ValueError("Customer ID cannot be null")
                amount = float(row[3])
                if amount is None:
                    raise ValueError("Total amount cannot be null")
                date = row[2]
                if date is None:
                    raise ValueError("Order date cannot be null")
                if customer_id not in results:
                    # Initialize a new customer
                    results[customer_id] = {
                        'total': amount,
                        'count': 1,
                        'last_date': date
                    }
                else:
                    # Update the existing customer
                    results[customer_id]['total'] += amount
                    results[customer_id]['count'] += 1
                    if date > results[customer_id]['last_date']:
                        results[customer_id]['last_date'] = date
        return list(results.values())
    except FileNotFoundError:
        print(f"Error: Could not open file at {file_path}")
        return []
    except ValueError as e:
        print(f"Error: {e}")
        return []
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return []





import pandas as pd

def calculate_order_total(orders_df):
    """
    Calculate total per order including tax.

    This function takes a dataframe containing order information and calculates
    the total for each order. It does this by:

    1. Calculating the total for each line item (quantity x unit_price)
    2. Calculating the tax for each line item (line_total x 0.08)
    3. Calculating the total for each line item including tax (line_total + tax)
    4. Grouping the dataframe by order_id and calculating the subtotal,
       total tax, and grand total for each order.
    """
    orders_df['line_total'] = orders_df['quantity'] * orders_df['unit_price']
    orders_df['tax'] = orders_df['line_total'] * 0.08
    orders_df['line_with_tax'] = orders_df['line_total'] + orders_df['tax']
    
    totals = orders_df.groupby('order_id').agg(
        subtotal=('line_total', 'sum'),
        total_tax=('tax', 'sum'),
        grand_total=('line_with_tax', 'sum')
    ).reset_index()
    
    return orders_df, totals
