import requests
import hashlib


if __name__ == "__main__":

    # Start the program
    r = requests.get("http://127.0.0.1:2250/start")
    print(r.json()["text"])

    # Login before requesting any service
    print("LOGIN")
    username = "root"
    password = r.json()["password"]
    print("Username: " + username)
    print("Password: " + password)
    password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    r = requests.post("http://127.0.0.1:2250/login", data={"username": username, "password": password})
    print(r.json()["text"])

    # Insert access code and token
    try:
        if (r.json()["access"]):
            accessCode = r.json()["accessCode"]
            print("Access Code: " + accessCode)
            r = requests.post("http://127.0.0.1:2250/login/access_code", data = {"accessCode": accessCode})
            print(r.json()["text"])
            # Auto populate token and send post request
            token = r.json()["token"]
            print("Enter token: " + token)
            r = requests.post("http://127.0.0.1:2250/login/token", data = {"token": token})
            print(r.json()["text"])
    except KeyError:
        print(r.json()["text"])