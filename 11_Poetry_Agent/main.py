import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import enable_verbose_stdout_logging
from agents.run import RunConfig

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found, please check your .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

lyric_poetry_analyst = Agent(
    name="Lyric Poetry Analyst",
    instructions="You are Lyric Poetry Analyst you analyse and give a brief description (tashree) of the poetry or stanzas.",
    handoff_description="""
    Gives description for Lyric poetry which is when poets write about their 
    own feelings and thoughts, like songs or poems about being sad or happy.
    """
)

narrative_poetry_analyst = Agent(
    name="Narrative Poetry Analyst",
    instructions="You are Narrative Poetry Analyst you analyse and give a brief description (tashree) of the poetry or stanzas.",
    handoff_description="""
    Gives description for Narrative poetry that tells a story with characters 
    and events, just like a regular story but written in poem form with rhymes 
    or special rhythm.
    """
)

dramatic_poetry_analyst = Agent(
    name="Dramatic Poetry Analyst",
    instructions="You are Dramatic Poetry Analyst you analyse and give a brief description (tashree) of the poetry or stanzas.",
    handoff_description="""
    Gives description for Dramatic poetry which is meant to be performed out 
    loud, where someone acts like a character and speaks their thoughts and 
    feelings to an audience (acting in a theatre).
    """
)

poetry_agent = Agent(
    name="Poetry Analyst",
    instructions="You analyse the poetry type (Lyric/Narrative, Dramatic) and handsoff to the appropriate agent.",
    handoffs=[lyric_poetry_analyst, narrative_poetry_analyst, dramatic_poetry_analyst]
)

enable_verbose_stdout_logging()

result = Runner.run_sync(
    poetry_agent, 
    "The moon's soft glow weaves dreams in quiet air.",
    run_config=config
)

print("\nAgent's Response:\n")
print(f"{result.final_output}\n")
print(f"Responded by:{result.last_agent.name}\n\n")
