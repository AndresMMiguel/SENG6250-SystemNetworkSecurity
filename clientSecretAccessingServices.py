import requests
import hashlib


if __name__ == "__main__":

    # Start the program
    r = requests.get("http://127.0.0.1:2250/start")
    print(r.json()["text"])
    print()

    # Login before requesting any service
    print("LOGIN")
    username = "secret"
    password = username
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
            token = r.json()["token"]
            print("Enter token: " + token)
            r = requests.post("http://127.0.0.1:2250/login/token", data = {"token": token})
            print(r.json()["text"])
    except KeyError:
        print(r.json()["text"])
    print()
        

    # ADD USER
    print("ADD USER")
    r = requests.post("http://127.0.0.1:2250/admin_console", data={"action": "addUser","username": username})
    print(r.text)
    print()

    # MODIFY USER
    print("MODIFY USER")
    r = requests.post("http://127.0.0.1:2250/admin_console", data={"action": "modifyUser", "username": username})
    print(r.text)
    print()

    # DELETE USER
    print("DELETE USER")
    r = requests.post("http://127.0.0.1:2250/admin_console", data={"action": "deleteUser", "username": username})
    print(r.text)
    print()

    # AUDIT EXPENSES
    print("AUDIT EXPENSES")
    r = requests.post("http://127.0.0.1:2250/audit_expenses", data={"username": username})
    print(r.text)
    print()

    # ADD EXPENSE
    print("ADD EXPENSE")
    r = requests.post("http://127.0.0.1:2250/add_expense", data={"expense": "50 AUD. ", "username": username})
    print(r.text)
    print()

    # AUDIT TIMESHEETS
    print("AUDIT TIMESHEETS")
    r = requests.post("http://127.0.0.1:2250/audit_timesheets", data={"username": username})
    print(r.text)
    print()

    # SUBMIT TIMESHEET
    print("SUBMIT TIMESHEET")
    r = requests.post("http://127.0.0.1:2250/submit_timesheet", data={"timesheet": "10:00 pm. ", "username": username})
    print(r.text)
    print()

    # VIEW MEETING MINUTES
    print("VIEW MEETING MINUTES")
    r = requests.post("http://127.0.0.1:2250/view_meeting_minutes", data={"username": username})
    print(r.text)
    print()

    # ADD MEETING MINUTES
    print("ADD MEETING MINUTES")
    r = requests.post("http://127.0.0.1:2250/add_meeting_minutes", data={"meetingMinutes": "In this meeting... ", "username": username})
    print(r.text)
    print()

    # VIEW ROSTER
    print("VIEW ROSTER")
    r = requests.post("http://127.0.0.1:2250/view_roster", data={"username": username})
    print(r.text)
    print()

    # ROSTER SHIFT
    print("ROSTER SHIFT")
    r = requests.post("http://127.0.0.1:2250/roster_shift", data={"roster": "Ryan shifted to 8 am. ", "username": username})
    print(r.text)
    print()