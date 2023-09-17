# domaintracker.py
The script will create a dictionary list from the domain you provided and save it into a file. Then we will use that
file to read each line to check if a domain (that kind of looks like your domain) has a resolvable address. We will use nslookup
to check for resolvable ip and if there is an mx record related to it. We will then run whois to identify the registrar url,
creation data, and expiry date.
You don't want others to impersonate your domain for any malicious purposes.

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
  
