import requests

# URL to check
url = 'https://www.example.com'

def check_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Website {url} is up and running!")
        else:
            print(f"Website {url} returned status code {response.status_code}.")
    except requests.exceptions.RequestException as e:
        print(f"Website {url} is down. Error: {e}")

check_website(url)
