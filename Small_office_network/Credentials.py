
#Credentials:

from getpass import getpass
from rich import print as rprint

username =   input("Username: ")
password = getpass("password: ")
secret   = getpass("secret: ")

while True:
    if username == "Automation" and password == "cisco123" and secret == "cisco123":
        break
    else:
        rprint("[bold red]invalid Username or Password![/bold red]")
        username =   input("Username: ")
        password = getpass("password: ")
        secret   = getpass("secret: ")
