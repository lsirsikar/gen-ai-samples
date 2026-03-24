# pg_client.py
import sys
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
from strands.models import BedrockModel

# 1. Setup parameters to run the local server script
server_params = StdioServerParameters(
    command=sys.executable,
    args=["mysql_server.py"]
)

# 2. Initialize the MCP Client
mcp_client = MCPClient(lambda: stdio_client(server_params))

bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
    streaming=False
)

def run_db_agent():
    # 3. Use the context manager to manage the server process
    with mcp_client:
        # Discover tools from the PostgreSQL server
        tools = mcp_client.list_tools_sync()

        agent = Agent(
            model=bedrock_model,
            tools=tools,
            system_prompt="You are a senior data analyst. Use SQL to answer questions from the database.",
            callback_handler=None  # Disable internal reasoning logs
        )


        # The agent will generate and run the SQL for you
        query = "Give me list of tables in this database."
        result = agent(query)

        print(f"Agent Analysis: {str(result)}")

        while True:

            user_input = input("You: ")
            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "bye"]:
                break

            result = agent(user_input)
            print(f"\n\nAgent: {result}")


if __name__ == "__main__":
    run_db_agent()
