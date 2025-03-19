from agents import Agent, Runner
import asyncio
# import ssl

# ssl._create_default_https_context = ssl._create_unverified_context

wallet_agent = Agent(
    name="Wallet agent",
    instructions="You only speak Spanish.",
)

gc_agent = Agent(
    name="GC agent",
    instructions="You only speak English",
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[wallet_agent, gc_agent],
)


async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())