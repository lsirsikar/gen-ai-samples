# quicksight_agent.py
import sys
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
from strands.models import BedrockModel


def main():
    print("🚀 Setting up MCP Servers (MySQL & Postgres)...")
    
    # Define server parameters
    mysql_params = StdioServerParameters(
        command=sys.executable,
        args=["mysql_server.py"]
    )
    postgres_params = StdioServerParameters(
        command=sys.executable, 
        args=["psql_server.py"]
    )
    
    # Create MCPClient instances
    mysql_client = MCPClient(lambda: stdio_client(mysql_params))
    postgres_client = MCPClient(lambda: stdio_client(postgres_params))
    
    print(f"✅ Created MCP clients")
    
    try:
        # Initialize the model
        model = BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
            region_name="us-east-1",
            streaming=False
        )

        # Create agent with MCP clients directly
        # Pass the MCPClient objects - the Agent will manage their lifecycle
        agent = Agent(
            model=model,
            tools=[mysql_client, postgres_client],
            system_prompt="You are a security analyst with access to MySQL logs and Postgres database."
        )
        
        # Define the task
        user_query = (
            "Check the MySQL for activity, violations and incident data in the last 30 mins. "
            "Correlate the activity, violations and incident data and present it in csv format."
        )
        
        print(f"\n🤖 Agent Task: {user_query}\n")
        
        # Run the agent - it will automatically manage the MCP client contexts
        final_answer = agent(user_query)
        
        print("\n--- Final Agent Response ---")
        print(final_answer)
    
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
