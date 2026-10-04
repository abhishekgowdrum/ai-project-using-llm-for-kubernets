from datetime import date
import subprocess
from langchain.agents import create_agent
#LLM
from langchain_ollama import ChatOllama

#Tools
from langchain_core.tools import tool

#Lets coonect with LLM
llm = ChatOllama(
    model="gemma4:e2b",
    temperature = 0,
    num_ctx = 8000
)

@tool
def get_date():
    """
    Get the current date from system
    """
    return date.today()

@tool
def get_pods():
    """
    get kubernetes pods 
    """
    return subprocess.run(["kubectl","get","pods"],capture_output = True, text = True)

#LLM+Tools

agent =create_agent(
    model = llm,
    tools= [get_pods,get_date],
    system_prompt= "You are a devops assistant that can answer user quieries  such as getting kubernetes pods,getting dates,etc "
)

question=input("ask Ai agent")
response = agent.invoke({"messages":[("user",question)]})
print(response ["messages"][-1].content)