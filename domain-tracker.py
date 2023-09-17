import certstream
import time
import subprocess
#from email_sender import send_email
from create_domainlist import generate_domain_list
import threading
from tqdm import tqdm
import csv
import subprocess

# Saves the recently match domain to an ip-address.
def save_identified_domain(domain, ip_address, mx_records, registrar_url, creation_date, expiry_date):
    sanitized_registrar_url = registrar_url.replace('\n', ' ').replace('\r', '')  # Replacing newlines with space
    with open(f"{keyword}_identified_domains.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([domain, ip_address, mx_records, sanitized_registrar_url, creation_date, expiry_date])



def load_identified_domains():
    try:
        with open(f"{keyword}_identified_domains.csv", "r") as f:
            reader = csv.reader(f)
            return set(row[0] for row in reader)
    except FileNotFoundError:
        return set()

def get_mx_records(domain):
    try:
        output = subprocess.check_output(f'nslookup -type=mx {domain}', shell=True, stderr=subprocess.STDOUT, text=True)
        lines = output.split("\n")
        mx_records = []
        for line in lines:
            if "MX preference" in line:
                mx_records.append(line.strip())
        return "; ".join(mx_records)
    except subprocess.CalledProcessError as e:
        return "N/A"

def get_whois_info(domain):
    try:
        output = subprocess.check_output(f'whois {domain}', shell=True, stderr=subprocess.STDOUT, text=True)
        lines = output.split("\n")
        registrar_url = creation_date = expiry_date = "N/A"
        for line in lines:
            if "Registrar URL:" in line:
                registrar_url = ":".join(line.split(":")[1:]).strip()
            elif "Creation Date:" in line:
                creation_date = line.split(":")[1].strip()
            elif "Registry Expiry Date:" in line:
                expiry_date = line.split(":")[1].strip()
        return registrar_url, creation_date, expiry_date
    except subprocess.CalledProcessError as e:
        return "N/A", "N/A", "N/A"
    
def print_callback(message, context):
    try:
        if message['message_type'] == "certificate_update":
            domains = message['data']['leaf_cert']['all_domains']
            for domain in domains:
                if f'{keyword}' in domain:
                    print(f"[!] Existing domain detected: {domain}")
                    #send_email(domain)
    except Exception as e:
        print(f"An error occurred: {e}")

from tqdm import tqdm

def monitor_domains_slice(domain_slice):
    dns_servers = ['8.8.8.8', '1.1.1.1', '208.67.222.222', '208.67.220.220']
    identified_domains = load_identified_domains()

    total_domains = len(domain_slice)

    with tqdm(total=total_domains, desc="Monitoring Domains", leave=False) as pbar:
        while True:
            for domain in domain_slice:
                pbar.update(1)

                if domain in identified_domains:
                    continue

                unique_ips = set()
                for dns_server in dns_servers:
                    try:
                        output = subprocess.check_output(f'nslookup -query=A {domain} {dns_server}', shell=True, stderr=subprocess.STDOUT, text=True)
                        lines = output.split("\n")
                        for line in lines:
                            if "Address" in line and not dns_server in line:
                                ip_address = line.split(":")[1].strip()
                                unique_ips.add(ip_address)
                    except subprocess.CalledProcessError as e:
                        output = e.output

                for ip_address in unique_ips:
                    identifier = f"{domain} : {ip_address}"
                    if identifier not in identified_domains:
                        mx_records = get_mx_records(domain)
                        registrar_url, creation_date, expiry_date = get_whois_info(domain)
                        save_identified_domain(domain, ip_address, mx_records, registrar_url, creation_date, expiry_date)
                        identified_domains.add(identifier)
                        pbar.set_postfix_str(f"Domain {domain} exists. IP Address: {ip_address}")

            pbar.n = 0
            pbar.last_print_n = 0
            pbar.refresh()
            time.sleep(3600)



if __name__ == "__main__":

    print("""
        Hey there! The script will create a dictionary list from the domain you provided and save it into a file. Then we will use that
        file to read each line to check if a domain (that kind of looks like your domain) has a resolvable address. We will use nslookup
        to check for resolvable ip and if there is an mx record related to it. We will then run whois to identify the registrar url,
        creation data, and expiry date.
        You don't want others to impersonate your domain for any malicious purposes.
    """)
    
    keyword = input("Enter the domain you want to use for this script: ")
    generate_domain_list(keyword)

    # Initialize CSV file with headers
    with open(f"{keyword}_identified_domains.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['domain', 'ip', 'mx', 'Registrar URL', 'Creation Date', 'Registry Expiry Date'])


    num_threads = int(input("Enter the number of threads you want to use for domain monitoring: "))
    print("The program is running in the background...")

    with open(f'{keyword}_generated_domains.txt', 'r') as f:
        potential_domains = f.read().splitlines()

    slice_size = len(potential_domains) // num_threads
    domain_slices = [potential_domains[i:i + slice_size] for i in range(0, len(potential_domains), slice_size)]

    # certstream_thread = threading.Thread(target=lambda: certstream.listen_for_events(print_callback, url='wss://certstream.calidog.io/'))
    # certstream_thread.daemon = True
    # certstream_thread.start()

    domain_threads = []
    for domain_slice in domain_slices:
        thread = threading.Thread(target=monitor_domains_slice, args=(domain_slice,))
        thread.daemon = True
        thread.start()
        domain_threads.append(thread)

    try:
        while True:  # keep the main thread running
            pass #time.sleep(1)  # sleep for a short time to reduce CPU usage
    except KeyboardInterrupt:  # exit the loop and terminate the program when Ctrl+C is pressed
        print("\nTerminating the program.")

