# HRInsight

HRInsight is employee data analysis project, for a small scale organisation, built with Python and MySQL. 
It explores salary patterns, department-level performance, and the relationship between salary and performance, then saves the charts.

## What it does

- Connects to MySQL using DB credentials stored in a local `.env` file.
- Loads the `employee`, `emp_performance`, and `emp_bonus` tables.
- Runs exploratory data analysis (EDA): 
  - Table shape, Sample rows
  - duplicate rows and missing values
- Summarises salary and performance by department.
- Creates three Matplotlib charts:
  - Average salary by department
  - Average performance score by department
  - Salary vs performance, with a linear trend line and correlation
- Checks employee IDs before merging to avoid silently multiplying rows.

## Tools

- Python (Pandas, Matplotlib)
- MySQL

## Charts

Charts are generated from local execution.

- Bar chart: Average salary for each department -`average_salary_by_department.png` 
- Bar chart: Average department performance -`average_performance_by_department.png`
    - green for scores >= 85
    - gold for scoores >=80 and <85
    - blue for <80
- Scatter chart: Salary and performance score for each employee -`salary_vs_performance.png`

## EDA checklist

The script checks:

- Number of rows and columns in each table
- Sample rows and column data types
- Duplicate and missing value check
- Salary summary statistics and salary by department
- Performance summary by department
- Salary/performance correlation

## Important notes

- Used synthetic data for this project.
- Ensure the database and expected tables exist. 
- Keep `.env` private, it is excluded by `.gitignore`.
