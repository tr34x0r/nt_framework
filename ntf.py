import sys
import atexit
import subprocess
import os
import requests
import socket
from bs4 import BeautifulSoup
import colorama

def change_mac():
    interface = input("Enter the name of the network interface you want to change the MAC address for: ")
    os.system(f"macchanger -r {interface}")
    print(f"Changed MAC address for {interface}.")

def turn_off_tor():
    status = os.popen("systemctl is-active tor").read().strip()
    if status == "active":
        os.system("systemctl stop tor")
        print("Tor service" + colorama.Fore.RED + " killed." + colorama.Fore.RESET)
    else:
        print("Tor is already off.")

atexit.register(turn_off_tor)

if os.geteuid() != 0:
    print(colorama.Fore.RED + "This script must be run as root." + colorama.Fore.RESET)
    exit(1)

def tor():
    os.system("systemctl start tor")


def scap():
    arp_scan = os.popen("arp-scan -l").read()
    ip_addresses = arp_scan.split("\n")[2:-3]
    open_ports = []
    
    for ip in ip_addresses:
        ip = ip.split("\t")[0]
        for port in [21, 22, 23, 25, 80, 443, 139, 445, 8080, 8888, 81]:
            response = os.system(f"nc -z -w 1 {ip} {port} 2>/dev/null")
            if response == 0:
                open_ports.append((ip, port))
                print("{} has port {} open".format(colorama.Fore.YELLOW + ip + colorama.Fore.RESET, colorama.Fore.RED + str(port) + colorama.Fore.RESET))
   
                


def whois(domain):
    if domain == "back":
        menu()
    if domain.endswith(".tj"):
        domain = domain.replace(".tj", "")
        try:
            response = requests.get(f"http://www.nic.tj/cgi/whois2?domain={domain}")
            soup = BeautifulSoup(response.text, 'html.parser')
            result = soup.get_text()
            lines = result.split("\n")
            for i, line in enumerate(lines):
                if "domain name" in line.lower():
                    start = i
                if "registration date" in line.lower():
                    end = i
                    break
            return "\n\n" + "\n".join(lines[start:end+1]) + "\n"
        except requests.exceptions.RequestException as e:
            return "An error occurred while retrieving whois information"
    else:
        cmd = "whois " + domain
        try:
            return subprocess.check_output(cmd, shell=True).decode()
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                return "This TLD has no whois server"
            else:
                raise


def ping(domain):
    if domain == "back":
        menu()
    cmd = "ping -c 1 " + domain
    try:
        result = subprocess.check_output(cmd, shell=True).decode()
        if "Unreachable" in result:
            return f"The {domain} ({socket.gethostbyname(domain)}) is unreachable"
        else:
            return f"1 ping sent to {domain} ({socket.gethostbyname(domain)})"
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return "The host might be down"
        else:
            if e.returncode == 2:
                return "An error occurred while trying to ping the domain"
            else:
                raise



def menu():
    colorama.init()
    output = subprocess.check_output(["ifconfig | grep 'inet.*192' | awk '{print $2}'"], shell=True).decode("utf-8")
    local_ip = output.strip().split("\n")[0]
    prompt = f"{colorama.Fore.RED}{socket.gethostname()}{colorama.Fore.RESET}@{colorama.Fore.GREEN}{local_ip}{colorama.Fore.RESET} > "
    while True:
        command = input(prompt)
        if command.startswith("whois"):
            if len(command.split()) > 1:
                domain = command.split()[1]
                result = whois(domain)
                print(result)
            else:
                domain = input("Enter a domain to whois: " + colorama.Fore.RED )
                colorama.Fore.RESET
                result = whois(domain)
                print(result)
        
        elif command == "scap":
            scap()

        elif command == "tor":
            tor()
        
        elif command == "mac":
            change_mac()    
                
        elif command.startswith("ping"):
            if len(command.split()) > 1:
                domain = command.split()[1]
                result = ping(domain)
                print(result)
            else:
                domain = input("Enter a domain to ping: " + colorama.Fore.RED)
                colorama.Fore.RESET
                result = ping(domain)
                print(result)
        elif command == "show":
            try:
                result = subprocess.check_output("curl -s icanhazip.com", shell=True).decode().strip()
                print("Your public IP is: " + colorama.Fore.YELLOW + result + colorama.Fore.RESET)
            except subprocess.CalledProcessError as e:
                print("An error occurred while retrieving your public IP")
        elif command == "devices":
            try:
                result = subprocess.check_output('arp-scan -l | grep -v "Starting" | grep -v "Interface" | grep -v "packets" | grep -v "received" | grep -v "Ending"', shell=True).decode().strip()
                print("Devices connected to the same network:\n")
                print(result + "\n")
            except subprocess.CalledProcessError as e:
                print("An error occurred while scanning the network for connected devices")
         
          
        elif command == "exit":
            break
        elif command == "help":
            print("Available commands:")
            print("whois [domain]")
            print("ping [domain]")
            print("show - Show my public ip")
            print("devices - Show devices that are connected to the same network)")
            print("scap - Scan for most vulnerable open ports in the network")
            print("tor - Start tor services")
            print("mac - Change your Mac Address")
            print("back")
            print("exit")
        elif command == "back":
            print("You are already in the menu.")
        else:
            print("Invalid command")



os.system("clear")
print(colorama.Fore.YELLOW)
os.system("figlet 'Network Testing Framework' -c -f small | sed 's/\[31m/\\\033\\\[31;1m/g'")
print(colorama.Fore.RESET)
print("Welcome to Network Testing Framework" + colorama.Fore.BLUE + " @cyberdome.tj" + colorama.Fore.RESET)
print("Type 'help' to see the list of commands")

menu()
