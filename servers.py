import json
from pathlib import Path

CONFIG_FILE = Path("servers.json")
STATUS_FILE = Path("status.json")
REQUIRED_FIELDS = ["name", "ip", "role", "cpu_cores", "ram_gb"]

class Server:
    def __init__(self,name,ip,role,cpu_cores,ram_gb):
        self.name=name
        self.ip=ip
        self.role=role
        self.cpu_cores=cpu_cores
        self.ram_gb=ram_gb
        self.status = "stopped"

    def start(self):
        if self.status=='running':
            print(f"Server '{self.name}' is already running.")
        else:
            self.status = "running"
            print(f"{self.name} started.")


    def stop(self):
        if self.status == "stopped":
            print(f"{self.name} is already stopped.")
        else:
            self.status = "stopped"
            print(f"{self.name} stopped.")

    def describe(self):
     return f"{self.name} | {self.ip} | {self.role} | {self.cpu_cores} CPU | {self.ram_gb} GB | {self.status}"

    def dict(self):
        return{"name":self.name,"ip":self.ip,"role":self.role,"cpu_cores":self.cpu_cores,"ram_gb":self.ram_gb,"status":self.status}


def load_servers(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Config file not found: {path}")
        return []
    except json.JSONDecodeError as error:
        print(f"Invalid JSON: {error}")
        return []

    servers = []
    for item in data:
        missing = []
        for field in REQUIRED_FIELDS:
            if field not in item:
                missing.append(field)

        if missing:
            print(f"Skipped invalid server, missing: {', '.join(missing)}")
            continue
        server= Server(item["name"], item["ip"], item["role"], item["cpu_cores"], item["ram_gb"])
        servers.append(server) 
    return servers

def show_servers(servers):
    for server in servers:
        print(server.describe())

def save_status(servers, path):
    data=[]
    for i in servers:
        data.append(i.dict())

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file)


def main():
    servers = load_servers(CONFIG_FILE)
    if not servers:
        return

    print(f"Loaded {len(servers)} servers.")
    print("\n--- Servers ---")
    show_servers(servers)

    web1 = servers[0]
    db1 = servers[1]

    web1.start()
    db1.start()
    web1.start()
    db1.stop()

    print("\n--- After changes ---")
    show_servers(servers)
    save_status(servers, STATUS_FILE)


if __name__ == "__main__":
    main()
