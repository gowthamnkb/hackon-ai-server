from openaiagent.src.agents import function_tool
import uuid
import requests
# Define the tool function
@function_tool
def perform_load(userId: str, progId: str, amount: int) -> any:

    try:
        res = creditWallet(userId, amount)
        return res
    except Exception as e:
        print("error came :", e)
        return {"status": "error", "message": str(e)}

def creditWallet(userId: str, amount: int) -> any:
    headers = {
        "Content-Type": "application/json",
        "Grpc-Metadata-X-Passport-JWT-V1": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVkZ2V2MSJ9.eyJpc3MiOiJodHRwczovL2VkZ2UucmF6b3JwYXkuY29tIiwic3ViIjoiaHR0cHM6Ly9zdWJzY3JpcHRpb25zLnJhem9ycGF5LmNvbSIsImp0aSI6IjEyMzQ1Njc4OTAiLCJpYXQiOjE1ODE0MzI1MTQsIm5iZiI6MTU4MTQzMjUxNCwiZXhwIjoxODk4MTkyNzQ5LCJpZGVudGlmaWVkIjp0cnVlLCJhdXRoZW50aWNhdGVkIjp0cnVlLCJtb2RlIjoibGl2ZSIsImNvbnN1bWVyIjp7ImlkIjoiMTAwMDAwMDAwMDAwMDAiLCJ0eXBlIjoibWVyY2hhbnQifSwibWVyY2hhbnQiOnsiaWQiOiIxMDAwMDAwMDAwMDAwMCJ9fQ.vFSQJ4BdHbOc2VOyzB_WMOxMM5LH3s22_WuIcsxmeQwAAdQVARs6OGIJHqglJQTBacUh1fr3cWGDDhCmLhbjcLXVcdHT6V1p7aTQzV9g2-O7Rj-TS6AhNQz0n1_8fsL9EljgHAPrpODhk-O8rwWO3pORGIaH6J8VFwSzAxmJXE1TyRMQ6lPRlIPN6_anqoS9t69kqXhK7w6F1ZE8WEswRq7oumCkhCUo72nrqRtb3Q6RQrk97vOt2YSk2HrZXg1Wj0EUdn4ogIDygEH25fDN97triHA7B2XZIhfK5w_etRQ9ojox2c2zu2V_STnqI6gewpeY_9AqhUHJed7NQ35q4Q"
    }
    loadUrl = "http://0.0.0.0:8081/v1/issuing/loads"

    payload = {"program_id": "iprog_L3HJb2aS36SQeH", "description": "load from chat-bot",
               'reference_id': str(uuid.uuid4()), 'user_id': "iuser_" + userId, "amount": str(amount)}
    response = requests.post(loadUrl, headers=headers, json=payload)
    print(response.json())

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"