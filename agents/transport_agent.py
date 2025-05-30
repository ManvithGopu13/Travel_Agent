from langchain_ollama import ChatOllama
from duckduckgo_search import DDGS
from langchain.tools import DuckDuckGoSearchRun
from langchain.schema.runnable import RunnableLambda

search = DuckDuckGoSearchRun()
llm = ChatOllama(model = "qwen2.5:7b")

async def _transport(location: str) -> str:
    query = f"How to reach {location} by train, bus, or private vehicles and local transport options"
    results = search.run(query)
    prompt = f"Give the transport info for reaching and travelling inside {location}: \n\n {results}\n\n break down into train, bus , car , local transport.Make it under 70-80 words in the form  of paragraphs"
    output = llm.invoke(prompt)
    return output.content

transport_agent = RunnableLambda(func=_transport)