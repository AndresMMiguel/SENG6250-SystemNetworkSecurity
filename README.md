## Running the programs

First we need to start the server with the following:

```sh
python3 server.py
```

It will say that is running on http://127.0.0.1:2250, which means you are ready to start the client:

```sh
python3 clientManualInput.py
```
Will let you write the input for the username and password, as well as the multifactor authentication in case you want to try it by yourself.

```sh
python3 clientAdminAccessingServices.py
```
It will login automatically so you don't have to worry about receiving your access code and token. Once logged in as a user in the group 'Admin', it will try to execute every service in the server.

```sh
python3 clientTopSecretAccessingServices.py
```
It will also do the automatic login as a user in the group 'Top Secret' and then try to access every services.

```sh
python3 clientSecretAccessingServices.py
```
It will do the automatic login as a user in the group 'Secret' and then try to access every services.

```sh
python3 clientUnclassifiedAccessingServices.py
```
It will do the automatic login as a user in the group 'Unclassified' and then try to access every services.

```sh
python3 clientUnloggedAccessingServices.py
```
It will try to access every services without login.