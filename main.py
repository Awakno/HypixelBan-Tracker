import requests
import time
from colorama import Fore, init

init(autoreset=True)

API_KEY = ""
WEBHOOK_URL = ""
r = requests.get("https://api.hypixel.net/v2/punishmentstats",headers={"API-Key":API_KEY})
if r.status_code != 200:
    print(f"{Fore.RED}[ERROR] {Fore.WHITE}Failed to get data from Hypixel API. Status Code: {r.status_code}")
    exit()
TOTAL_WATCHDOG_BANS = r.json()['watchdog_total']
TOTAL_STAFF_BANS = r.json()['staff_total']

print(f"{Fore.GREEN}[INFO] {Fore.WHITE}Starting Hypixel Watchdog Tracker...")

while True:
    r = requests.get("https://api.hypixel.net/v2/punishmentstats",headers={"API-Key":API_KEY})
    if r.status_code != 200:
        print(f"{Fore.RED}[ERROR] {Fore.WHITE}Failed to get data from Hypixel API. Status Code: {r.status_code}")
        time.sleep(5)
        continue
    if r.status_code == 200:
        data = r.json()
        watchdog_bans = data['watchdog_total']
        staff_bans = data['staff_total']
        if watchdog_bans > TOTAL_WATCHDOG_BANS:
            #print(f"New Watchdog Ban! Total: {watchdog_bans - TOTAL_WATCHDOG_BANS}")
            r = requests.post(WEBHOOK_URL,json={"content":f"🐶 Bans: {watchdog_bans - TOTAL_WATCHDOG_BANS} <t:{int(time.time())}:R>","username": "Hypixel Watchdog Tracker","avatar_url":"https://logos-world.net/wp-content/uploads/2023/12/Hypixel-Emblem.png"})
            TOTAL_WATCHDOG_BANS = watchdog_bans
        if staff_bans > TOTAL_STAFF_BANS:
            #print(f"New Staff Ban! Total: {staff_bans - TOTAL_STAFF_BANS}")
            r = requests.post(WEBHOOK_URL,json={"content":f"👮 Bans: {staff_bans - TOTAL_STAFF_BANS} <t:{int(time.time())}:R>","username": "Hypixel Watchdog Tracker","avatar_url":"https://logos-world.net/wp-content/uploads/2023/12/Hypixel-Emblem.png"})
            TOTAL_STAFF_BANS = staff_bans
        
    time.sleep(5)
    