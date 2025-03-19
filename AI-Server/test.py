from openaiagent.src.agents import Agent, Runner
import openaiagent.src.agents as agents
import asyncio


wallet_agent = Agent(
    name="Wallet agent",
    instructions="""You're a carpenter, Answer in Hindi""",

model="gpt-4o-mini"
)

gc_agent = Agent(
    name="GC agent",
    instructions="You're a gardener. Answer in Tamil",
model="gpt-4o-mini"
)

runConfig = agents.RunConfig(
    model="gpt-4o-mini",
    tracing_disabled=True,
)
triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the request. If gardener send to GC agent, If Carpenter, send to Wallet agent",
model="gpt-4o-mini",
    handoffs=[wallet_agent, gc_agent],
)



async def main():
    result = await Runner.run(triage_agent, input="Which tool should I use to cut woods?" ,run_config=runConfig)
    print(result.final_output)
    result = await Runner.run(triage_agent, input="Which indoor plant is good to plant?" ,run_config=runConfig)
    print(result.final_output)



if __name__ == "__main__":
    asyncio.run(main())