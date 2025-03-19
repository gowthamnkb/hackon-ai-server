from openaiagent.src.agents import Agent, Runner
import openaiagent.src.agents as agents
import asyncio

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
            instructions="""You're a AI Bot""",
            model="gpt-4o-mini",
        )

        gc_agent = Agent(
            name="GC agent",
            instructions="You're a AI Bot",
            model="gpt-4o-mini"
        )

        self.runConfig = agents.RunConfig(
            model="gpt-4o-mini",
            tracing_disabled=True,
        )

        self.triage_agent = Agent(
            name="Triage agent",
            instructions="Route to random agents. ",
            model="gpt-4o-mini",
            handoffs=[wallet_agent, gc_agent],
        )

        response = asyncio.run(self.mainFn(History))
        History.append({"role": "assistant", "content": response})

        return response