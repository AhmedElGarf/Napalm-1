import json
import urllib3
import pprint
import pandas as pd
import getpass
import sys
import pyfiglet
from napalm import get_network_driver

urllib3.disable_warnings()


ascii_banner = pyfiglet.figlet_format("NAPALM")
print(ascii_banner)


unwanted_params = {"interface_list"}
def formatter(list, unwanted):
    return [{x: list[x] for x in list if x not in unwanted}]


user = input("-   Please enter your login user \n")
password = getpass.getpass(prompt=' >> Please Enter Your Login Password ', stream=None)
with open('ips.txt') as f:
    IPs = f.read().splitlines()
    for IP in IPs:
        try:


        ## Openeing Connection to switch using NAPALM
            print("-   Connecting to switch " + IP + "..." )
            driver = get_network_driver('ios')
            sw = driver(IP, user, password)
            sw.open()


        ## NAPALM command to get some known values (Hostname , OS , Model , Interfaces , Uptime)
            ios_output = sw.get_facts()
            
            
        
            
        ## Converting the NAPALM output to JSON format to be easily exporeted to Excel with good format
            jsonOUT = (json.dumps(ios_output, indent=4))
            
            
            json2 = json.loads(jsonOUT)
            json2['Device IP'] = IP

            
        ## Using the unwanted parameters to remove Interfaces element from JSON file and make a new file
            json_after_formatting = formatter(json2, unwanted_params)
            
            
        ## Parsing the vaules into Excel sheet using Pandas 
            df = pd.DataFrame(json_after_formatting)
            df.to_csv('inventory.csv' ,mode='a', index=False , header=None)
            
            print("-   Data collected sucessfuly\n")
        except:
                print("-   Device is not reachable\n")
