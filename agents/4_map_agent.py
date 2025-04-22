from langchain_ollama import ChatOllama
from langchain.schema.runnable import RunnableLambda
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import AgentExecutor, create_openai_functions_agent, create_tool_calling_agent, create_react_agent, Agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import folium
from geopy.geocoders import Nominatim
import asyncio
import os


search = DuckDuckGoSearchRun()
llm = ChatOllama(model="qwen2.5:7b")
geolocator = Nominatim(user_agent="travel_bot")

async def _generate_map(location: str) -> str:
    # query = f"Name the Top 15 must-visit places in and near to {location}."
    # query = f"Top 15 tourist places in {location}"
    # results = search.run(query)
    # print(results)
    # prompt = f"Extract 15 major tourist attraction places to visit in and near {location}.Only return the place name, with it's coordinates, one per line. Return format : Place name - latitude, longitude"
    prompt = f"Extract atleast 15 tourist places to visit in and near {location}. Only return the place name , one per line. Return format : Place name . Jus the format nothing more , like numbers  "
    
    ai_response = llm.invoke(prompt)
    print(ai_response.content)
    places = ai_response.content.strip().split("\n")
    # result = await agent_executor.ainvoke({"location": location})
    # print(f"Result : {result}")

    # places = result["output"].strip().split("\n")

    coordinates = []
    for place in places:
        # print(f"==={place}===")
        try:
            # full_query = f"{place}, {location}"
            full_query = f"{place}"
            geo = geolocator.geocode(full_query)
            if geo:
                coordinates.append((place, geo.latitude, geo.longitude))
                print(f"{place}; lat: {geo.latitude}; long: {geo.longitude}")
            else :
                print(f"No coordinates found for {place}")
            # name_part , coords_part = place.split(" - ")
            # lat_str, lon_str = coords_part.split(", ")
            # print(f"place name: {name_part}, latitude : {lat_str} and {float(lat_str)}, longitude: {lon_str} and {float(lon_str)}")
            # coordinates.append((name_part.strip(), float(lat_str), float(lon_str)))
        except:
            print(f"No coordinates found for {place}")
            continue

    if not coordinates:
        return "Couldn't geocode any places for this location. Try a more specific location."
    
    center_lat, center_lng = coordinates[0][1], coordinates[0][2]
    fmap = folium.Map(location=[center_lat, center_lng], zoom_start=13)

    for name, lat, lng in coordinates:
        folium.Marker(location=[lat, lng], popup=name, tooltip=name, icon=folium.Icon(color = "red")).add_to(fmap)

    map_path = f"maps/{location.replace(' ', '_')}_travel_map.html"
    os.makedirs("maps", exist_ok=True)
    fmap.save(map_path)

    return f"Here's the interactive travel map for {location}!\n Open this file: '{map_path}'"


map_agent = RunnableLambda(func=_generate_map)