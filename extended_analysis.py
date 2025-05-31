import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
from scipy.stats import pearsonr
import plotly.express as px

# Create extended results directory
os.makedirs('results/extended', exist_ok=True)

def create_heatmap_correlations():
    """Create correlation heatmap between key metrics"""
    # Load necessary data
    sales_df = pd.read_csv('data/processed/processed_sales.csv')
    products_df = pd.read_csv('data/processed/processed_products.csv')
    segments_df = pd.read_csv('data/processed/customer_segments.csv')
    
    # Merge data
    merged_df = pd.merge(sales_df, products_df, on='ProductID')
    merged_df = pd.merge(merged_df, segments_df, on='CustomerID')
    
    # Calculate metrics
    metrics = merged_df.groupby('CustomerID').agg({
        'TotalPrice': 'sum',
        'Quantity': 'sum',
        'Recency': 'first',
        'Frequency': 'first',
        'Monetary': 'first',
        'Churn': 'first'
    }).reset_index()
    
    # Remove non-numeric columns
    numeric_metrics = metrics.select_dtypes(include=[np.number])
    
    # Calculate correlation matrix
    corr_matrix = numeric_metrics.corr()
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix of Key Metrics')
    plt.tight_layout()
    plt.savefig('results/extended/correlation_heatmap.png')
    plt.close()

def create_product_performance_dashboard():
    """Create interactive product performance dashboard"""
    # Load data
    sales_df = pd.read_csv('data/processed/processed_sales.csv')
    products_df = pd.read_csv('data/processed/processed_products.csv')
    
    # Merge data
    product_performance = pd.merge(sales_df, products_df, on='ProductID')
    
    # Calculate metrics
    product_metrics = product_performance.groupby(['Category', 'ProductName']).agg({
        'Quantity': 'sum',
        'TotalPrice': 'sum',
        'UnitPrice': 'mean'
    }).reset_index()
    
    # Create interactive dashboard using Plotly
    fig = px.scatter(
        product_metrics,
        x='Quantity',
        y='TotalPrice',
        size='UnitPrice',
        color='Category',
        hover_name='ProductName',
        title='Product Performance Dashboard'
    )
    
    # Save as HTML
    fig.write_html('results/extended/product_performance.html')

def create_customer_ltv_analysis():
    """Create customer lifetime value analysis"""
    # Load data
    sales_df = pd.read_csv('data/processed/processed_sales.csv')
    customers_df = pd.read_csv('data/processed/processed_customers.csv')
    
    # Calculate customer LTV
    customer_ltv = sales_df.groupby('CustomerID').agg({
        'TotalPrice': 'sum',
        'OrderDate': ['min', 'max']
    }).reset_index()
    
    customer_ltv.columns = ['CustomerID', 'TotalRevenue', 'FirstPurchase', 'LastPurchase']
    
    # Calculate purchase period
    customer_ltv['PurchasePeriod'] = (pd.to_datetime(customer_ltv['LastPurchase']) - 
                                    pd.to_datetime(customer_ltv['FirstPurchase'])).dt.days
    
    # Calculate average revenue per day
    customer_ltv['RevenuePerDay'] = customer_ltv['TotalRevenue'] / customer_ltv['PurchasePeriod']
    
    # Create histogram
    plt.figure(figsize=(12, 6))
    sns.histplot(data=customer_ltv, x='RevenuePerDay', bins=50)
    plt.title('Customer Revenue per Day Distribution')
    plt.xlabel('Average Revenue per Day')
    plt.ylabel('Number of Customers')
    plt.tight_layout()
    plt.savefig('results/extended/customer_ltv.png')
    plt.close()

def create_time_series_forecast():
    """Create time series forecast for sales"""
    # Load sales data
    sales_df = pd.read_csv('data/processed/processed_sales.csv')
    
    # Convert to datetime
    sales_df['OrderDate'] = pd.to_datetime(sales_df['OrderDate'])
    
    # Calculate daily sales
    daily_sales = sales_df.groupby('OrderDate')['TotalPrice'].sum().reset_index()
    
    # Create rolling average
    daily_sales['RollingMean'] = daily_sales['TotalPrice'].rolling(window=7, min_periods=1).mean()
    
    # Create forecast plot
    plt.figure(figsize=(15, 6))
    plt.plot(daily_sales['OrderDate'], daily_sales['TotalPrice'], label='Actual Sales')
    plt.plot(daily_sales['OrderDate'], daily_sales['RollingMean'], label='7-day Rolling Mean', color='orange')
    plt.title('Sales Time Series with Rolling Average')
    plt.xlabel('Date')
    plt.ylabel('Total Sales')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('results/extended/sales_forecast.png')
    plt.close()

