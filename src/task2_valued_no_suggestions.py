# task2_valued_no_suggestions.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, lit

def initialize_spark(app_name="Task2_Valued_No_Suggestions"):
    """
    Initialize and return a SparkSession.
    """
    spark = SparkSession.builder \
        .appName(app_name) \
        .getOrCreate()
    return spark

def load_data(spark, file_path):
    """
    Load the employee data from a CSV file into a Spark DataFrame.

    Parameters:
        spark (SparkSession): The SparkSession object.
        file_path (str): Path to the employee_data.csv file.

    Returns:
        DataFrame: Spark DataFrame containing employee data.
    """
    schema = "EmployeeID INT, Department STRING, JobTitle STRING, SatisfactionRating INT, EngagementLevel STRING, ReportsConcerns BOOLEAN, ProvidedSuggestions BOOLEAN"
    
    df = spark.read.csv(file_path, header=True, schema=schema)
    return df


def identify_valued_no_suggestions(df):
    """
    Find employees who feel valued but have not provided suggestions and calculate their proportion.

    Parameters:
        df (DataFrame): Spark DataFrame containing employee data.

    Returns:
        tuple: Number of such employees and their proportion.
    """
    # TODO: Implement Task 2
    # Steps:
    # 1. Identify employees with SatisfactionRating >= 4.
    # 2. Among these, filter those with ProvidedSuggestions == False.
    # 3. Calculate the number and proportion of these employees.
    # 4. Return the results.

    filtered_count = df.filter((df.SatisfactionRating >= 4) &
                         (df.ProvidedSuggestions == lit(False))).count()

    total_count = df.count()
    proportion = (filtered_count / df.count()) * 100 if total_count > 0 else 0

    return filtered_count, proportion


def write_output(number, proportion, output_path):
    """
    Write the results to a text file.

    Parameters:
        number (int): Number of employees feeling valued without suggestions.
        proportion (float): Proportion of such employees.
        output_path (str): Path to save the output text file.

    Returns:
        None
    """
    with open(output_path, 'w') as f:
        f.write(f"Number of Employees Feeling Valued without Suggestions: {number}\n")
        f.write(f"Proportion: {proportion}%\n")

def main():
    """
    Main function to execute Task 2.
    """
    # Initialize Spark
    spark = initialize_spark()
    
    # Define file paths
    input_file = "/opt/bitnami/spark/Employee/input/employee_data.csv"
    output_file = "/opt/bitnami/spark/Employee/outputs/task2/valued_no_suggestions.txt"
    
    # Load data
    df = load_data(spark, input_file)
    
    # Perform Task 2
    number, proportion = identify_valued_no_suggestions(df)
    
    # Write the result to a text file
    write_output(number, proportion, output_file)
    
    # Stop Spark Session
    spark.stop()

if __name__ == "__main__":
    main()
