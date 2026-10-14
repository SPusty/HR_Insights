import os
from dotenv import load_dotenv
import logging
import mysql.connector as mysql
import matplotlib.pyplot as mplt
import pandas as pd
from pathlib import Path

 #logger
logging.basicConfig(level=logging.INFO,format="%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)
# Establish a connection to the MySQL database
def connectDB():
    try:
        DB_USERNAME = os.getenv("DB_USERNAME")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_NAME = os.getenv("DB_NAME")

        conn= mysql.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        logger.info("Connected to DB: %s",conn.database)
        return conn
    except mysql.Error as err:
        logger.error("error during DB connection: %s",err)
        return None

#fetch data from database and merge
def loadnmergeTables(dbConn):
    print("Preparing to fetch data from the database:\n")
    emp_query = "Select * FROM employee"
    df_emp =pd.read_sql(emp_query, dbConn)
    perf_query = "Select * FROM emp_performance"
    df_perf = pd.read_sql(perf_query, dbConn)

    print("Data fetched successfully. Here are the first few rows of the dataframe:\n")
    print(df_emp.head(2))
    print(df_perf.head(2))
    
    if df_emp.duplicated().sum() > 0:
        print(f"Duplicate record count:\n {df_emp.duplicated().sum()}")
        df_emp.drop_duplicates(inplace=True)
    else:
        print("No duplicate records found.")
    
    #merge with performance dataset
    print(f"\nMerging with emp_performance table:\n")
    try:
        df_merged = pd.merge(df_emp,df_perf, on='employee_id',how='left',validate='one_to_one')
        if df_merged['performance_score'].isna().sum()>0:
            logger.info("Employees without performance scores: %s", df_merged['performance_score'].isna().sum())
        print(f"Data merged successfully. Here is the merged dataframe:\n {df_merged.head()}")
        return df_merged
    except Exception as error:
        print(f"Error occured during merge: {error}")
        return None

#analysis of employee table data-- average, min,max,count of employee
def tableInspection(df_merged):
    print(f"Employee data shape: {df_merged.shape}")
    #salary statistics of all employees
    print(f"Salary statistics for all employees:\n{df_merged['salary'].agg(['sum','mean','max','min']).round(2)}")
    # average performance score for each department
    print(f"Performance scores by department:\n {round(df_merged.groupby('department').agg(highest_score=('performance_score', 'max'), lowest_score=('performance_score', 'min'), average_score=('performance_score', 'mean')),2)}")

    #department level summary
    print(f"Department summary:\n {round(df_merged.groupby('department').agg(employee= ('employee_id','count'),avg_salary= ('salary','mean'),highest_score=('performance_score', 'max'), lowest_score=('performance_score', 'min')),2)}")

    dept_avg_sal = round(df_merged.groupby('department')['salary'].mean().sort_values(ascending=False),2)
    print(f"Avg. salary per department: {dept_avg_sal}")

    dept_perf = round(df_merged.groupby('department')['performance_score'].mean().sort_values(ascending=False),2)
    print(f"Avg. Performance by department: {dept_perf}")

    #correlation between salary and performance score
    print(f"Salary and Performance score correlation: {df_merged['salary'].corr(df_merged['performance_score'])}")

    return dept_avg_sal,dept_perf,df_merged
 

#chart
def visualChart(dept_avg_sal,dept_perf,df_merged):
    # chart1: salary distribution across departments
    mplt.bar(dept_avg_sal.index,dept_avg_sal.values)
    mplt.title('Average salary per department')
    mplt.xlabel('Department')
    mplt.ylabel('Avg Salary')
    mplt.tight_layout()
    mplt.savefig('avgSalByDept.png')
    #mplt.show()
    mplt.close('all')

    #Chart2: performance by department
    barColor = ['green' if score >= 85 
                else 'gold'  if score >= 80  
                else 'skyblue'
                for score in dept_perf.values]
    print(barColor)
    mplt.bar(dept_perf.index,dept_perf.values,color=barColor)
    mplt.tight_layout()
    mplt.title('Performance by department')
    mplt.xlabel('Department')
    mplt.ylabel('Avg Performance')
    mplt.savefig('avgPerfByDept.png')
    #mplt.show()
    mplt.close()

    #Chart3: salary vs performance
    x=df_merged['salary']
    y=df_merged['performance_score']
    mplt.scatter(x,y)
    mplt.title('Salary vs Performance')
    mplt.xlabel('Salary')
    mplt.ylabel('Performance Score')
    mplt.tight_layout()
    mplt.savefig('salaryVsPerformance.png')
    #mplt.show()
    mplt.close()

    
def main():
    #env
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path)

    #connect DB
    dbConn = connectDB()
    #load from DB and merge employee, performance tables
    if dbConn is None:
        logger.error("DB connection failed.")
        return
    else:
        df_merged = loadnmergeTables(dbConn)
        dbConn.close()
        
    #inspect and EDA
    if df_merged is None:
        logger.error("No data available.")
        return
    else:
        dept_avg_sal,dept_perf,df_merged = tableInspection(df_merged)
        #chart
        visualChart(dept_avg_sal,dept_perf,df_merged)

#call main
if __name__== "__main__":
    main()

