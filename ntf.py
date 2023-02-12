# -*- coding: utf-8 -*-
import readline
import sys
import atexit
import subprocess
import os
import requests
import socket
import colorama
from linux_commands import ls, clr, ip_conf, pc_info
from bs4 import BeautifulSoup
from tabulate import tabulate

"""---------TAP-SUPPORT---------"""
readline.parse_and_bind('tab: complete')

"""---------HISTORY-SUPPORT---------"""
histfile = ".history"
try:
    readline.read_history_file(histfile)
except FileNotFoundError:
    pass
atexit.register(readline.write_history_file, histfile)


"""---------ROOT---------"""
if os.geteuid() != 0:
    print(colorama.Fore.RED + " You need root privileges! " + colorama.Fore.RESET)
    exit(1)

"""---------MAC---------"""
def change_mac():
    interface = input("Enter the name of the network interface you want to change the MAC address for: ")
    os.system(f"macchanger -r {interface}")
    print(f"Changed MAC address for {interface}.")

"""---------TOR-OFF---------"""
def turn_off_tor():
    status = os.popen("systemctl is-active tor").read().strip()
    if status == "active": 
        os.system("systemctl stop tor")
        print("Tor service" + colorama.Fore.RED + " killed." + colorama.Fore.RESET)
    else:
        os.system("rm -rf .history && echo Logs and other stuff cleared!")
atexit.register(turn_off_tor)

"""---------TOR---------"""
def tor():
    os.system("systemctl start tor")

"""---------SCAP---------"""
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

"""---------WHOIS---------"""
def whois(domain):
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
            print(f"Results for {domain}:")
            print("------------------")
            print("\n".join(lines[start:end+1]))
        except requests.exceptions.RequestException as e:
            print("An error occurred while retrieving whois information")
    else:
        cmd = "whois " + domain
        try:
            print(subprocess.check_output(cmd, shell=True).decode())
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                print("This TLD has no whois server")
            else:
                raise

"""---------PING---------"""
def ping(domain):
    if domain == "back":
        menu()
    cmd = "ping -c 3 " + domain
    try:
        result = subprocess.check_output(cmd, shell=True).decode()
        if "Unreachable" in result:
            return f"The {domain} ({socket.gethostbyname(domain)}) is unreachable"
        else:
            return f"3 ping sent to {domain} ({socket.gethostbyname(domain)})"
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return "The host might be deivown"
        else:
            if e.returncode == 2:
                return "An error occurred while trying to ping the domain"
            else:
                raise

"""---------MENU---------"""
def menu():
    colorama.init()
    output = subprocess.check_output(["ifconfig | grep 'inet.*192' | awk '{print $2}'"], shell=True).decode("utf-8")
    local_ip = output.strip().split("\n")[0]
    prompt = f"{colorama.Fore.RED}{socket.gethostname()}{colorama.Fore.RESET}@{colorama.Fore.GREEN}{local_ip}{colorama.Fore.RESET} > "
    while True:
        command = input(prompt)
        if command == "whois" or command == "WHOIS":
            if len(command.split()) > 1:
                domain = command.split()[1]
                result = whois(domain)
                print(result)
            else:
                domain = input("Enter a domain to whois: " + colorama.Fore.RED )
                colorama.Fore.RESET
                result = whois(domain)
                print(result)
        elif command == "scap" or command == "SCAP":
            scap()
        elif command == "tor" or command == "TOR":
            tor()
        elif command == "mac" or command == "MAC":
            change_mac()  
        #---------PING---------#
        elif command == "ping" or command == "PING":
            if len(command.split()) > 1:
                domain = command.split()[1]
                result = ping(domain)
                print(result)
            else:
                domain = input("Enter a domain to ping: " + colorama.Fore.RED)
                colorama.Fore.RESET
                result = ping(domain)
                print(result)
        #---------IP---------#
        elif command == "publip" or command == "PUBLIP":
            try:
                result = subprocess.check_output("curl -s icanhazip.com", shell=True).decode().strip()
                print("Your public IP is: " + colorama.Fore.YELLOW + result + colorama.Fore.RESET)
            except subprocess.CalledProcessError as e:
                print("An error occurred while retrieving your public IP")
        #---------DEVICES---------#
        elif command == "devices" or command == "DEVICES":
            try:
                result = subprocess.check_output('arp-scan -l | grep -v "Starting" | grep -v "Interface" | grep -v "packets" | grep -v "received" | grep -v "Ending"', shell=True).decode().strip()
                print("Devices connected to the same network:\n")
                print(result + "\n")
            except subprocess.CalledProcessError as e:
                print("An error occurred while scanning the network for connected devices")
        #---------MENU-HELP---------#
        elif command == "help" or command == "HELP" or command == "?":
            print("")
            print("|=====================================================|")
            print("\tCommand".ljust(20),"Description")
            print("|=====================================================|")
            print(" WHOIS [domain]".ljust(20),"| Check domain information")
            print("|-----------------------------------------------------|")
            print(" PING [domain]".ljust(20),"| Test connection to a domain")
            print("|-----------------------------------------------------|")
            print(" PUBLIP".ljust(20),"| Show public IP address")
            print("|-----------------------------------------------------|")
            print(" DEVICES".ljust(20),"| Show connected network devices")
            print("|-----------------------------------------------------|")
            print(" SCAP".ljust(20),"| Scan for open ports in network")
            print("|-----------------------------------------------------|")
            print(" TOR".ljust(20),"| Start tor services")
            print("|-----------------------------------------------------|")
            print(" MAC".ljust(20),"| Change Mac Address")
            print("|-----------------------------------------------------|")
            print(" INFO".ljust(20),"| System info")
            print("|=====================================================|")
            print("".ljust(15),"Linux Command")
            print("|=====================================================|")
            print(" CLEAR".ljust(20),"| Clear terminal")
            print("|-----------------------------------------------------|")
            print(" LS".ljust(20),"| List current director")
            print("|-----------------------------------------------------|")
            print(" IFCONFIG".ljust(20),"| List ip configuration")
            print("|=====================================================|")
            print(" BACK".ljust(20),"| Go back to previous menu")
            print("|-----------------------------------------------------|")
            print(" EXIT".ljust(20),"| Exit program")
            print("|=====================================================|")
            print("")
        #---------LINUX-COMMANDS---------#
        elif command == "clear" or command == "CLEAR":
            clr()
        elif command == "ifconfig" or command == "IFCONFIG":
            ip_conf()
        elif command == "info" or command == "INFO":
            pc_info()
        elif command == "ls" or command == "LS":
            ls()
        #---------EXIT---------#
        elif command == "banner" or command == "BANNER":                                                                                                                                                                                                                                                                                                
            banner()
        elif command == "exit" or command == "quit":
            clr()
            os.system("echo OBSERVER YOUR SECURITY!")
            break
        elif command == "back" or command == "BACK":
            print("You are already in the menu.")
        elif command == "":
            print("Command not typed")
        else:
            print("Invalid command")

#---------BANNER---------#
os.system("clear")
def banner():
    print(colorama.Fore.YELLOW)
    os.system("figlet 'Network Testing Framework' -c -f small | sed 's/\[31m/\\\033\\\[31;1m/g'")
    print(colorama.Fore.RESET)
banner()
print("Welcome to Network Testing Framework" + " by " + colorama.Fore.BLUE + "@cyberdome.tj" + colorama.Fore.RESET)
print("Type 'help' or '?' to see the list of commands")

menu()
