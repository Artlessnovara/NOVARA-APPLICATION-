import requests
import os

BASE_URL = 'http://127.0.0.1:5000'

def test_signup_and_login():
    # --- Test Signup ---
    signup_data = {
        'full_name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'role': 'Student'
    }

    # We need to get the CSRF token first.
    # For simplicity in this test, we'll assume a session and get the token.
    # In a real testing scenario, you'd use a testing client from Flask.

    with requests.Session() as s:
        # Get the signup page to get the CSRF token
        r = s.get(f"{BASE_URL}/auth/signup")

        # A simple way to extract the token - this is brittle and for demo purposes only
        try:
            csrf_token = r.text.split('name="csrf_token" type="hidden" value="')[1].split('"')[0]
            signup_data['csrf_token'] = csrf_token
        except IndexError:
            print("Could not find CSRF token. Skipping signup test.")
            return

        print("Testing signup...")
        r = s.post(f"{BASE_URL}/auth/signup", data=signup_data, allow_redirects=True)

        if r.status_code == 200 and "You have successfully signed up! Please login." in r.text:
            print("Signup successful!")
        else:
            print(f"Signup failed. Status: {r.status_code}, Response: {r.text[:200]}")
            return # Stop if signup failed

        # --- Test Login ---
        login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }

        # Get the login page to get a new CSRF token
        r = s.get(f"{BASE_URL}/auth/login")
        try:
            csrf_token = r.text.split('name="csrf_token" type="hidden" value="')[1].split('"')[0]
            login_data['csrf_token'] = csrf_token
        except IndexError:
            print("Could not find CSRF token for login. Skipping login test.")
            return

        print("\nTesting login...")
        r = s.post(f"{BASE_URL}/auth/login", data=login_data, allow_redirects=True)

        if r.status_code == 200 and "Test User" in r.text:
            print("Login successful!")
        else:
            print(f"Login failed. Status: {r.status_code}, Response: {r.text[:200]}")


if __name__ == '__main__':
    test_signup_and_login()
