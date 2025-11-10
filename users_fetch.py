""" Task Description 
1. Use the GET method to call the following public API endpoint: https://jsonplaceholder.typicode.com/users 
2. The API returns a list of users in JSON format. Loop through each user and display the following details: • Name • Username • Email • City (from address.city) 
3. The output should look like this: 
User 1: 
Name: Leanne Graham 
Username: Bret 
Email: Sincere@april.biz 
City: Gwenborough
4. Use the 'requests' library for the API call. 
5. (Optional Bonus) 
• Print only users whose city name starts with the letter 'S'. 
• Handle API errors (e.g., failed response or empty list). """

import requests
import argparse
import sys

API_URL = "https://jsonplaceholder.typicode.com/users"

def fetch_users():
    try:
        resp = requests.get(API_URL, timeout=10)
    except requests.RequestException as e:
        print(f"Network error while calling API: {e}")
        return None

    if resp.status_code != 200:
        print(f"API returned non-200 status code: {resp.status_code}")
        return None

    try:
        data = resp.json()
    except ValueError:
        print("Failed to parse JSON from response.")
        return None

    if not isinstance(data, list) or len(data) == 0:
        print("API returned empty list or unexpected data.")
        return None

    return data

def print_users(users, starts_with=None):
    count = 0
    for i, user in enumerate(users, start=1):
        # Safely extract fields with fallback
        name = user.get("name", "N/A")
        username = user.get("username", "N/A")
        email = user.get("email", "N/A")
        city = user.get("address", {}).get("city", "N/A")

        if starts_with:
            if not city or not isinstance(city, str) or not city.lower().startswith(starts_with.lower()):
                continue

        count += 1
        print(f"User {count}:")
        print(f"Name: {name}")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"City: {city}")
        print("-" * 24)

    if count == 0:
        print("No users matched the filter.")

def main():
    parser = argparse.ArgumentParser(description="Fetch and display users from jsonplaceholder.typicode.com")
    parser.add_argument("--starts-with", "-s", help="Print only users whose city starts with this letter", type=str)
    args = parser.parse_args()

    users = fetch_users()
    if users is None:
        sys.exit(1)

    print_users(users, starts_with=args.starts_with)

if __name__ == "__main__":
    main()
