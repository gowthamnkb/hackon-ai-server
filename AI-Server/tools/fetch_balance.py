from openaiagent.src.agents import function_tool
from tools.db_tools import execute_query

# Define the tool function
@function_tool
def fetch_balance(contact: str) -> dict:
    try:
        results = execute_query(f"""select b.balance from users u
            join wallets w on w.user_id = u.id
            join accounts a on a.id = w.account_id
            join balances b on b.id = a.balance_id
            where contact={contact} and partner_customer_id <> ''
        """)

        return results


    except Exception as e:
        return {"status": "error", "message": str(e)}
