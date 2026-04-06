import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_ollama import ChatOllama
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

class InitArgs(BaseModel):
    project_name: str = Field(default=".")
    auth: bool = Field(default=False)
    storage: bool = Field(default=True)
    metrics: bool = Field(default=False)
    db: str = Field(default="sqlite")
    storage_type: str = Field(default="file")
    validation_mode: str = Field(default="strict")

async def run_agent():
    server_params = StdioServerParameters(command="uv", args=["run", "fabrica-mcp"])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            async def init_project(**kwargs) -> str:
                result = await session.call_tool("fabrica_init", arguments=kwargs)
                return result.content[0].text

            fabrica_tool = StructuredTool.from_function(
                coroutine=init_project,
                name="fabrica_init",
                description="Initialize a new Fabrica project.",
                args_schema=InitArgs,
            )

            llm = ChatOllama(model="qwen2.5-coder:7b", base_url="http://127.0.0.1:11434")
            tools = [fabrica_tool]
            
            agent_executor = create_react_agent(llm, tools)
            
            print("Sending prompt to LLM...")
            result = await agent_executor.ainvoke({
                "messages": [("user", "Initialize a new Fabrica project called 'llm_test_proj' with a postgres database and metrics enabled.")]
            })
            
            for msg in result["messages"]:
                print(f"\n[{msg.__class__.__name__}]:\n{msg.content}")

if __name__ == "__main__":
    asyncio.run(run_agent())