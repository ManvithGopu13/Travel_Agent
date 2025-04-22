from langchain_ollama import ChatOllama
from duckduckgo_search import DDGS
from langchain.tools import DuckDuckGoSearchRun
from langchain.schema.runnable import RunnableLambda

search = DuckDuckGoSearchRun()
llm = ChatOllama(model = "qwen2.5:7b")

async def _accomodation(location: str) -> str:
    query = f"Best hostels , dormitories , public restplaces to stay in {location} with pricing and website links."
    results = search.run(query)
    prompt = f"List good hostels/dorms/dharamasatras or public restplaces in {location} from this {results}\n\n Provide name, type, price per night.Make it under 100-150 words"
    output = llm.invoke(prompt)
    return output.content

accomodation_agent = RunnableLambda(func=_accomodation)