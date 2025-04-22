from langchain_ollama import ChatOllama
from duckduckgo_search import DDGS
from langchain.tools import DuckDuckGoSearchRun
from langchain.schema.runnable import RunnableLambda

search = DuckDuckGoSearchRun()
llm = ChatOllama(model = "qwen2.5:7b")

async def _place_info(location: str) -> str:
    query = f"Top 15 tourist places to isit in {location} with  details like timings, entry fee, and history"
    results = search.run(query)
    prompt = f"Extract and format tourist info from this search result:\n\n{results}\n\nProvide 15 entries with name, history, timings, and entry fee."
    return llm.invoke(prompt)

place_info_agent = RunnableLambda(func=_place_info)