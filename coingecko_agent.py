import os
import requests
import autogen
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

print(type(os.environ.get("CHATGPT_API_KEY")))

# Configurations for OpenAI LLMs or other services
config_list =[{"model": "gpt-3.5-turbo", "api_key": os.environ.get("CHATGPT_API_KEY")}]
# config_list = [
#     {
#         "model": "gpt-3.5-turbo",
#         "api_key": os.environ.get("CHATGPT_API_KEY", "open_api_key"),
#         "temperature": 0.7,  # Adjust creativity level
#     }
# ]

# Function to get current coin data by ID
def get_coin_info(coin_id: str) -> str:  # Added return type
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:

    # Save response to coin info.json file
     with open("coin_info.json", "w") as file:
        file.write(response.text)
     return "coin information keys: " + str(response.json().keys())

# Function to get historical coin data by ID and date (format: dd-mm-yyyy)
def get_coin_history(coin_id: str, date: str) -> str:  # Added return type
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/history?date={date}"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    with open("coin_history.json", "w") as file:
        file.write(response.text)
    return "Coin history keys: " + str(response.json().keys())

def display_json_data(file_path: str) -> None:
    with open(file_path, "r") as file:
        data = json.load(file)
        print(data)

# Create an assistant agent for queries
llm_config = {"config_list": config_list}

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",  # Change to ALWAYS for user input handling
    code_execution_config={"work_dir": "coding", "use_docker": False, "last_n_messages": 3},
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
)

assistant = autogen.AssistantAgent(
    name="CoinGeckoAgent",
    system_message="You are an agent that provides cryptocurrency data. You can fetch current and historical data using functions.", 
    llm_config=llm_config
)

# Register functions with AutoGen
autogen.agentchat.register_function(
    get_coin_info,
    caller=assistant,
    executor=user_proxy,
    description="Fetch current cryptocurrency data by coin ID and save it to coin_info.json."
)

autogen.agentchat.register_function(
    get_coin_history,
    caller=assistant,
    executor=user_proxy,
    description="Fetch historical cryptocurrency data by coin ID and date and save it to coin_history.json."
)

autogen.agentchat.register_function(
    display_json_data,
    caller=assistant,
    executor=user_proxy,
    description="Display JSON data from a file."
)

# Group the agents for interaction
agents = [user_proxy, assistant]

# Chat initiation
def initiate_chat(query: str) -> None:
    group_chat = autogen.GroupChat(
        agents=agents, messages=[], max_round=3, speaker_selection_method="round_robin"
    )
    
    manager = autogen.GroupChatManager(group_chat, llm_config=llm_config)

    result = user_proxy.initiate_chat(
        manager, 
        message=query,
    )

if __name__ == "__main__":
    query = input("Enter the query: ")

    if not query:
        query = """What is the current price of Bitcoin (ID: bitcoin)"""
    
    initiate_chat(query=query)
    # print(get_coin_info("bitcoin").keys())
