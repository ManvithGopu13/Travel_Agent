from langchain_ollama import ChatOllama
from langchain.schema.runnable import RunnableLambda

llm = ChatOllama(model = "qwen2.5:7b")

async def _generate_itenerary(all_data: dict) -> str:
    prompt = f"""Based on the following travel information, generate a 4-5 day travel itinerary covering most of the places:

Tourist Places: {all_data['place_info']}
Accommodations: {all_data['accommodation']}
Transport Info: {all_data['transport']}

Include arrival day, daily plans, lodging suggestions, and travel times.
Under 200 words.
"""
    
    output = llm.invoke(prompt)
    return output.content

iterenary_agent = RunnableLambda(func=_generate_itenerary)