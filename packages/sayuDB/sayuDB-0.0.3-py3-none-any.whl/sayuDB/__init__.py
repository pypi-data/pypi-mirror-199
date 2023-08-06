from .processor import *
import os, json

if not os.path.isfile('config.json'):
    with open('config.json', 'w') as ww:
        json.dump({
    "blocked_ip": []
}, ww, indent=4)
if not os.path.isfile('users.json'):
    with open('users.json', 'w') as ww:
        json.dump({
    "root": {
        "username": "root",
        "password": "",
        "access": []
    }
}, ww, indent=4)

if not os.path.isdir('datas'):
    os.makedirs('datas')