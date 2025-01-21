import requests

API_BASE_URL = "https://api.potterdb.com/v1/"

def test_api_endpoint(endpoint, params=None):
    try:
        url = f"{API_BASE_URL}{endpoint}"
        print(f"Testing endpoint: {url} with params: {params}")
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Response Data: {data}")
        print("="*50)
    except requests.exceptions.RequestException as e:
        print(f"Error testing endpoint {endpoint}: {e}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")

def main():
    test_api_endpoint("characters", {"page[number]": 1})
    test_api_endpoint("spells", {"page[number]": 1, "filter[name_cont]": "Expelliarmus"})
    test_api_endpoint("movies")
    test_api_endpoint("potions", {"page[number]": 2})

if __name__ == "__main__":
    main()

