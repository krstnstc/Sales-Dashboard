# Sales and Customer Analysis Dashboard

## Overview
A comprehensive business intelligence solution designed to provide actionable insights for retail operations through advanced analytics and interactive visualizations.

## Key Features
- 📊 Advanced Analytics:
  - RFM analysis for customer segmentation
  - Predictive churn modeling
  - Sales trend forecasting
  - Product performance analysis
  - Customer lifetime value calculation

- 📈 Interactive Visualizations:
  - Modern HTML-based interactive reports
  - Interactive Power BI dashboards
  - Excel pivot tables with what-if analysis
  - Correlation heatmaps
  - Time series analysis

- 🛠️ Data Processing:
  - Automated data cleaning and preprocessing
  - Data validation and quality checks
  - Batch processing capabilities
  - Data transformation pipelines

## Technical Architecture
```
├── data/
│   ├── raw/                # Raw input data files
│   ├── processed/          # Cleaned and processed data
│   └── generated/          # Sample data generation
├── notebooks/              # Data analysis notebooks
├── excel/                  # Excel analysis files
├── powerbi/               # Power BI dashboard files
├── results/               # Analysis results and visualizations
│   ├── html/              # Interactive HTML reports
│   └── extended/          # Extended analysis results
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## Setup and Installation
1. **Prerequisites**:
   - Python 3.8+
   - Required packages (install using pip):
     ```bash
     pip install -r requirements.txt
     ```

2. **Data Preparation**:
   - Place raw data files in `data/raw/`
   - Run data preprocessing:
     ```bash
     python run_preprocessing.py
     ```
   - Run advanced analytics:
     ```bash
     python run_advanced_analytics.py
     ```

3. **Analysis Tools**:
   - Open Excel files in `excel/` for pivot table analysis
   - Open Power BI files in `powerbi/` for interactive dashboards
   - View HTML reports in `results/html/`

## Data Sources
- **Sales Data**:
  - Order details (OrderID, CustomerID, OrderDate)
  - Product information (ProductID, Category, UnitPrice)
  - Transaction metrics (Quantity, TotalPrice)
  - Location data (Region, Location)

- **Customer Data**:
  - Customer demographics
  - Purchase history
  - Engagement metrics
  - Churn indicators

- **Product Data**:
  - Product catalog
  - Pricing information
  - Category hierarchy
  - Cost metrics

## Analysis Capabilities
1. **Customer Segmentation**:
   - RFM-based segmentation
   - Value-based clustering
   - Churn prediction modeling
   - Marketing segment analysis

2. **Sales Performance**:
   - Trend analysis
   - Seasonality detection
   - Regional performance
   - Category analysis

3. **Product Analytics**:
   - Performance metrics
   - Category distribution
   - Price elasticity
   - Cross-selling analysis

## Usage
1. **Data Analysis**:
   ```bash
   # Run preprocessing
   python run_preprocessing.py
   
   # Run advanced analytics
   python run_advanced_analytics.py
   
   # Generate HTML report
   python create_html_report.py
   ```

2. **Interactive Analysis**:
   - Open Power BI dashboard for real-time insights
   - Use Excel files for what-if scenarios
   - Explore HTML report for detailed analysis

## License
This project is proprietary and confidential. All rights reserved.

## Contact
For support or questions, please contact me at my email.
