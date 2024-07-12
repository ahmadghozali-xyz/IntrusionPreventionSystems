import re
import os
from datetime import datetime
from pytz import timezone

def block_ip(ip):
    command = f"netsh advfirewall firewall add rule name=\"Block {ip}\" dir=in action=block remoteip={ip}"
    os.system(command)
    print(f"IP {ip} telah diblokir.")
    log_blocked_ip(ip)

def read_and_block_ips_from_file(log_filename):
    try:
        with open(log_filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File {log_filename} tidak ditemukan.")
        return
    
    for line in lines:
        ip = extract_ip(line)
        if ip:
            if is_bad_ip(ip):
                block_ip(ip)
            else:
                print(f"IP {ip} tidak mencurigakan.")
        else:
            print("Format IP tidak valid dalam log.")

def extract_ip(line):
    match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
    if match:
        return match.group(1)
    return None

def is_bad_ip(ip):
    # Check if IP is in the range 190.0.0.0 to 199.255.255.255 (mencurigakan)
    parts = ip.split('.')
    first_octet = int(parts[0])
    if 190 <= first_octet <= 199:
        return False
    return True

def log_blocked_ip(ip):
    result_txt = 'result.txt'
    current_time = datetime.now(timezone('Asia/Jakarta')).strftime('%d-%m-%Y %H:%M:%S')
    with open(result_txt, 'a') as file:
        file.write(f"{current_time} IP {ip} telah diblokir oleh IPS.\n")

def main():
    log_filename = 'log.txt'  # Ganti dengan nama file log yang sesuai
    read_and_block_ips_from_file(log_filename)
    print("Daftar IP yang mencurigakan dan telah diblokir telah dicatat dalam file result.txt.")

if __name__ == "__main__":
    main()
