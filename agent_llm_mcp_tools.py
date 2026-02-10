from strands import Agent, tool
from strands.models import BedrockModel
from strands.models.ollama import OllamaModel
from strands.models.llamaapi import LlamaAPIModel
from strands.models.gemini import GeminiModel
from strands.models.llamacpp import LlamaCppModel
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters


@tool
def person_info(query):
    # Ollama
    ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3:8b"
    )

    system_prompt_cmd = """
    You are a very good agent that brings information about persons from wikipedia.
    """

    agent = Agent(
        model=ollama_model,
        system_prompt=system_prompt_cmd  # Pass the persona here
    )

    response = agent(query)
    return response


@tool
def geography_info(query):
    # Ollama
    ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3:8b"
    )

    system_prompt_cmd = """
    You are a very good agent that brings information about geographies from google.com.
    """

    agent = Agent(
        model=ollama_model,
        system_prompt=system_prompt_cmd  # Pass the persona here
    )

    response = agent(query)
    return response


bedrock_model = BedrockModel(
  model_id="us.amazon.nova-pro-v1:0",
  region_name="us-east-1",
  temperature=0.3,
  streaming=True, # Enable/disable streaming
)

def call_model():
    system_prompt_cmd = """
    You are a very good agent that understands user query and takes relevant action.
    
    Instructions:
    - if related to person or geography, let's use tools.
    - if related to technical documentation, let's use MCP server.
    - if anything else, let's use underlying model only.

    Respond to the user in one line sentence only using natural language.
    """

    aws_docs_client = MCPClient(
        lambda: stdio_client(StdioServerParameters(command="uvx", args=["awslabs.aws-documentation-mcp-server@latest"]))
    )

    with aws_docs_client:
        agent = Agent(
            model=bedrock_model,
            system_prompt=system_prompt_cmd,  # Pass the persona here
            tools=[person_info, geography_info] + aws_docs_client.list_tools_sync()
        )

        print("Agent is ready! Type 'exit' to quit.")

        while True:
            user_query = input("\nUser query: ")

            if not user_query:
                continue
            
            if user_query.lower() in ["exit", "quit"]:
                break

            print("\n--- Generated Response from Agent: ---")
            response = agent(user_query)
            

if __name__=="__main__":
    call_model()
