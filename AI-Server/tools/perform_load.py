from openaiagent.src.agents import function_tool
import uuid
import requests
# Define the tool function
@function_tool
def perform_load(userId: str, progId: str, amount: int) -> any:

    try:
        print("param", userId, progId, amount)
        res = creditWallet(userId, progId, amount)
        return res
    except Exception as e:
        print("error came :", e)
        return {"status": "error", "message": str(e)}

def creditWallet(userId: str, progId: str, amount: int) -> any:
    headers = {
        "Content-Type": "application/json",
        "Grpc-Metadata-X-Passport-JWT-V1": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVkZ2V2MSJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJhdXRoZW50aWNhdGVkIjp0cnVlLCJtb2RlIjoidGVzdCIsImNvbnN1bWVyIjp7ImlkIjoiMTAwMDAwMDAwMDAwMDAiLCJ0eXBlIjoibWVyY2hhbnQifX0.DfU0igDh8S15oV1Oi6bYEVIeQvE29AY_-RkLnoiCbr7pWasOAWW67nS2Wx4dae8xL2yBHbU1RylGxZ6ok8Rr6Rz6WYA3smD5XTRKEs9ztGXQ7w9Z2T1FzA6FWzY8ibWhtM_LzMwfBDxqhTBHF1lNhmT-Vuz3kyIaWWJzqK0vBCHmY1uWcJ151BnmpP0R_yJ1i3PE3j41U_r_Sq1dSFjYgZ02f84B52DDStp5XCDucrGU1TDtu_aqvQ_PAbavmtOu72O6TohxB2dl3G67lB0Dy1UT77KqICF7f57q6g73KiPTF-rTMAmB2n8nY5Fb1r4KgvrM95LauRFmX1PQYYCMxA"
    }
    loadUrl = "http://0.0.0.0:8081/v1/issuing/loads"

    payload = {"program_id": "iprog_" + progId, "description": "load from chat-bot",
               'reference_id': str(uuid.uuid4()), 'user_id': "iuser_" + userId, "amount": str(amount)}
    response = requests.post(loadUrl, headers=headers, json=payload)
    print(response.json())

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"