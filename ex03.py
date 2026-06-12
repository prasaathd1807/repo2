inventory = {
    "R1":{
        "type": "router-cat1", "model": "3660"
    },
    "R2":{
        "type": "router-cat2", "model": "7200"
    }
}

for hostname, details in inventory.items():
    print(f"Hostname    : {hostname}")
    print(f"Type        : {details['type']}")
    print(f"Model       : {details['model']}")