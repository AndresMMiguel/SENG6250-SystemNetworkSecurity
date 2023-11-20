import requests
import hashlib


if __name__ == "__main__":

    # Start the program
    r = requests.get("http://127.0.0.1:2250/start")
    print(r.json()["text"])

    # Login before requesting any service
    print("LOGIN")
    username = input("Enter username: ")
    password = input("Enter password: ")
    token = input("Enter token, leave it blank if you don't have one: ")
    password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    r = requests.post("http://127.0.0.1:2250/login", data={"username": username, "password": password, "token": token})
    print(r.json()["text"])

    # Insert access code
    try:
        if (r.json()["access"]):
            accessCode = input("Enter access code: ")
            r = requests.post("http://127.0.0.1:2250/login/access_code", data = {"accessCode": accessCode})
            print(r.json()["text"])
            token = r.json()["token"]
            token = input("Enter token: ")
            r = requests.post("http://127.0.0.1:2250/login/token", data = {"token": token})
            print(r.json()["text"])
    except KeyError:
        pass