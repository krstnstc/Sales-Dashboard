import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_data(num_customers=1000, num_products=50, num_orders=5000, start_date='2023-01-01', end_date='2024-12-31'):
    # Create output directory if it doesn't exist
    os.makedirs('data/raw', exist_ok=True)
    
    # Generate date range
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    date_range = end_date - start_date
    
    # Generate customer data
    customer_ids = [f'CUST{str(i).zfill(5)}' for i in range(1, num_customers + 1)]
    customer_join_dates = [start_date + timedelta(days=np.random.randint(0, date_range.days)) for _ in range(num_customers)]
    
    customers_df = pd.DataFrame({
        'CustomerID': customer_ids,
        'Name': [f'Customer {i}' for i in range(1, num_customers + 1)],
        'Email': [f'customer{i}@example.com' for i in range(1, num_customers + 1)],
        'JoinDate': customer_join_dates,
        'LastPurchaseDate': [date + timedelta(days=np.random.randint(0, (end_date - date).days)) 
                           for date in customer_join_dates]
    })
    
    # Generate product data
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports', 'Beauty', 'Toys']
    product_names = [
        'Wireless Earbuds', 'Smart Watch', 'Laptop', 'Smartphone', 'Headphones',
        'T-Shirt', 'Jeans', 'Dress', 'Sneakers', 'Jacket',
        'Coffee Maker', 'Air Fryer', 'Blender', 'Knife Set', 'Cookware Set',
        'Novel', 'Textbook', 'Cookbook', 'Biography', 'Science Fiction',
        'Yoga Mat', 'Dumbbells', 'Running Shoes', 'Basketball', 'Bicycle'
    ]
    
    products_df = pd.DataFrame({
        'ProductID': [f'PROD{str(i).zfill(5)}' for i in range(1, num_products + 1)],
        'Category': np.random.choice(categories, size=num_products, p=[0.2, 0.15, 0.15, 0.1, 0.1, 0.15, 0.15]),
        'ProductName': np.random.choice(product_names, size=num_products, replace=True),
        'Cost': np.random.uniform(5, 500, num_products).round(2),
        'Price': np.random.uniform(10, 1000, num_products).round(2)
    })
    
    # Generate sales data
    order_ids = [f'ORD{str(i).zfill(6)}' for i in range(1, num_orders + 1)]
    order_dates = [start_date + timedelta(days=np.random.randint(0, date_range.days)) for _ in range(num_orders)]
    regions = ['North', 'South', 'East', 'West']
    
    sales_data = []
    for order_id, order_date in zip(order_ids, order_dates):
        customer_id = np.random.choice(customer_ids)
        product = products_df.sample(1).iloc[0]
        quantity = np.random.randint(1, 5)
        unit_price = product['Price'] * (1 - np.random.uniform(0, 0.3))  # Apply random discount
        region = np.random.choice(regions)
        
        sales_data.append({
            'OrderID': order_id,
            'CustomerID': customer_id,
            'OrderDate': order_date.strftime('%Y-%m-%d'),
            'ProductID': product['ProductID'],
            'Quantity': quantity,
            'UnitPrice': round(unit_price, 2),
            'Region': region
        })
    
    sales_df = pd.DataFrame(sales_data)
    
    # Save data to CSV files
    sales_df.to_csv('data/raw/sales_data.csv', index=False)
    customers_df.to_csv('data/raw/customers.csv', index=False)
    products_df.to_csv('data/raw/products.csv', index=False)
    
    print(f"Generated {len(sales_df)} sales records for {len(customers_df)} customers and {len(products_df)} products.")

if __name__ == "__main__":
    generate_sample_data()
