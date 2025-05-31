# Power BI Dashboard Setup

## Data Model
1. Import the following processed CSV files into Power BI:
   - `../data/processed/processed_sales.csv`
   - `../data/processed/processed_customers.csv`
   - `../data/processed/processed_products.csv`
   - `../data/processed/customer_segments.csv`

2. Create the following relationships:
   - `processed_sales[CustomerID]` -> `processed_customers[CustomerID]`
   - `processed_sales[ProductID]` -> `processed_products[ProductID]`
   - `processed_customers[CustomerID]` -> `customer_segments[CustomerID]`

## Recommended Visuals
1. **Sales Overview**
   - Total Sales (Card)
   - Total Orders (Card)
   - Average Order Value (Card)
   - Sales Trend (Line Chart)
   
2. **Product Performance**
   - Top Selling Products (Bar Chart)
   - Sales by Category (Pie/Donut Chart)
   
3. **Customer Analysis**
   - Customer Segments (Donut Chart)
   - RFM Distribution (Scatter Plot)
   
4. **Regional Performance**
   - Sales by Region (Map)
   - Regional Growth (Line Chart)

## Filters
Add the following filters:
- Date Range
- Region
- Product Category
- Customer Segment

## Measures
Create the following measures in your Power BI model:

```dax
Total Sales = SUM('processed_sales'[TotalPrice])
Total Orders = DISTINCTCOUNT('processed_sales'[OrderID])
Average Order Value = DIVIDE([Total Sales], [Total Orders])
YoY Sales Growth = 
    VAR CurrentYearSales = [Total Sales]
    VAR PreviousYearSales = 
        CALCULATE(
            [Total Sales],
            SAMEPERIODLASTYEAR('processed_sales'[OrderDate])
        )
    RETURN
        IF(
            NOT ISBLANK(PreviousYearSales) && PreviousYearSales <> 0,
            DIVIDE(CurrentYearSales - PreviousYearSales, PreviousYearSales),
            BLANK()
        )
```
