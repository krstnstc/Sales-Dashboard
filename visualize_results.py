import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Create results directory
os.makedirs('results', exist_ok=True)

def create_sales_trend_plot():
    """Create sales trend plot over time"""
    # Load sales data
    sales_df = pd.read_csv('data/processed/processed_sales.csv')
    
    # Convert OrderDate to datetime
    sales_df['OrderDate'] = pd.to_datetime(sales_df['OrderDate'])
    
    # Group by month and calculate total sales
    monthly_sales = sales_df.groupby(sales_df['OrderDate'].dt.to_period('M'))['TotalPrice'].sum()
    
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_sales.index.to_timestamp(), monthly_sales.values)
    plt.title('Monthly Sales Trend')
    plt.xlabel('Date')
    plt.ylabel('Total Sales')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('results/sales_trend.png')
    plt.close()

def create_category_sales_plot():
    """Create bar chart of sales by category"""
    # Load sales and products data
    sales_df = pd.read_csv('data/processed/processed_sales.csv')
    products_df = pd.read_csv('data/processed/processed_products.csv')
    
    # Merge and calculate sales by category
    category_sales = pd.merge(sales_df, products_df, on='ProductID')
    category_sales = category_sales.groupby('Category')['TotalPrice'].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=category_sales.values, y=category_sales.index)
    plt.title('Sales by Product Category')
    plt.xlabel('Total Sales')
    plt.ylabel('Category')
    plt.tight_layout()
    plt.savefig('results/category_sales.png')
    plt.close()

def create_customer_segmentation_plot():
    """Create customer segmentation visualization"""
    # Load customer segments
    segments_df = pd.read_csv('data/processed/customer_segments.csv')
    
    # Calculate segment distribution
    segment_dist = segments_df['Segment'].value_counts()
    
    plt.figure(figsize=(8, 8))
    plt.pie(segment_dist.values, labels=segment_dist.index, autopct='%1.1f%%', startangle=140)
    plt.title('Customer Segmentation Distribution')
    plt.tight_layout()
    plt.savefig('results/customer_segments.png')
    plt.close()

def create_rfm_analysis():
    """Create RFM analysis scatter plot"""
    # Load customer segments
    segments_df = pd.read_csv('data/processed/customer_segments.csv')
    
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=segments_df, x='Recency', y='Monetary', hue='Segment', size='Frequency', 
                   palette='viridis', sizes=(20, 200))
    plt.title('RFM Analysis')
    plt.xlabel('Recency (days)')
    plt.ylabel('Monetary Value')
    plt.tight_layout()
    plt.savefig('results/rfm_analysis.png')
    plt.close()

def create_region_analysis():
    """Create sales by region analysis"""
    # Load sales data
    sales_df = pd.read_csv('data/processed/processed_sales.csv')
    
    # Calculate sales by region
    region_sales = sales_df.groupby('Region')['TotalPrice'].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=region_sales.index, y=region_sales.values)
    plt.title('Sales by Region')
    plt.xlabel('Region')
    plt.ylabel('Total Sales')
    plt.tight_layout()
    plt.savefig('results/region_sales.png')
    plt.close()

def create_churn_analysis():
    """Create churn analysis visualization"""
    # Load customer segments
    segments_df = pd.read_csv('data/processed/customer_segments.csv')
    
    # Calculate churn rates by segment
    churn_rates = segments_df.groupby('Segment')['Churn'].mean() * 100
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=churn_rates.index, y=churn_rates.values)
    plt.title('Churn Rate by Customer Segment')
    plt.xlabel('Segment')
    plt.ylabel('Churn Rate (%)')
    plt.tight_layout()
    plt.savefig('results/churn_analysis.png')
    plt.close()

def create_results_summary():
    """Create a summary text file with key findings"""
    # Load data
    sales_df = pd.read_csv('data/processed/processed_sales.csv')
    segments_df = pd.read_csv('data/processed/customer_segments.csv')
    
    # Calculate key metrics
    total_sales = sales_df['TotalPrice'].sum()
    total_orders = sales_df['OrderID'].nunique()
    avg_order_value = sales_df['TotalPrice'].mean()
    total_customers = segments_df['CustomerID'].nunique()
    churn_rate = segments_df['Churn'].mean()
    
    # Write summary
    with open('results/analysis_summary.txt', 'w') as f:
        f.write("Sales and Customer Analysis Summary\n")
        f.write("-" * 50 + "\n\n")
        
        f.write(f"Key Metrics:\n")
        f.write(f"- Total Sales: ${total_sales:,.2f}\n")
        f.write(f"- Total Orders: {total_orders}\n")
        f.write(f"- Average Order Value: ${avg_order_value:,.2f}\n")
        f.write(f"- Total Customers: {total_customers}\n")
        f.write(f"- Overall Churn Rate: {churn_rate:.1%}\n\n")
        
        f.write("Customer Segmentation:\n")
        segment_dist = segments_df['Segment'].value_counts()
        for segment, count in segment_dist.items():
            f.write(f"- Segment {segment}: {count} customers\n")
        
        f.write("\nTop Performing Categories:\n")
        category_sales = pd.merge(sales_df, pd.read_csv('data/processed/processed_products.csv'), on='ProductID')
        top_categories = category_sales.groupby('Category')['TotalPrice'].sum().nlargest(5)
        for category, sales in top_categories.items():
            f.write(f"- {category}: ${sales:,.2f}\n")

def main():
    print("Generating visualizations...")
    
    # Create all visualizations
    create_sales_trend_plot()
    create_category_sales_plot()
    create_customer_segmentation_plot()
    create_rfm_analysis()
    create_region_analysis()
    create_churn_analysis()
    create_results_summary()
    
    print("\nVisualizations and results have been saved to the 'results' folder:")
    print("- sales_trend.png: Monthly sales trend")
    print("- category_sales.png: Sales by product category")
    print("- customer_segments.png: Customer segmentation distribution")
    print("- rfm_analysis.png: RFM analysis scatter plot")
    print("- region_sales.png: Sales by region")
    print("- churn_analysis.png: Churn rate by segment")
    print("- analysis_summary.txt: Text summary of key findings")

if __name__ == "__main__":
    main()
