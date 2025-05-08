import pyperclip
import requests
import random
import string
import time
import sys
import re
import os
from colorama import init, Fore, Back, Style
init(autoreset=True)  # Initialize colorama

# Update the API key
API = 'https://mailsac.com/v2/k_n5cjHnOj2cIByM4ii1bDXRMfymVo9wvi6c528ldBHO'

# Update the domain list
domainList = ['mailsac.com']
domain = random.choice(domainList)

def banner():
    print(Fore.CYAN + r'''                                                                                
        ▄████  ██   █  █▀ ▄███▄   █▀▄▀█ ██   ▄█ █     
        █▀   ▀ █ █  █▄█   █▀   ▀  █ █ █ █ █  ██ █     
        █▀▀    █▄▄█ █▀▄   ██▄▄    █ ▄ █ █▄▄█ ██ █     
        █      █  █ █  █  █▄   ▄▀ █   █ █  █ ▐█ ███▄  
         █        █   █   ▀███▀      █     █  ▐     ▀ 
          ▀      █   ▀              ▀     █           
                ▀                        ▀                   
    ''')
    print(Fore.YELLOW + "          domainList = ['mailsac.com','mailsac.com','mailsac.com']")
    print(Fore.MAGENTA + "          " + "═" * 40)
    print(Fore.MAGENTA + "          Code Creator: " + Fore.GREEN + "Sami Khatatba")
    print(Fore.MAGENTA + "          " + "═" * 40 + "\n")

def generateUserName():
    name = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(name) for i in range(10))
    return username

def extract():
    getUserName = re.search(r'login=(.*)&',newMail).group(1)
    getDomain = re.search(r'domain=(.*)', newMail).group(1)
    return [getUserName, getDomain]

# Got this from https://stackoverflow.com/a/43952192/13276219
def print_statusline(msg: str):
    last_msg_length = len(print_statusline.last_msg) if hasattr(print_statusline, 'last_msg') else 0
    print(' ' * last_msg_length, end='\r')
    print(Fore.GREEN + msg, end='\r')
    sys.stdout.flush()
    print_statusline.last_msg = msg

def deleteMail():
    url = 'https://mailsac.com/api/addresses/{email}'.format(email=mail)
    headers = {
        'Mailsac-Key': 'k_n5cjHnOj2cIByM4ii1bDXRMfymVo9wvi6c528ldBHO'
    }

    print_statusline(Fore.RED + "Disposing your email address - " + mail + '\n')
    req = requests.delete(url, headers=headers)

def checkMails():
    url = f'https://mailsac.com/api/addresses/{mail}/messages'
    headers = {
        'Mailsac-Key': 'k_n5cjHnOj2cIByM4ii1bDXRMfymVo9wvi6c528ldBHO'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 403:
            print_statusline(Fore.RED + "Access denied. The email address might be invalid or rate limit exceeded.")
            return
        response.raise_for_status()
        req = response.json()
    except requests.exceptions.RequestException as e:
        print_statusline(Fore.RED + f"Error checking mails: {str(e)}")
        return
    except ValueError:
        print_statusline(Fore.RED + "Invalid response from server")
        return

    length = len(req)
    if length == 0:
        print_statusline("Your mailbox is empty. Hold tight. Mailbox is refreshed automatically every 5 seconds.")
    else:
        idList = []
        for i in req:
            for k,v in i.items():
                if k == 'id':
                    mailId = v
                    idList.append(mailId)

        x = 'mails' if length > 1 else 'mail'
        print_statusline(f"You received {length} {x}. (Mailbox is refreshed automatically every 5 seconds.)")

        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'All Mails')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        for i in idList:
            msgRead = f'{API}?action=readMessage&login={extract()[0]}&domain={extract()[1]}&id={i}'
            req = requests.get(msgRead).json()
            for k,v in req.items():
                if k == 'from':
                    sender = v
                if k == 'subject':
                    subject = v
                if k == 'date':
                    date = v
                if k == 'textBody':
                    content = v

            mail_file_path = os.path.join(final_directory, f'{i}.txt')

            with open(mail_file_path,'w') as file:
                file.write("Sender: " + sender + '\n' + "To: " + mail + '\n' + "Subject: " + subject + '\n' + "Date: " + date + '\n' + "Content: " + content + '\n')

banner()
print(Fore.MAGENTA + "Welcome to FakeMail Generator!")
userInput1 = input(Fore.BLUE + "Do you wish to use to a custom domain name (Y/N): ").capitalize()

try:
    if userInput1 == 'Y':
        userInput2 = input(Fore.BLUE + "\nEnter the name that you wish to use as your domain name: ")
        newMail = f"{API}?login={userInput2}&domain={domain}"
        reqMail = requests.get(newMail)
        mail = f"{extract()[0]}@{extract()[1]}"
        pyperclip.copy(mail)
        print("\nYour temporary email is " + mail + " (Email address copied to clipboard.)" +"\n")
        print(Fore.CYAN + f"---------------------------- | Inbox of {mail}| ----------------------------\n")
        while True:
            checkMails()
            time.sleep(5)

    if userInput1 == 'N':
        newMail = f"{API}?login={generateUserName()}&domain={domain}"
        reqMail = requests.get(newMail)
        mail = f"{extract()[0]}@{extract()[1]}"
        pyperclip.copy(mail)
        print("\nYour temporary email is " + mail + " (Email address copied to clipboard.)" + "\n")
        print(Fore.CYAN + f"---------------------------- | Inbox of {mail} | ----------------------------\n")
        while True:
            checkMails()
            time.sleep(5)

except KeyboardInterrupt:
    deleteMail()
    print(Fore.RED + "\nProgramme Interrupted")
    os.system('cls' if os.name == 'nt' else 'clear')