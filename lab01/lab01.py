from netmiko import ConnectHandler
router = {"device_type": "cisco_ios", "host": "192.168.10.1", "username": "admin", "password": "Password123"}

conn = ConnectHandler(**router)

output = conn.send_command("show ip int br")

print(output)

conn.disconnect()