from agents import handoff

from openaiagent.src.agents import Agent, Runner
import openaiagent.src.agents as agents
import asyncio

class ProcessModel:
    def __init__(self):
        self.triage_agent = None
        self.run_config = None


    def process(self, request):
        message = request['message']

        wallet_agent = Agent(
            name="Wallet agent",
            instructions="""You're a carpenter, Answer in Hindi""",

            model="gpt-4o-mini",
            # handoffs=[wallet_input_agent, wallet_output_agent]
        )

        gc_agent = Agent(
            name="GC agent",
            instructions="You're a gardener. Answer in Tamil",
            model="gpt-4o-mini"
        )

        self.runConfig = agents.RunConfig(
            model="gpt-4o-mini",
            tracing_disabled=True,
        )

        self.triage_agent = Agent(
            name="Triage agent",
            instructions=message,
            model="gpt-4o-mini",
            handoffs=[wallet_agent, gc_agent],
        )

        return asyncio.run(self.mainFn(message))

    async def mainFn(self, input):
        result = await Runner.run(self.triage_agent, input=input, run_config=self.runConfig)
        return result.final_output





"""
1. Wallet Product
1.1 Input Agent
1.2 Txt Output Agent
1.3. HTML Output Agent

(optional if we have time)
2. GCOMS Product
2.1 Input Agent
2.2 Txt Output Agent
2.3. HTML Output Agent


-------------------------
2 Agents
1. Wallet Agent
2. GC Agent



Instrcution

1. Input format
1.1. point 1

2. Text Output 
"""

    




"""
1. Wallet Product
1.1 Input Agent
1.2 Txt Output Agent
1.3. HTML Output Agent


Input1: what is the balance of wallet for contact xxx?
Output1 : {"select * from balances where contact = xxx"}
wallet : Rs. 1000
Input2 : {"balance":1000}
Output2 : "Wallet balance is Rs. 1000"



I1: I want to do a load 
O1: {"prompt":"Please provide the UserId"}
I2: {"userId":"123"}
O2: {"prompt":"select * from programs where user_id = '123"}
I3: {"programId":"123"}
O3: {"prompt":"After this load, balnce will be xx. Shall I proceed?"}
I4: {"proceed":"yes"}
O4: {"action":"CreateLoad", input}
I5: {"Give out put of load respnose - otput}
O5: {"Load is success. You recharge iD is xx, balance is yy}



"""