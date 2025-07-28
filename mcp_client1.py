import os
import asyncio
import subprocess
from mcp import ClientSession
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient

# Set environment variables
os.environ["GOOGLE_API_KEY"] = "AIzaSyAgTgVwISHCTSiZwE9rpbymHR-VI9q-Tio"

# Find the full path to npx
try:
    npx_path = subprocess.check_output(["which", "npx"]).decode().strip()
    print(f"Using npx from: {npx_path}")
except subprocess.CalledProcessError:
    npx_path = "npx"  # Fall back to just "npx" if we can't find it
    print("Could not determine npx path, using default 'npx'")

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Create the MultiServerMCPClient
client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            "args": ["/opt/MCP_Demo/mcp_server.py"],
            "transport": "stdio",
        },
        "postgres": {
            "command": npx_path,
            "args": ["-p", "@modelcontextprotocol/server-postgres", "@modelcontextprotocol/server-postgres"],
            "env": {
                "DATABASE_URL": "postgresql://bhargav:Bhargav%40264@localhost:5432/stocks_data",
                "PATH": os.environ.get("PATH", "")  # Pass the current PATH
            },
            "transport": "stdio",
        }
    }
)

async def run_agent():
    try:
        async with client:
            print("Client initialized successfully")
            all_tools = client.get_tools()
            print(f"Found {len(all_tools)} tools")
            agent = create_react_agent(llm, all_tools)
            print("Agent created, invoking query...")
            agent_response = await agent.ainvoke({"messages": "what is industry of paytm"})
            return agent_response
    except Exception as e:
        print(f"Error in run_agent: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    result = asyncio.run(run_agent())
    print(result)