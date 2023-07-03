#Credentials:

import getpass

username = input("Username: ")
password = getpass.getpass("Password: ")
secret   = getpass.getpass("secret: ")

while True:
    if username == "Automation" and password == "cisco123" and secret == "cisco123":
        break
    else:
        print("Login unsuccessful! Username or password incorrect!")
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        secret   = getpass.getpass("secret: ")
      
    