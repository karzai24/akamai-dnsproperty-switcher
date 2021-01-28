#!/usr/bin/env
###################################################################################################
# Version: 1.0                                                                                    #
# Date: January 2, 2021                                                                           #
# Author: Mohammad Karzai (karzai24.mk@gmail.com)                                                 #
# # Usage: python main.py sitename pull_site/add_site                                             #
# # Example: python main.py Boston pull_site                                                      #
# # 1. Get list of properties from Akamai                                                         #
# # 2. Get config for each property and return json object                                        #
# # 3. Read the json and append the field we would like to change. By DataCenter ID               #
# # 4. Send appended json to Akamai via PUT                                                       #
###################################################################################################
import requests
import logging
import json
import sys
from akamai.edgegrid import EdgeGridAuth

########################################
# Add your Akamai API Keys here:       #
########################################
my_client_token = 'removed'
my_client_secret = 'removed'
my_access_token = 'removed'

########################################
# Add your domain information here:    #
########################################
base_url = "removed"
domain = "removed"
base_api = "config-gtm/v1/domains/"

########################################
# Variables                            #
########################################
my_Auth = EdgeGridAuth(client_token=my_client_token, client_secret=my_client_secret, access_token=my_access_token)
enabled = True
disabled = False
headers = {'Content-Type': 'application/json'}

########################################
# Cli Arguments                        #
########################################
site_name = sys.argv[1]
my_action = sys.argv[2]

## Get the DataCenter ID from datacenter and fill here.
def switch_sites(site):
    switcher = {
        "London": 1111,
        "Boise": 2222,
        "Boston": 3333,
        "Oregon": 4444
    }
    return switcher.get(site, "Invalid DataCenter Name")


def getPropertiesList():
    reqURL = base_url + base_api + domain + "properties"
    s = requests.Session()
    s.auth = my_Auth
    r = s.get(reqURL)
    response_content = json.loads(r.content)
    logging.info(r.headers)
    my_prop_list = []
    for item in response_content["items"]:
        if item["name"] != "NULL":
            prop_name = item["name"]
            my_prop_list.append(prop_name)
    return my_prop_list


def saveAkaInfo2Json():
    my_json_list = []
    my_props = getPropertiesList()
    for prop in my_props:
        reqURL = base_url + base_api + domain + "properties/" + prop
        s = requests.Session()
        s.auth = my_Auth
        r = s.get(reqURL)
        my_json_list.append(r.content)
        logging.info(r.headers)
    return my_json_list


def updateAkaJson():
    most_recent_config = saveAkaInfo2Json()
    for json_properties in most_recent_config:
        prop = json.loads(json_properties)
        my_endpoint = prop["name"]
        for target in prop["trafficTargets"]:
            if my_action == "pull_site" and target["datacenterId"] == switch_sites(site_name):
                target["enabled"] = disabled
            elif my_action == "add_site" and target["datacenterId"] == switch_sites(site_name):
                target["enabled"] = enabled
        reqURL = base_url + base_api + domain + "properties/" + my_endpoint
        s = requests.Session()
        s.auth = my_Auth
        r = s.put(reqURL, data=json.dumps(prop), headers=headers)
        logging.info(r.headers)
        

if __name__ == '__main__':
    logging.basicConfig(filename='my-dns.log', filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', level=10)
    updateAkaJson()
