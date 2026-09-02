<img width="1500" height="500" alt="QuickLogger_Header" src="https://github.com/user-attachments/assets/7fa9a1d3-c73b-4f6c-901d-676197ad41dc" />

**THIS PROJECT IS FOR EDUCATIONAL-PURPOSES ONLY!**
**I DO NOT ENCOURAGE NOR PROMOTE CYBER-CRIME!**
---


**What is QuickLogger?**

QuickLogger is an advanced KeyLogger built around David Bombal's KeyLogger source-code on GitHub.
It frequently uses pattern matching techniques and is able to detect: typed Passwords, typed Emails, typed Usernames, typed Domains.
It exfiltrates data across the network to https://webhook.site/, but since it's open-source you can easily modify it with a couple lines of code.
___
**How does it capture passwords?**

QuickLogger uses a long list of Possible, Overused, Months, and birth years, which are frequently used or combined in passwords.
Using the data it checks if the victim typed in a possible, overused, or month joined by a year which gets classified as a password.

(e.g: david2002, myaccount, may2016)
___
**What does does it FingerPrint from the system?**

Anti-Malware uses advanced heuristics which checks if a program accesses information from the system that it's not supposed to,
so in order for QuickLogger to keep a evade that detection it only fingerprints the administrator name and computer name since they're ordinary system-information
almost every application FingerPrints.
___
**How did QuickLogger get it's name?**

I wanted a simple and compact name like Snake Keylogger, 
I've choose Phoenix Keylogger at first for it to stand out (inspired by the BlackHole Phoenix A) but it was alreay taken, but
since the it is a KeyLogger and it's supposed to be as fast exfiltrating as possible (for a Python), I've went for 'QuickLogger' instead.
___
**Does it extract anything else?**

Yes, QuickLogger actually extracts additional text documents searching for passwords saved on the computer inside of them.
___
**Does QuickLogger have any evasion system?**
No, QuickLogger doesn't have any pre-built evasion systems due to 2 reasons:
1. (It's a waste of time) QuickLogger is meant to be a small project for Educational-Purposes.
2. If evasion systems we're included then that would mean infections would actually begin.
---

*Note: QuickLogger doesn't have an operating panel and never will as this is just a small project.*
