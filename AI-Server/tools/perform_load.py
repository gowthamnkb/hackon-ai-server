from openaiagent.src.agents import function_tool

# Define the tool function
@function_tool
def perform_load(userId: str, progId: str, amount: int) -> dict:
    try:
        # Perform load
        results = {"id": "iload_sampleId000001", "program_id": progId, "amount": 10000}
        return {"status": "success", "data": results}

    except Exception as e:
        return {"status": "error", "message": str(e)}
