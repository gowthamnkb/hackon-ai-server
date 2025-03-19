from openaiagent.src.agents import Agent, Runner
import openaiagent.src.agents as agents
import asyncio
from instructions.wallet import WALLET_INSTRUCTIONS
from instructions.giftcard import GIFTCARD_INSTRUCTIONS
from tools.db_tools import execute_sql_query
from tools.perform_load import perform_load
from tools.fetch_balance import fetch_balance

History =  {}
class ProcessModel:
    def __init__(self):
        self.runConfig = None
        self.triage_agent = None

    def process(self, request):
        print("History - ", History)
        return self.askAI(request)

    async def mainFn(self, input):
        result = await Runner.run(self.triage_agent, input=input, run_config=self.runConfig)
        return result.final_output

    def askAI(self, request):
        message = request['message']
        token = request.get('token', 'no_token')
        if token not in History:
            History[token] = []
        History[token].append({"role": "user", "content": message})

        wallet_agent = Agent(
            name="Wallet agent",
            instructions= WALLET_INSTRUCTIONS,
            model="gpt-4o",
            tools=[execute_sql_query, perform_load, fetch_balance],
        )

        giftcard_agent = Agent(
            name="Giftcard agent",
           instructions=GIFTCARD_INSTRUCTIONS,
            model="gpt-4o-mini",
            tools=[execute_sql_query],
        )

        self.runConfig = agents.RunConfig(
            model="gpt-4o-mini",
            tracing_disabled=True,
        )

        self.triage_agent = Agent(
            name="Triage agent",
            instructions="""
                Handoff to the appropriate agent based on the keyword wallet/giftcard in query.
                Set merchant_id globally which is rreferenced in all agents
            """,
            model="gpt-4o-mini",
            handoffs=[wallet_agent, giftcard_agent],
        )

        response = asyncio.run(self.mainFn(History[token]))
        History[token].append({"role": "assistant", "content": response})

        return response