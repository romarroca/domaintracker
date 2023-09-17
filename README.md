# domaintracker.py
The script will generate a list of domain variations based on the domain you provide and save it to a file. We will then read each line from this file to check whether any domains resembling yours have resolvable IP addresses. To do this, we'll use nslookup to identify resolvable IPs and associated MX records. Following this, we'll run a WHOIS query to find out details such as the registrar URL, creation date, and expiry date of the domain. The script enables you to monitor for potential domain impersonation and report any abuse for timely intervention.

## Usage
- pip install -r requirements.txt
- python domain-tracker.py
  This will ask for domain input, option for creating the domain list and  number of threads you want(This will depend on your available resources so choose wisely)
  - ![image](https://github.com/romarroca/domaintracker/assets/87074019/2a4c3449-72bf-4cf4-8d77-95baa74f1c27)
- Ctrl c if you want to exit.
- ![image](https://github.com/romarroca/domaintracker/assets/87074019/93cbc0bf-8c4c-4c72-b8f9-15cf62a58fcb)

## Output
- This will create the {keyword}_generated_domains.txt where keyword is the user input
- This will create the {keyword}_identified_domains.csv where keyword is the user input
  ![image](https://github.com/romarroca/domaintracker/assets/87074019/4c5d2e2f-d293-4dd8-8c2e-30580b7c3531)

### You can modify the create_domainlist.py to your liking. Feel free to edit also the TLD text file depending on your usage.
  
