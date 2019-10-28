#!/usr/bin/python3

import os
import socket
import requests
import json

key = "[KEY]"
secret = "[SECRET]"
domain = "[DOMAIN]"

base_url = "https://api.godaddy.com"
endpoint_update = "/v1/domains/" + domain + "/records"
endpoint_records = "/v1/domains/" + domain + "/records/A/@"

def get_ip():
    r = requests.get("http://ip.42.pl/raw")
    if r.status_code != 200: # Fallback
        r = requests.get("https://api.ipify.org/?format=raw")
    return r.text

def update_dns(ip):
    headers = {"Authorization": "sso-key " + key + ":" + secret}
    records = requests.get(base_url + endpoint_records, headers=headers).json()
    record = {"data": ip, "name": "@", "type": "A"}
    new_records = []

    for _ in records:
        new_records.append(record)

    if len(new_records) >= 1:
        return  requests.put(base_url + endpoint_records, json=new_records, headers=headers)
    else:
        new_records.append(record)
        return requests.patch(base_url + endpoint_update, json=new_records, headers=headers)

ip = get_ip()
r = update_dns(ip)
if r.status_code == 200:
    print("[*] Updated dns record for " + domain + " to " + ip)
else:
    print("[!] Error updating dns record: " + r.status_code)