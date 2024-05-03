import requests
import os 

def extract_search_results(response):
    top_heading = "Here are your search results"
    results = [top_heading]
    if 'webPages' in response and 'value' in response['webPages']:
        for item in response['webPages']['value']:
            url = item.get('url', 'No URL available')
            content = item.get('snippet', 'No content available')
            result = f"url: {url}\ncontent: {content}"
            results.append(result)
    return "\n\n".join(results)


def bing_web_search(query:str):
    # set parameters
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": os.environ['BING_SUBSCRIPTION_KEY']}
    params = {
        "q": query,
        "textDecorations": True,
        "textFormat": "HTML"}
    # get response
    response = requests.get(search_url, headers=headers, params=params)
    return extract_search_results(response.json())