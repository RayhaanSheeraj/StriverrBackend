import requests

def get_quotes(api_key, category=None):
    """
    Fetches quotes from the API Ninjas quotes endpoint.

    Args:
        api_key (str): Your API key for authentication.
        category (str, optional): A category to filter quotes (e.g., "inspirational", "love").

    Returns:
        dict: A dictionary containing the response data if the request is successful.
        None: If the request fails, returns None.
    """
    api_url = 'https://api.api-ninjas.com/v1/quotes'


    params = {'category': category} if category else {}

    try:
        response = requests.get(api_url, headers={'X-Api-Key': api_key}, params=params)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            print("Error:", response.status_code, response.text)
            return None
    except requests.RequestException as e:
        print("An error occurred:", e)
        return None

# Example usage
if __name__ == "__main__":
    API_KEY = 'dsH4Bmo4W7wv5SVKvjbSRQ==mRJPmT9DcU5oqtI7' 
    category = "inspirational" #optional

    quotes = get_quotes(API_KEY, category=category)

    if quotes:
        for i, quote in enumerate(quotes, start=1):
            print(f"Quote {i}: {quote['quote']}\n - {quote['author']}\n")
