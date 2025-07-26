import os
from typing import TypedDict
from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, enable_verbose_stdout_logging, function_tool

from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")

# Set up the provider for Gemini API

provider = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/",
)

# Define the model for Gemini
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",  
    openai_client=provider,
)

# Run configuration
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)

# enable_verbose_stdout_logging()

class Location(TypedDict):
    city:str
    country:str

@function_tool
def get_current_location()->str:
    """
    get the current location of the user
    """
    return Location(city='karachi', country='pakistan')

class News(TypedDict):
    title:str
    description:str

@function_tool
def get_current_news()->str:
    """
    get the current news of the user
    """
    return News(title='no news', description='no news')

plant_agent = Agent(
    name='plant_agent',
    instructions='you should give all the information about the plant',
)

@function_tool
def get_current_photosynthesis()->str:
    return 'photosynthesis is the process of converting light energy into chemical energy'


agent = Agent(
    name='assistant',
    instructions=
    ''' you should solved the all question that user will asked with you .
    used tool to solved the user query and also you should handoff the plant_agent to get the information about the plant
        you should solved all query of the users
    ''',
    tools=[get_current_location, get_current_news],
    handoffs=[plant_agent],
    model= model
)



result = Runner.run_sync(
    agent,
    """ 
    what is meant by angiography
    what is the current news
        what is my current location
    """,
    run_config=run_config
)
print('='*50)
print("Result: ",result.last_agent.name)
print(result.new_items)
print("Result: ",result.final_output)