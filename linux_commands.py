import os

def ls():
    print("[+] EXEC: LS \n")
    os.system("echo Currently at $PWD directory: && ls -la")
def clr():
    os.system("clear")
def ip_conf():
    print("[+] EXEC: IPCONFIG \n")
    os.system("ifconfig")
def pc_info():
    if os.system("which neofetch") != 0:
        os.system("sudo apt-get install -y && neofetch")
    else:
        print("[+] EXEC: \n")
        os.system("neofetch")