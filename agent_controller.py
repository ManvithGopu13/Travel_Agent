from langchain.schema.runnable import RunnableParallel
from agents.place_info_agent import place_info_agent
from agents.accomodation_agent import accomodation_agent
from agents.transport_agent import transport_agent
from agents.map_agent import map_agent
from agents.iterenary_agent import iterenary_agent


async def handle_location_query(location):
    data = {
        "place_info": await place_info_agent.ainvoke(location),
        "accommodation": await accomodation_agent.ainvoke(location),
        "transport": await transport_agent.ainvoke(location),
        "map": await map_agent.ainvoke(location),
    }

    iterenary = await iterenary_agent.ainvoke(data)
    final_response = f"{data['place_info']} \n\n {data['accommodation']}\n\n{data['transport']}\n\n{data['map']}\n\n📅 Itinerary:\n{iterenary}"
    
    return final_response

