from tools.schema import DB_SCHEMA


GIFTCARD_INSTRUCTIONS = f"""
    Generate SQL queries based on the provided database schema: {DB_SCHEMA}.
    Use relationships in the schema to construct joins or subqueries where applicable.
    Execute read queries using the execute_sql_query tool.
    Use merchant_id where condition whereever applicable.
    Handling missing inputs:
"""