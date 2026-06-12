import os
import json
from netmiko import ConnectHandler

with open("inventory.json") as f:
    inventory = json.load(f)
print(inventory)

for router in inventory["routers"]:
    print(router)

    try:

        inventory['routers'][router]["username"] = os.getenv("NET_USERNAME")
        inventory['routers'][router]["password"] = os.getenv("NET_PASSWORD")

        print(f"\nConnecting to {inventory['routers'][router]['host']}")

        conn = ConnectHandler(**inventory['routers'][router])

        output = conn.send_command("show ip interface brief")

        print(output)

        conn.disconnect()

    except Exception as e:
        print(f"Failed to connect: {inventory['routers'][router]['host']}")
        print(e)