def create_marketing_segmentation():
    """Create marketing segmentation analysis"""
    # Load data
    segments_df = pd.read_csv('data/processed/customer_segments.csv')
    
    # Create marketing segments based on RFM
    conditions = [
        (segments_df['Recency'] < 30) & (segments_df['Frequency'] > 5) & (segments_df['Monetary'] > segments_df['Monetary'].quantile(0.75)),
        (segments_df['Recency'] < 60) & (segments_df['Frequency'] > 3) & (segments_df['Monetary'] > segments_df['Monetary'].quantile(0.5)),
        (segments_df['Recency'] > 90) & (segments_df['Frequency'] < 2) & (segments_df['Monetary'] < segments_df['Monetary'].quantile(0.25))
    ]
    
    values = ['High Value', 'Medium Value', 'Low Value']
    
    # Create new dataframe to store marketing segments
    marketing_segments = segments_df.copy()
    marketing_segments['MarketingSegment'] = np.select(conditions, values, default='Regular')
    
    # Create segment distribution
    plt.figure(figsize=(12, 6))
    sns.countplot(data=marketing_segments, x='MarketingSegment')
    plt.title('Marketing Segmentation Distribution')
    plt.xlabel('Marketing Segment')
    plt.ylabel('Number of Customers')
    plt.tight_layout()
    plt.savefig('results/extended/marketing_segments.png')
    plt.close()
    
    # Save the segmented data
    marketing_segments.to_csv('results/extended/customer_segments_marketing.csv', index=False)
    
    return marketing_segments

def create_extended_summary():
    """Create extended analysis summary"""
    # Load all data
    sales_df = pd.read_csv('data/processed/processed_sales.csv')
    products_df = pd.read_csv('data/processed/processed_products.csv')
    segments_df = pd.read_csv('data/processed/customer_segments.csv')
    
    # Load marketing segments
    marketing_segments = pd.read_csv('results/extended/customer_segments_marketing.csv')
    
    # Calculate extended metrics
    # Product performance metrics
    product_metrics = pd.merge(sales_df, products_df, on='ProductID')
    product_performance = product_metrics.groupby('Category').agg({
        'TotalPrice': 'sum',
        'Quantity': 'sum',
        'UnitPrice': 'mean'
    }).reset_index()
    
    # Customer metrics
    customer_metrics = sales_df.groupby('CustomerID').agg({
        'TotalPrice': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    # Marketing segment counts
    segment_counts = marketing_segments['MarketingSegment'].value_counts()
    
    # Write summary
    with open('results/extended/extended_analysis_summary.txt', 'w') as f:
        f.write("Extended Sales and Customer Analysis Summary\n")
        f.write("-" * 50 + "\n\n")
        
        f.write("Product Performance Analysis:\n")
        f.write("- Top 3 Categories by Revenue:\n")
        for i, (category, revenue) in enumerate(product_performance.nlargest(3, 'TotalPrice')[['Category', 'TotalPrice']].values):
            f.write(f"  {i+1}. {category}: ${revenue:,.2f}\n")
        
        f.write("\nCustomer Segmentation Analysis:\n")
        f.write(f"- Total Customers: {len(customer_metrics)}\n")
        f.write(f"- Average Revenue per Customer: ${customer_metrics['TotalPrice'].mean():,.2f}\n")
        f.write(f"- Average Order Quantity: {customer_metrics['Quantity'].mean():,.2f}\n")
        
        f.write("\nMarketing Insights:\n")
        for segment, count in segment_counts.items():
            f.write(f"- {segment} Customers: {count}\n")

def main():
    print("Generating extended analysis...")
    
    # Create all extended visualizations
    create_heatmap_correlations()
    create_product_performance_dashboard()
    create_customer_ltv_analysis()
    create_time_series_forecast()
    create_marketing_segmentation()
    create_extended_summary()
    
    print("\nExtended analysis completed! New visualizations and insights have been saved to:")
    print("results/extended/")
    print("\nNew visualizations include:")
    print("- correlation_heatmap.png: Correlations between key metrics")
    print("- product_performance.html: Interactive product performance dashboard")
    print("- customer_ltv.png: Customer lifetime value analysis")
    print("- sales_forecast.png: Sales time series with rolling average")
    print("- marketing_segments.png: Marketing segmentation distribution")
    print("- extended_analysis_summary.txt: Detailed analysis summary")

if __name__ == "__main__":
    main()
