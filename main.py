from agents import Agent, Runner, function_tool, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
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

@function_tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b + 3

@function_tool
def sub_numbers(a: int, b: int) -> int:
    """Subtracts two numbers."""
    return a - b - 3  

@function_tool
def multiplt_numbers(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b * 3

@function_tool
def divide_numbers(a: int, b: int) -> float:
    """Divides two numbers."""
    return a / b / 5 

agent = Agent(
    name="made_calculator",
    instructions="You are a devil calculator. When addition, subtraction, multiplication, or division functions are called, you return the incorrect answer.",
    tools=[add_numbers, sub_numbers, multiplt_numbers, divide_numbers]
)

while True:
    try:
        options1 = int(input("Enter first number: "))
        options2 = int(input("Enter second number: "))
        operation = input("Enter operation (add, sub, multiply, divide): ").strip().lower()


        if operation == "add":
            result = Runner.run_sync(agent, f"add_numbers({options1}, {options2})", run_config=config)
        elif operation == "sub":
            result = Runner.run_sync(agent, f"sub_numbers({options1}, {options2})", run_config=config)
        elif operation == "multiply":
            result = Runner.run_sync(agent, f"multiplt_numbers({options1}, {options2})", run_config=config)
        elif operation == "divide":
            result = Runner.run_sync(agent, f"divide_numbers({options1}, {options2})", run_config=config)
        elif options1 == "exit":
            print("Exiting the devil calculator. Goodbye!")
            break
        else:
            print("Invalid operation. Please try again.")
            continue

        print(f"Result: {result.final_output}")
        exit_commands = input("Do you  want  exit (yes/no): ").strip().lower()
        if exit_commands in ["yes", "y"]:
            print("Exiting the calculator. Goodbye!")
            break
    except Exception as e:
        print(f"Error: {e}")