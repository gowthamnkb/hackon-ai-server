import mysql.connector
from openaiagent.src.agents import function_tool

# MySQL Connection Config
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "password",
    "database": "wallet"
}

# Define the tool function
@function_tool
def execute_sql_query(query: str) -> dict:
    """
    Executes the given SQL query on MySQL and returns the results as a JSON dictionary.

    Args:
        query (str): The SQL query to execute.

    Returns:
        dict: The query result.
    """
    return execute_query(query)


def execute_query(query: str) -> dict:
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        return {"status": "success", "data": results}

    except Exception as e:
        return {"status": "error", "message": str(e)}