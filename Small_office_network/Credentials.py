
#Credentials:

from getpass import getpass

username =   input("Username: ")
password = getpass("password: ")
secret   = getpass("secret: ")

while True:
    if username == "Automation" and password == "cisco123" and secret == "cisco123":
        break
    else:
        print("invalid Username or Password!")
        username =   input("Username: ")
        password = getpass("password: ")
        secret   = getpass("secret: ")
