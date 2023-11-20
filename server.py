import json
import os
import requests
import string
import random
import hashlib
from datetime import datetime
from flask import Flask, request, redirect, url_for
app = Flask(__name__)


users = open('data/users.json')
users = json.load(users)
userAccessing = "root"
userLogged = ""

def store_json():
    with open("data/users.json", "w") as outfile:
        json.dump(users, outfile, indent=2)


# Function to send a new user email via Mailgun API
def send_psswd_mail(username, password, email):
	return requests.post(
		"https://api.mailgun.net/v3/sandbox107d37aac3a94f43bca9d0e7b0a09769.mailgun.org/messages",
		auth=("api", "b309c1e12d23f8a1c8704a34a8047763-5465e583-b3e236d1"),
		data={"from": "Mako <mailgun@sandbox107d37aac3a94f43bca9d0e7b0a09769.mailgun.org>",
			"to": email,
			"subject": "Account created",
			"text": "Congratulations on creating your profile, here is your access information: \n Username: " + username + "\n Password: " + password})


# Function to send the access code email via Mailgun API
def send_access_mail(accessCode, email):
	return requests.post(
		"https://api.mailgun.net/v3/sandbox107d37aac3a94f43bca9d0e7b0a09769.mailgun.org/messages",
		auth=("api", "b309c1e12d23f8a1c8704a34a8047763-5465e583-b3e236d1"),
		data={"from": "Mako <mailgun@sandbox107d37aac3a94f43bca9d0e7b0a09769.mailgun.org>",
			"to": email,
			"subject": "Access code for Mako login",
			"text": "Here is your access code to log into Mako. \n Access code: " + accessCode})


# Function to send the token email via Mailgun API
def send_token_mail(token, email):
	return requests.post(
		"https://api.mailgun.net/v3/sandbox107d37aac3a94f43bca9d0e7b0a09769.mailgun.org/messages",
		auth=("api", "b309c1e12d23f8a1c8704a34a8047763-5465e583-b3e236d1"),
		data={"from": "Mako <mailgun@sandbox107d37aac3a94f43bca9d0e7b0a09769.mailgun.org>",
			"to": email,
			"subject": "Token for Mako login",
			"text": "Here is your token to log into Mako. It will be valid for 15 minutes.\n Token: " + token})


# Function to generate a random access code
def createAccessCode(username):
    characterList = string.digits + string.ascii_letters
    accessCode = ""

    for i in range(4):
        accessCode += random.choice(characterList)
    users[username]["accessCode"] = accessCode
    store_json()
    return accessCode


# Function to generate and store a random password for the user specified
def createPassword(username):
    characterList = string.digits + string.ascii_letters
    password = ""

    for i in range(16):
        password += random.choice(characterList)
    hashpassword = hashlib.sha512(password.encode('utf-8')).hexdigest()
    users[username]["password"] = hashpassword
    store_json()
    return password


# Function to create the Token and store it in the json
def createToken():
    randomString = ""
    for i in range(16):
        randomString += random.choice(string.ascii_letters)
    token = hashlib.sha256(str(hash(randomString)).encode('utf-8')).hexdigest()
    users[userAccessing]["token"] = token
    users[userAccessing]["tokenIssued"] = str(datetime.now())
    store_json()
    return token

# Function to check the token validity
def tokenValid(token):
    try:
        global userLogged
        if (users[userAccessing]["token"] == token):
            delta = datetime.now() - datetime.strptime(users[userAccessing]["tokenIssued"], "%Y-%m-%d %H:%M:%S.%f")
            if (delta.total_seconds()/60 < 15):
                userLogged = userAccessing
                return True
        return False
    
    except KeyError:
        return False


# Function to start the program printing out the root password
@app.route("/start")
def start():
    password = createPassword('root')
    return {"text": f"Root password: {password}", "password": password}

# Function to login
@app.route("/login", methods=["POST"])
def login():
    global userAccessing
    # Check if username is listed in the json file
    if request.form.get("username"):
        try:
            users[request.form.get("username")]
            # Update the current user trying to access
            userAccessing = request.form.get("username")

            # Check if the password matches the one stored in the json
            if (request.form.get("password") == users[userAccessing]["password"]):

                # Check if the token matches the one stored in the json
                if (tokenValid(request.form.get("token"))):
                    return {"text": "Token correct, login successful"}
                
                else:
                    # Generate a random access code
                    createAccessCode(userAccessing)
                    # Send access code via email
                    send_access_mail(users[userAccessing]["accessCode"], users[userAccessing]["email"])

                    return {"text": f"Hello {request.form['username']}, an access code has been sent to your email, please insert that to continue. Note that the email could have arrived to your junk mail box", "access": True, "accessCode": users[userAccessing]["accessCode"]}
                
            return {"text": "Access denied, password is not correct"}
        
        except KeyError:
            return {"text": "Access denied, username not found"}
    return {"text": "Access denied, authentication failed"}

# Function to check the access code
@app.route("/login/access_code", methods=["POST"])
def access_code():
    if request.form.get("accessCode"):
        if (request.form.get("accessCode") == users[userAccessing]["accessCode"]):
            #create Token and send email
            token = createToken()
            send_token_mail(token, users[userAccessing]["email"])
            return {"text": "A token has been sent to your email. Note that the email could have arrived to your junk mail box", "token": token}
    return {"text": "Access denied, access code incorrect"}

