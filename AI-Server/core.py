from openaiagent.src.agents import Agent, Runner
import openaiagent.src.agents as agents
import asyncio
from tools.db_tools import execute_sql_query
from tools.schema import DB_SCHEMA
from tools.perform_load import perform_load
from tools.fetch_balance import fetch_balance

History =  []
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
        History.append({"role": "user", "content": message})

        wallet_agent = Agent(
            name="Wallet agent",
            instructions=f"""
                You are a SQL expert. Generate SQL queries based on this database schema:\n{DB_SCHEMA}
                Create queries by referring to the relationships mentioned in schema to create joins or sub queries.
                And call execute_sql_query tool to run query and return response.
                If the query is perform some action, call tool perform_<action> with user_id, program_id, amount as inputs
                If program_id is not in input, run sql query to fetch ids, names from programs table and return them and ask merchant to choose one. 
                If these inputs are not available, ask for them.
                if request is to credit/load wallet than amount and either contact or user_id must be provided.
                if contact provided and generate sql query and run to fetch the userID and use for load
                else if not passed either than prompt error for input.
                Once you have the inputs, run sql query to check current wallet balance of the user and return above inputs and
                would be balance after load operation.""",
            model="gpt-4o-mini",
            tools=[execute_sql_query, perform_load, fetch_balance],
        )

        giftcard_agent = Agent(
            name="Giftcard agent",
            instructions=f"""
                You work with queries on giftcards.
            """,
            model="gpt-4o-mini",
            tools=[execute_sql_query],
        )

        self.runConfig = agents.RunConfig(
            model="gpt-4o-mini",
            tracing_disabled=True,
        )

        self.triage_agent = Agent(
            name="Triage agent",
            instructions="Handoff to the appropriate agent based on the keyword wallet/giftcard in query.",
            model="gpt-4o-mini",
            handoffs=[wallet_agent, giftcard_agent],
        )

        response = asyncio.run(self.mainFn(History))
        History.append({"role": "assistant", "content": response})

        return response