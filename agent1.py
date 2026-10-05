from datetime import date
import subprocess

from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool


# LLM
llm = ChatOllama(
    model="gemma3:1b",
    temperature=0,
    num_ctx=4000
)


# Tools

@tool
def get_date():
    """
    Get the current date from system
    """
    return str(date.today())


@tool
def get_pods():
    """
    Get Kubernetes pods
    """
    result = subprocess.run(
        ["kubectl", "get", "pods", "-A"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout


# LLM + Tools

agent = create_agent(
    model=llm,
    tools=[get_pods, get_date],
    system_prompt=(
        "You are a DevOps assistant. "
        "You can help with Kubernetes pods and dates. "
        "Use the available tools when necessary."
    )
)


question = input("Ask AI agent: ")

response = agent.invoke(
    {"messages": [("user", question)]}
)

print(response["messages"][-1].content)
