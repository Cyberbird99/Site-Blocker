import time
from datetime import datetime
import os

# List of sites to block
sites_to_block = [
    "www.example.com",
    "www.example2.com",
    "www.example3.com",
]

# Paths to the hosts file for different operating systems
HOSTS_LINUX = "/etc/hosts"
HOSTS_WINDOWS = r"C:\Windows\System32\drivers\etc\hosts"

# Determine the appropriate hosts file path based on the OS
if os.name == 'posix':
    hosts_path = HOSTS_LINUX
elif os.name == 'nt':
    hosts_path = HOSTS_WINDOWS
else:
    print("Unknown OS")
    exit()

REDIRECT_IP = "127.0.0.1"

def block_sites(start_hour, end_hour):
    while True:
        current_time = datetime.now()
        start_time = datetime(current_time.year, current_time.month, current_time.day, start_hour)
        end_time = datetime(current_time.year, current_time.month, current_time.day, end_hour)
        
        try:
            if start_time <= current_time <= end_time:
                with open(hosts_path, "r+") as hostfile:
                    lines = hostfile.readlines()
                    hostfile.seek(0)
                    hosts_set = set(line.strip().split()[1] for line in lines if len(line.strip().split()) > 1)
                    
                    # Add new blocks if not already present
                    for site in sites_to_block:
                        if site not in hosts_set:
                            hostfile.write(f"{REDIRECT_IP} {site}\n")
                    
                    # Truncate the file to remove any extra lines if necessary
                    hostfile.truncate()
            else:
                with open(hosts_path, "r+") as hostfile:
                    lines = hostfile.readlines()
                    hostfile.seek(0)
                    # Write back all lines that do not include the sites to be blocked
                    for line in lines:
                        if not any(site in line for site in sites_to_block):
                            hostfile.write(line)
                    hostfile.truncate()
                    
            time.sleep(4)
        
        except PermissionError as e:
            print(f"PermissionError: {e}")
            break

if __name__ == "__main__":
    block_sites(8, 18)