# Function to check the token
@app.route("/login/token", methods=["POST"])
def token():
    if request.form.get("token"):
        if (tokenValid(request.form.get("token"))):
            return {"text": "Login successful"}
    return {"text": "Access denied, token incorrect or not valid"}


@app.route("/admin_console", methods=["POST"])
def admin_console():
    if (userLogged == request.form.get("username")):
        if (users[userAccessing]["group"] == "admin"):
            # ADD
            if(request.form.get("action")=="addUser"):
                users[request.form.get("addname")] = {"email": request.form.get("email")}
                password = createPassword(request.form.get("addname"))
                # Send password created to the new user
                send_psswd_mail(request.form.get("addname"), password, request.form.get("email"))
                users[request.form.get("addname")]["group"] = "Unclassified"
                store_json()
                return f"User {request.form.get('addname')} created"
            # MODIFY
            elif(request.form.get("action")=="modifyUser"):
                users[request.form.get("changeUser")]["group"] = request.form.get("group")
                store_json()
                return f"User {request.form.get('changeUser')} changed to group {request.form.get('group')}"
            # DELETE
            elif(request.form.get("action")=="deleteUser"):
                del users[request.form.get("delUser")]
                store_json()
                return f"User {request.form.get('delUser')} deleted"
            else:
                return "No service requested"
    return "You don't have the rights for this service"


@app.route("/audit_expenses", methods=["POST"])
def audit_expenses():
    # Can be read by everybody
    if (userLogged == request.form.get("username")):
        if os.path.exists("data/expenses.txt"):
            with open("data/expenses.txt", 'r') as f:
                return f.read()
        return "No expenses yet"
    return "You don't have the rights for this service"


@app.route("/add_expense", methods=["POST"])
def add_expense():
    # Can be written only by Top Secret or Admin
    if (userLogged == request.form.get("username")):
        if(users[userAccessing]["group"]=="admin" or users[userAccessing]["group"] == "Top secret"):
            if request.form.get("expense"):
                with open("data/expenses.txt", 'a') as f:
                    f.write(request.form.get("expense") + " ")
                return "Expense added"
            return "No expense was given"
        else:
            return "You don't have the rights for this service"
    else:
        return "You don't have the rights for this service"


@app.route("/audit_timesheets", methods=["POST"])
def audit_timesheets():
    # Can be read by everybody
    if (userLogged == request.form.get("username")):
        if os.path.exists("data/timesheets.txt"):
            with open("data/timesheets.txt", 'r') as f:
                return f.read()
        return "No timesheets yet"
    else:
        return "You don't have the rights for this service"


@app.route("/submit_timesheet", methods=["POST"])
def submit_timesheet():
    # Can be written only by Top Secret or Admin
    if (userLogged == request.form.get("username")):
        if(users[userAccessing]["group"]=="admin" or users[userAccessing]["group"] == "Top secret"):
            if request.form.get("timesheet"):
                with open("data/timesheets.txt", 'a') as f:
                    f.write(request.form.get("timesheet") + " ")
                return "Timesheet added"
            return "No timesheet was given"
        else:
            return "You don't have the rights for this service"
    else:
        return "You don't have the rights for this service"


@app.route("/view_meeting_minutes", methods=["POST"])
def view_meeting_minutes():
    # Top secret subjects can't read this
    if (userLogged == request.form.get("username")):
        if(users[userAccessing]["group"]=="Secret" or users[userAccessing]["group"]=="Unclassified"):
            if os.path.exists("data/meeting_minutes.txt"):
                with open("data/meeting_minutes.txt", 'r') as f:
                    return f.read()
            return "No meeting minutes yet"
        else:
            return "You don't have the rights for this service"
    else:
            return "You don't have the rights for this service"


@app.route("/add_meeting_minutes", methods=["POST"])
def add_meeting_minutes():
    # Unclassified subjects can't write this
    if (userLogged == request.form.get("username")):
        if(users[userAccessing]["group"]!="Unclassified"):
            if request.form.get("meetingMinutes"):
                with open("data/meeting_minutes.txt", 'a') as f:
                    f.write(request.form.get("meetingMinutes") + " ")
                return "Meeting minutes added"
            return "No meeting minutes given"
        else:
            return "You don't have the rights for this service"
    else:
            return "You don't have the rights for this service"


@app.route("/view_roster", methods=["POST"])
def view_roster():
    # Only Unclassified subjects can read this
    if (userLogged == request.form.get("username")):
        if(users[userAccessing]["group"] =="Unclassified"):
            if os.path.exists("data/roster.txt"):
                with open("data/roster.txt", 'r') as f:
                    return f.read()
            return "No roster yet"
        else:
            return "You don't have the rights for this service"
    else:
            return "You don't have the rights for this service"


@app.route("/roster_shift", methods=["POST"])
def roster_shift():
    # Can be written by everybody
    if (userLogged == request.form.get("username")):
        if request.form.get("roster"):
            with open("data/roster.txt", 'a') as f:
                f.write(request.form.get("roster"))
            return "Shift rostered"
        return "No shift given"
    else:
            return "You don't have the rights for this service"


if __name__ == "__main__":
    os.makedirs("data/", exist_ok=True)
    app.run(host="127.0.0.1", port="2250")