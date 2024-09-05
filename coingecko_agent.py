import os
import requests
import autogen

# Define the configuration directly in the Python code
#open_api_key= put your chat-gpt keys 
#coin-gecko key = CG-FNinjK8Xx68KNtnrATojM7sT
config_list = [
    {
        "model": "gpt-3.5-turbo",
        "api_key": os.environ.get("CHATGPT_API_KEY", "open_api_key"),
        "base_url": "https://api.openai.com/v1/completions",
        "temperature": 0.7,  # Adjust creativity level
    },
    {
        "model": "coingecko",
        "api_key": os.environ.get("COINGECKO_API_KEY", "coin-gecko-key"),
        "base_url": "https://api.coingecko.com/api/v3/coins/",
        "tags": ["coingecko", "crypto"],
    }
]

# Create assistant agent with config list
llm_config = {"config_list": config_list}
assistant = autogen.AssistantAgent(name="CoinGeckoAgent", llm_config=llm_config)

# Function to get current coin data by ID
def get_coin_info(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    response = requests.get(url)
    return response.json()

# Function to get historical coin data by ID and date (format: dd-mm-yyyy)
def get_coin_history(coin_id, date):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/history?date={date}" #bitcoin #30-12-2023
    response = requests.get(url)
    return response.json()

# Example usage
coin_data = get_coin_info("bitcoin")
print("Current Coin Data:", coin_data)

historical_data = get_coin_history("bitcoin", "01-09-2023")
print("Historical Coin Data on 01-09-2023:", historical_data)
