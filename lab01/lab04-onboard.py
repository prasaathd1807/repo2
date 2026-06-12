import json
import os

from netmiko import ConnectHandler

# Create folders if not exist

os.makedirs("proofs", exist_ok=True)
os.makedirs("backups", exist_ok=True)

USERNAME = os.getenv("NET_USERNAME")
PASSWORD = os.getenv("NET_PASSWORD")

with open("inventory2.json") as f:
    inventory = json.load(f)

for hostname, router in inventory["routers"].items():

    print(f"\nConnecting to {hostname}")

    try:

        router["username"] = USERNAME
        router["password"] = PASSWORD

        conn = ConnectHandler(**router)

        # Onboarding Configuration

        ip_map = {
            "R1": "10.10.10.1",
            "R2": "10.10.10.2",
            "R3": "10.10.10.3"
        }

        config_commands = [

            "interface loopback10",
            f"ip address {ip_map[hostname]} 255.255.255.0",
            "description Created_By_Python",

            "banner motd #Authorized Access Only#",

            "no ip domain-lookup",

            "ip domain-name corp.local",

            "service password-encryption",

            "line console 0",
            "logging synchronous"
        ]

        output = conn.send_config_set(config_commands)

        print(output)

        conn.save_config()

        # -------------------------
        # Validation Commands
        # -------------------------

        validation = ""

        validation += "\n===== SHOW IP INTERFACE BRIEF =====\n"
        validation += conn.send_command(
            "show ip interface brief"
        )

        validation += "\n\n===== SHOW BANNER =====\n"
        validation += conn.send_command(
            "show running-config | section banner"
        )

        validation += "\n\n===== SHOW LOOPBACK =====\n"
        validation += conn.send_command(
            "show running-config interface loopback10"
        )

        # Save proof file

        proof_file = f"proofs/{hostname}_validation.txt"

        with open(proof_file, "w") as file:
            file.write(validation)

        print(f"Validation saved -> {proof_file}")

        # -------------------------
        # Full Backup
        # -------------------------

        running_config = conn.send_command(
            "show running-config"
        )

        backup_file = f"backups/{hostname}.cfg"

        with open(backup_file, "w") as file:
            file.write(running_config)

        print(f"Backup saved -> {backup_file}")

        conn.disconnect()

    except Exception as e:

        print(f"Failed on {hostname}")
        print(e)