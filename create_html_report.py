import os
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import webbrowser
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import json
import numpy as np

# Add Plotly for interactive charts
def create_interactive_charts():
    """Create interactive charts using Plotly"""
    # Load data
    sales_df = pd.read_csv('data/processed/processed_sales.csv')
    products_df = pd.read_csv('data/processed/processed_products.csv')
    segments_df = pd.read_csv('data/processed/customer_segments.csv')
    marketing_segments = pd.read_csv('results/extended/customer_segments_marketing.csv')
    
    # Create sales trend chart
    sales_trend = px.line(
        sales_df.groupby('OrderDate')['TotalPrice'].sum().reset_index(),
        x='OrderDate',
        y='TotalPrice',
        title='Sales Trend Over Time',
        labels={'OrderDate': 'Date', 'TotalPrice': 'Sales Amount'},
        template='plotly_dark'
    )
    sales_trend.update_traces(line=dict(width=2))
    
    # Create product category distribution
    product_dist = px.pie(
        pd.merge(sales_df, products_df, on='ProductID')
        .groupby('Category')['TotalPrice'].sum()
        .reset_index(),
        values='TotalPrice',
        names='Category',
        title='Product Category Distribution',
        template='plotly_dark'
    )
    
    # Create customer segment distribution
    segment_dist = px.bar(
        marketing_segments.groupby('MarketingSegment').size().reset_index(name='count'),
        x='MarketingSegment',
        y='count',
        title='Customer Segment Distribution',
        template='plotly_dark'
    )
    
    # Save charts as JSON
    charts = {
        'sales_trend': sales_trend.to_json(),
        'product_dist': product_dist.to_json(),
        'segment_dist': segment_dist.to_json()
    }
    
    return charts

