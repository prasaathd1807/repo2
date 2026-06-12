import json

with open("device.json") as f:
    inventory = json.load(f)

device_name = input("Enter device name (R1/R2)")
device = inventory[device_name]

print(f"Hostname : {device_name}")
print(f"IP       : {device['ip']}")
print(f"Vendor   : {device['vendor']}")
print(f"Type     : {device['type']}")
print(f"Model    : {device['model']}")