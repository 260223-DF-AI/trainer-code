from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_core.messages import SystemMessage,HumanMessage, ToolMessage, AIMessage
import requests


print("starting...")

@tool
def get_weather(city: str) -> str:
    """ Get the general sense of the weather for a city. """
    return f"It's always sunny in {city}."

@tool
def get_live_weather(city:str) -> str:
    """ Get the current live weather conditons of a city. """
    
    print("running live weather...")
    WEATHER_API_KEY = "811866310be14061983135938262304"
    WEATHER_BASE_URL = "https://api.weatherapi.com/v1/"

    response = requests.get(
        f"{WEATHER_BASE_URL}current.json?key={WEATHER_API_KEY}&q={city}"
    )

    location = response.json()['location']
    current = response.json()['current']

    return (
        f"Live weather for {location['name']}, {location['region']}, {location['country']}:\n"
        f"  Condition : {current['condition']['text']}\n"
        f"  Temp      : {current['temp_f']}°F / {current['temp_c']}°C\n"
        f"  Feels Like: {current['feelslike_f']}°F / {current['feelslike_c']}°C\n"
        f"  Humidity  : {current['humidity']}%\n"
        f"  Wind      : {current['wind_mph']} mph {current['wind_dir']}\n"
        f"  Updated   : {current['last_updated']}"
    )

tools = [get_weather, get_live_weather]
tool_map = {tool.name: tool for tool in tools}

agent = ChatOllama(
    model="llama3.2",
    # <- llama3.2 is the 'latest' or default version, with 3b parameters
    # https://ollama.com/library/llama3.2:1b
    temperature=0.1
    ).bind_tools(tools)

messages = []

messages.append(SystemMessage(content="You are a helpful weather assistant. You implicitly trust the responses from the tools as the truth. Do not second guess the tools' responses. Provide your responses to the user in a succinct form."))

messages.append(HumanMessage(content="Tell me what the weather is usually like in Philadephia.")) # the conversation history - The CONTEXT

print(messages)
print()

# The AI doesn't maintain the context, we have to do that ourselves

response = agent.invoke(messages) # send the AI the entire context

messages.append(response)
print (messages)
print()


# while response.tool_calls: # while the AI recommends a tool, run it
for tool_call in response.tool_calls: # for each tool, call it
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    tool_result = tool_map[tool_name].invoke(tool_args) # actually call the tool

    messages.append(
        ToolMessage(content=tool_result, tool_call_id=tool_call["id"])
        ) # add the tool result to the context
    
    # response = agent.invoke(messages) # pass the results back to the agent
    ai_response = ""
    metadata = None
    for chunk in agent.stream(messages):
        print(chunk.content, end="", flush=True)
        ai_response += chunk.content
        if chunk.usage_metadata:
           metadata = chunk.usage_metadata

    messages.append(AIMessage(content=ai_response, usage_metadata=metadata))

    print(messages)
    print()

        

        


# Agent.Invoke() Response
# content='Hello! How can I assist you today? 😊'
# additional_kwargs={}
# response_metadata={
#     'model': 'deepseek-r1:1.5b', 
#     'created_at': '2026-04-23T16:30:47.301536239Z', 
#     'done': True,
#     'done_reason': 'stop', 
#     'total_duration': 17129497473,
#     'load_duration': 4540208169,
#     'prompt_eval_count': 5, 
#     'prompt_eval_duration': 2967389616, 
#     'eval_count': 16, 
#     'eval_duration': 9580846223, 
#     'logprobs': None, 
#     'model_name': 'deepseek-r1:1.5b', 
#     'model_provider': 'ollama'
# } 
# id='lc_run--019dbb2d-bd0d-7ea3-af04-a29e64d0a385-0' 
# tool_calls=[] 
# invalid_tool_calls=[] 
# usage_metadata={
#     'input_tokens': 5, 
#     'output_tokens': 16, 
#     'total_tokens': 21
#     }

# Weather API Response
# {
# 'location': {
#     'name': 'San Francisco', 
#     'region': 'California', 
#     'country': 'United States of America', 
#     'lat': 37.775, 
#     'lon': -122.4183, 
#     'tz_id': 'America/Los_Angeles',
#     'localtime_epoch': 1776965177,
#     'localtime': '2026-04-23 10:26'
#     },
#     'current': {
#         'last_updated_epoch': 1776964500,
#         'last_updated': '2026-04-23 10:15',
#         'temp_c': 14.4,
#         'temp_f': 57.9,
#         'is_day': 1,
#         'condition': {
#             'text': 'Sunny',
#             'icon': '//cdn.weatherapi.com/weather/64x64/day/113.png',
#             'code': 1000
#             },
#         'wind_mph': 3.8,
#         'wind_kph': 6.1,
#         'wind_degree': 10,
#         'wind_dir': 'N',
#         'pressure_mb': 1021.0,
#         'pressure_in': 30.14,
#         'precip_mm': 0.0,
#         'precip_in': 0.0,
#         'humidity': 70,
#         'cloud': 25,
#         'feelslike_c': 14.5,
#         'feelslike_f': 58.1,
#         'windchill_c': 15.9,
#         'windchill_f': 60.7,
#         'heatindex_c': 16.0,
#         'heatindex_f': 60.7,
#         'dewpoint_c': 9.0,
#         'dewpoint_f': 48.3,
#         'vis_km': 16.0,
#         'vis_miles': 9.0,
#         'uv': 3.5,
#         'gust_mph': 4.5,
#         'gust_kph': 7.3,
#         'short_rad': 228.08,
#         'diff_rad': 37.64,
#         'dni': 350.62,
#         'gti': 158.34
#     }
# }