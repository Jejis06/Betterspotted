from colorama import Fore
from modules import CREDS,BLACKLIST
import subprocess
import json,os



name = None
description = None
instalogin = None
instapassword = None
mcpd = None
postingtime = None
DATA = {}

def blacklist_info():

    dd = f"""
\t\t\t\t\t\t\t\t\t[BLACKLIST QUICK GUIDE]
    I created file called {BLACKLIST}. In there there are lists that are named 'blocked_words' ,'inline_blocked_words' and 'themes'
    
    {BLACKLIST}
        |
        |
        |->'blocked_words' - in this list you can add words that you dont want to post on your spotted    
        |
        |->'inline_blocked_words' - in this list you can add special charatcters or sets of characters that you dont want to appear in the contents you post
        |
        |->'themes' - themes is a special list that has two sublists called 'rainbow' and 'sad' that let you customize your posts apperance
                |
                |->  'rainbow' - is a sublist where you add words for wich you want the background to be rainbow
                |
                |->  'sad' - is a sublist where you add words for wich you want the background to be black and white
            
        !!! Deafult theme is random background color and its fitting color as font color !!!
    
    """

    print(Fore.YELLOW + dd + Fore.WHITE)
    with open("./manual.txt","w") as f:
        f.write(dd)
        f.close()




def setup():
    global DATA
    print(Fore.GREEN + "\t\t\t\t\t\t\t\t\t[INITIATING SETUP]")
    print(Fore.MAGENTA + "\t\t\t[SERVER SETTINGS]")
    server_settings()
    print(Fore.GREEN + "\t\t\t\t\t\t\t\t\t[ALL SERVER SETTINGS DONE]")
    print(Fore.MAGENTA + "\t\t\t[INSTAGRAM SETTINGS]")
    instagram_settings()
    DATA = {
        "SERVER_SETTINGS": [
            {
                "SAVE_DATA": 1,
                "POSTING_TIME":postingtime,
                "PORT": 8080,
                "NAME": name,
                "DESC": description,
                "MAX_CONNECTIONS_PER_DAY": mcpd
            }
        ],
        "INSTAGRAM_SETTINGS": [
            {
                "LOGIN": instalogin,
                "PASSWORD": instapassword,
                "MAX_IMAGES_IN_POST":3,
                "FONT_PATH": "./static/fonts/font2.ttf"
            }
        ]
    }
    print(Fore.MAGENTA + "\t\t\t[Your choices]")
    print(DATA)
    a = input("Submit? 'y' or 'n': ")
    if a == "n":
        setup()
    else:
        print(Fore.GREEN +"\t\t\t\t\t\t\t\t\t[SETUP COMPLETE]")
        print(Fore.WHITE)
def server_settings():
    global mcpd
    global description
    global name
    global postingtime

    name = input(Fore.WHITE + "Name of your spotted : ")
    description = input("Short description of your spotted : ")
    mcpd = input("Max number of submitions user can make per day (20 works great) : ")
    try:
        int(mcpd)
    except :
        print(Fore.RED +"\t\t\t[ERROR NOT A NUMBER SO SETTING IT TO DEAFULT (20)]" + Fore.WHITE)
        mcpd = 20
    postingtime =  input("On what exact time the bot should post your images. Format => hh,mm : ")
    try:
        t = postingtime.split(",")
        h = int(t[0])
        m = int(t[1])
        postingtime = [h,m]
    except :
        print(Fore.RED + "\t\t\t[ERROR WITH DATE SO RESTARTING SETUP]" )
        server_settings()
def instagram_settings():
    global instalogin
    global instapassword
    print(Fore.YELLOW + "Remember the account you want to use has to be buisnes account (HOW TO CREATE BUISSNES ACCOUNT : https://www.facebook.com/business/help/502981923235522)" + Fore.WHITE)
    instalogin = input("Instagram login of your spotted : ")
    instapassword = input("Password : ")
    print(Fore.YELLOW + "[CHECKING IF THE LOGIN AND PASSWORD IS CORRECT (THIS MIGHT TAKE A WHILE)]")
    x = subprocess.getoutput(f"node ./poster/login.js {instalogin} {instapassword}")

    if x == "1" or x == 1:
       print(Fore.RED + "\t\t\t[WRONG CREDENTIALS]")
       instagram_settings()



def start():
    TITLE = f"""
    {Fore.YELLOW}__________________________________________________________________________________________________
    \t\t\t\t   _____ ____  ____  ______________________     ____  ____  ______
    \t\t\t\t  / ___// __ \/ __ \/_  __/_  __/ ____/ __ \   / __ )/ __ \/_  __/
    \t\t\t\t  \__ \/ /_/ / / / / / /   / / / __/ / / / /  / __  / / / / / /   
    \t\t\t\t{Fore.BLUE} ___/ / ____/ /_/ / / /   / / / /___/ /_/ /  / /_/ / /_/ / / /    
    \t\t\t\t/____/_/    \____/ /_/   /_/ /_____/_____/  /_____/\____/ /_/
    ______________________________________________________________________{Fore.MAGENTA}by Ignacy Bu{Fore.BLUE}________________

        """

    print(TITLE)  # title screen

    if os.path.isfile(CREDS) == False:
        setup()
        with open(CREDS, "w") as o:
            json.dump(DATA, o, indent=6)

    if os.path.isfile(BLACKLIST) == False:
        new_blacklist = {'blocked_words': [], 'inline_blocked_words': [],
                         'themes': [{'rainbow': ['rainbow'], 'sad': ['sad']}]}
        with open(BLACKLIST, "w") as o:
            json.dump(new_blacklist, o, indent=6)
        blacklist_info()

    print(Fore.GREEN + "\t\t\t\t\t\t\t\t\t[STARTING SERVER]")
    print(Fore.WHITE)
    from server import START_SERVER
    START_SERVER()


if __name__ == '__main__':
    start()



