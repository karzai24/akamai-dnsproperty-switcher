# akamai-dnsproperty-switcher
Script that will turn on and off entire datacenter from within all properties inside Akamai.
Get your datacenter ID from Akamai and replace entries in switch statement on line 48.
Usage: python main.py sitename pull_site/add_site
Example: python main.py Boston pull_site
1. Get list of properties from Akamai
2. Get config for each property and return json object
3. Read the json and append the field we would like to change. By DataCenter ID
4. Send appended json to Akamai via PUT 
