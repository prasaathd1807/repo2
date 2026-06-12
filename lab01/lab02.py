import json
from netmiko import ConnectHandler

with open("inventory.json") as file:
    inventory = json.load(file)

    routerlist = inventory["R1"]

    routerlist["username"] = "admin"
    routerlist["password"] = "Password123"

    conn = ConnectHandler(**routerlist)

    output = conn.send_command("show ip interface brief")

    print(output)

    conn.disconnect()