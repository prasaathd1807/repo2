import json
import os
import csv
from datetime import datetime
from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# Load inventory
with open("inventory.json") as f:
    inventory = json.load(f)

# CSV report file
csv_file = "connection_report.csv"

with open(csv_file, mode="w", newline="") as report:
    writer = csv.writer(report)

    # CSV Header
    writer.writerow([
        "Timestamp",
        "Device",
        "Site",
        "IP Address",
        "Status",
        "Message"
    ])

    for name, router in inventory["routers"].items():
        print(router['site'])
        router["username"] = os.getenv("NET_USERNAME")
        router["password"] = os.getenv("NET_PASSWORD")

        print(f"\n{'=' * 60}")
        print(f"Connecting to {name} ({router['site']})")
        print(f"{'=' * 60}")

        status = "FAILED"
        message = ""

        try:
            conn = ConnectHandler(host=router['host'], device_type=router['device_type'], username=router["username"], password=router["password"])

            output = conn.send_command("show version")

            print(output)

            conn.disconnect()

            status = "SUCCESS"
            message = "Connected and command executed successfully"

        except NetmikoAuthenticationException:
            message = "Authentication Failed"
            print(f"[ERROR] {name}: Authentication Failed")

        except NetmikoTimeoutException:
            message = "Connection Timed Out"
            print(f"[ERROR] {name}: Connection Timed Out")

        except Exception as e:
            message = str(e)
            print(f"[ERROR] {name}: {e}")

        finally:
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                name,
                router["site"],
                router["host"],
                status,
                message
            ])

print(f"\nConnection report saved to: {csv_file}")