def generate_html_report():
    """Generate an HTML report combining all analysis results"""
    # Create HTML directory
    os.makedirs('results/html', exist_ok=True)
    
    # Load template environment
    env = Environment(loader=FileSystemLoader('.'))
    
    # Load all data
    sales_df = pd.read_csv('data/processed/processed_sales.csv')
    products_df = pd.read_csv('data/processed/processed_products.csv')
    segments_df = pd.read_csv('data/processed/customer_segments.csv')
    marketing_segments = pd.read_csv('results/extended/customer_segments_marketing.csv')
    
    # Create interactive charts
    charts = create_interactive_charts()
    
    # Calculate key metrics
    total_sales = sales_df['TotalPrice'].sum()
    total_orders = sales_df['OrderID'].nunique()
    avg_order_value = sales_df['TotalPrice'].mean()
    total_customers = segments_df['CustomerID'].nunique()
    churn_rate = segments_df['Churn'].mean()
    
    # Calculate product metrics
    product_metrics = pd.merge(sales_df, products_df, on='ProductID')
    top_products = product_metrics.groupby('ProductName').agg({
        'TotalPrice': 'sum',
        'Quantity': 'sum'
    }).sort_values('TotalPrice', ascending=False).head(5)
    
    # Calculate marketing segment distribution
    segment_dist = marketing_segments['MarketingSegment'].value_counts().to_dict()
    
    # Create template data
    template_data = {
        'title': 'Sales and Customer Analysis Report',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'charts': charts,
        'key_metrics': {
            'Total Sales': f'${total_sales:,.2f}',
            'Total Orders': f'{total_orders:,}',
            'Average Order Value': f'${avg_order_value:,.2f}',
            'Total Customers': f'{total_customers:,}',
            'Churn Rate': f'{churn_rate:.1%}'
        },
        'top_products': top_products.to_dict('records'),
        'segment_distribution': segment_dist,
        'visualizations': {
            'correlation_heatmap': '../extended/correlation_heatmap.png',
            'customer_ltv': '../extended/customer_ltv.png'
        }
    }
    
    # Create template
    template = env.from_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ title }}</title>
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <!-- Font Awesome -->
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <!-- Custom Styles -->
        <style>
            :root {
                --primary-color: #2c3e50;
                --secondary-color: #3498db;
                --background-color: #f8f9fa;
                --card-background: #ffffff;
                --text-color: #2c3e50;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: var(--background-color);
                color: var(--text-color);
                line-height: 1.6;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 2rem;
            }
            
            .header {
                text-align: center;
                padding: 4rem 0;
                background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
                color: white;
                border-radius: 10px;
                margin-bottom: 3rem;
            }
            
            .header h1 {
                font-size: 2.5rem;
                margin-bottom: 1rem;
            }
            
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
                margin-bottom: 3rem;
            }
            
            .metric-card {
                background: var(--card-background);
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;
            }
            
            .metric-card:hover {
                transform: translateY(-5px);
            }
            
            .metric-value {
                font-size: 2rem;
                font-weight: 700;
                color: var(--secondary-color);
                margin-bottom: 0.5rem;
            }
            
            .section {
                background: var(--card-background);
                padding: 2rem;
                border-radius: 15px;
                margin-bottom: 3rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .section-header {
                color: var(--primary-color);
                margin-bottom: 2rem;
                border-bottom: 2px solid var(--secondary-color);
                padding-bottom: 1rem;
            }
            
            .table {
                width: 100%;
                margin-bottom: 2rem;
            }
            
            .table th {
                background-color: var(--secondary-color);
                color: white;
                font-weight: 600;
            }
            
            .table td {
                vertical-align: middle;
                padding: 1rem;
            }
            
            .visualization {
                margin-bottom: 2rem;
            }
            
            .interactive-visualization {
                width: 100%;
                height: 500px;
                border-radius: 10px;
                overflow: hidden;
            }
            
            .segment-distribution {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
                margin-bottom: 3rem;
            }
            
            .segment-card {
                background: var(--card-background);
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            
            .segment-value {
                font-size: 2rem;
                font-weight: 700;
                color: var(--primary-color);
                margin-bottom: 0.5rem;
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .metrics-grid {
                    grid-template-columns: 1fr;
                }
                
                .segment-distribution {
                    grid-template-columns: 1fr;
                }
                
                .header h1 {
                    font-size: 2rem;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{{ title }}</h1>
                <p class="text-white">Generated on: {{ date }}</p>
            </div>

            <div class="section">
                <h2 class="section-header">Key Business Metrics</h2>
                <div class="metrics-grid">
                    {% for metric, value in key_metrics.items() %}
                    <div class="metric-card">
                        <div class="metric-value">{{ value }}</div>
                        <p class="text-muted">{{ metric }}</p>
                        <i class="fas fa-arrow-up text-success"></i>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div class="section">
                <h2 class="section-header">Product Performance Analysis</h2>
                <div class="row">
                    <div class="col-md-6">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Product Name</th>
                                    <th>Total Revenue</th>
                                    <th>Total Quantity</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for product in top_products %}
                                <tr>
                                    <td>{{ product.ProductName }}</td>
                                    <td>${{ product.TotalPrice|round(2) }}</td>
                                    <td>{{ product.Quantity }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    <div class="col-md-6">
                        <div class="visualization">
                            <h3>Product Category Distribution</h3>
                            <div id="productDist"></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2 class="section-header">Customer Segmentation</h2>
                <div class="row">
                    <div class="col-md-6">
                        <div class="segment-distribution">
                            {% for segment, count in segment_distribution.items() %}
                            <div class="segment-card">
                                <div class="segment-value">{{ count }}</div>
                                <p>{{ segment }} Customers</p>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="visualization">
                            <h3>Segment Distribution</h3>
                            <div id="segmentDist"></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2 class="section-header">Sales Performance</h2>
                <div class="visualization">
                    <h3>Sales Trend Analysis</h3>
                    <div id="salesTrend"></div>
                </div>
            </div>

            <div class="section">
                <h2 class="section-header">Additional Visual Analysis</h2>
                <div class="row">
                    <div class="col-md-6">
                        <div class="visualization">
                            <h3>Correlation Analysis</h3>
                            <img src="{{ visualizations.correlation_heatmap }}" 
                                 class="img-fluid" 
                                 alt="Correlation Heatmap">
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="visualization">
                            <h3>Customer Lifetime Value</h3>
                            <img src="{{ visualizations.customer_ltv }}" 
                                 class="img-fluid" 
                                 alt="Customer Lifetime Value">
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Plotly.js -->
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <script>
            // Load interactive charts
            const charts = {{ charts|tojson }};
            
            // Sales Trend
            Plotly.newPlot('salesTrend', JSON.parse(charts.sales_trend));
            
            // Product Distribution
            Plotly.newPlot('productDist', JSON.parse(charts.product_dist));
            
            // Segment Distribution
            Plotly.newPlot('segmentDist', JSON.parse(charts.segment_dist));
        </script>
    </body>
    </html>
    """)
    
    # Render template
    html = template.render(**template_data)
    
    # Save HTML file
    with open('results/html/report.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("HTML report generated successfully!")
    print("Opening report in browser...")
    
    # Open in browser
    webbrowser.open('results/html/report.html')

if __name__ == "__main__":
    generate_html_report()
