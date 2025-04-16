# app.py
import requests

def main():
    print("Hello, World!")

    # Simple HTTP GET request to test the requests library
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    if response.status_code == 200:
        print("Successfully fetched data from API:")
        print(response.json())
    else:
        print("Failed to fetch data from API.")

if __name__ == "__main__":
    main()

