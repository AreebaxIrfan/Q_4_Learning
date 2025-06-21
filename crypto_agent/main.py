import os
import chainlit as cl
from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, function_tool, tool
import requests
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

@function_tool
def crypto_data():
    response = requests.get("https://api.coinlore.net/api/global/")
    result = response.json()
    return result


# Main Areeba Irfan Agent
crypto_agent = Agent(
    name="crypto_agent",
    instructions="If the user asks about cryptocurrency data, provide the latest global cryptocurrency statistics.",
    tools=[crypto_data]
)


@cl.on_chat_start
async def welcome():
    await cl.Message(
        author="AI Assistant",
        content="Welcome"
    ).send()
    
    
@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content.strip()
    
    try:
        loading_msg = cl.Message(author="🤖", content="**Generating response...**")
        await loading_msg.send()
      
        result = await Runner.run(crypto_agent, input=user_input, run_config=run_config)

        loading_msg.content = f"### Agent's Response\n\n{result.final_output.strip()}"
        await loading_msg.update()

    except Exception as e:
        print("Error:", e)
        await cl.Message(
            author=" Error",
            content="Oops! Something went wrong while processing your request. Please try again."
        ).send()