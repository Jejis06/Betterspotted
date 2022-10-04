import json
import os,sys
import time
from image_processing import GENERATE_PHOTO
import datetime
from PIL import Image, ImageFont, ImageDraw
from colorama import Fore
BLACKLIST = "blacklist.json"
CREDS = "creds.json"



#comes de Wątory, gdzie jeden kmieć a trzy dwory

#get credentials form CREDS json file
def GET_CREDS():
    try:
        with open(CREDS, 'r') as openfile:
            data = json.load(openfile)
        return data
    except:
        return False



#check if has database
def checkDataBase(name="data.json"):
    if os.path.isfile(name) == False:
        try:
            open(name, 'a').close()
        except OSError:
            print(Fore.RED + f'[CANT CREATE DATABASE PLEASE CREATE {name} FILE IN THIS DIR]' + Fore.WHITE)
        else:
            print(Fore.GREEN + '[SUCCESS WHEN CREATING DATABASE]' + Fore.WHITE)
#cenzor data acording to BLACKLIST json file
def CENSOR(data):
    if os.path.isfile(BLACKLIST) == False:
        print(Fore.RED +f"[ERROR '{BLACKLIST}' DOESNT EXIST]" + Fore.WHITE)
        sys.exit(0)
    with open(BLACKLIST, "r+") as file:
        base = json.load(file)

    #check if word is in blacklist
    for i in base["blocked_words"]:
        ff = f" {i} "
        if ff in data:
            approved = False
    #check if smthing is in any way in  file
    for i in base["inline_blocked_words"]:
        ff = f" {i} "
        if ff in data:
            approved = False

    else:
        approved =True

    #set the theme
    if approved:
        x = 1
        for i in base["themes"][0]["rainbow"]:
            ff = f" {i} "
            if ff in data:
                x = 2
        if x == 1:
            for i in base["themes"][0]["sad"]:
                ff = f" {i} "
                if ff in data:
                    x = 3

    if approved:
        return {"check":True,"mode":x}
    else:
        return {"check":False}

#mabe ill use it later
def ProgressBar(process,total):
    prc = 100*(process/float(total))
    bar = chr(219) * int(prc) +'_'*(100-int(prc))
    print(f"\r|{bar}|{prc:.2f}%",end="\r")



#clear data and mabe save it to save dir
def CLEAR_DATA():
    creds = int(GET_CREDS()['SERVER_SETTINGS'][0]["SAVE_DATA"])
    if creds == 1: #2 to zle
        if os.path.isdir("./past_data/") == False:
            os.mkdir("./past_data/")
        t = time.time()
        ml = int(t * 1000)
        data = str(ml)
        os.mkdir(f"./past_data/{data}")
        os.replace(f"./data.json",f"./past_data/{data}/data.json")
    with open("data.json","w") as f:
        f.write("[]")
        f.close()

#send to instagram
def SEND(debug = False,noremove = False,nosend=False):

    MAX_POSTS_PER_DAY = 25
    checkDataBase()
    creds = GET_CREDS()
    INSTAGRAM_USERNAME = creds['INSTAGRAM_SETTINGS'][0]["LOGIN"]
    INSTAGRAM_PASSWORD = creds['INSTAGRAM_SETTINGS'][0]["PASSWORD"]

    SPLITTER = int(creds['INSTAGRAM_SETTINGS'][0]['MAX_IMAGES_IN_POST']) # max images in one post




    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            f.close()
    except:
        print(Fore.GREEN + "[ERROR WITH OPENING FILE]" + Fore.WHITE)
        sys.exit(0)
    imagefile = "img"
    PATH = f"./{imagefile}/"
    
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    SIZE = len(data)
    SEND_AMM = SIZE



    if SIZE > SEND_AMM:
        SIZE = SEND_AMM

    if (SIZE > 0):

        print(Fore.MAGENTA + "[STARTING SENDING PROCEDURE]\n[PREPARING PHOTOS]" + Fore.WHITE)

        os.environ["LOG"] = INSTAGRAM_USERNAME
        os.environ["PAS"] = INSTAGRAM_PASSWORD
        All = []
        msgarr = []
        modearr = []

        for i in range(SIZE):
            t = datetime.datetime.fromtimestamp(data[i]['born_ms'] / 1000.0)
            parent = data[i]['parent']
            msg = data[i]['data']

            mode = data[i]['mode']
            file = f"{PATH}img{i}.jpeg"

            msgarr.append(msg)
            modearr.append(mode)
            All.append(file)

        FONT_PATH = GET_CREDS()['INSTAGRAM_SETTINGS'][0]['FONT_PATH']
        arr = All
        num = len(arr)

        W = 1080
        H = 608
        
        #If someone reads this im sorry
        
        Slice = SPLITTER
        o = [0] * Slice
        for i in range(Slice):
            npm = Slice - i
            if (num % npm < num):
                o[i] = ((num - num % npm) / npm)
                num -= npm * ((num - num % npm) / npm)
        global PPP
        PPP = 0
        All = []
        for i in range(len(o)):
            if int(o[i]) != 0:

                for j in range(int(o[i])):
                    rm = []
                    rmm = []
                    rmmm = []
                    dst = Image.new('RGB', (W, H))
                    for jj in range(Slice - i):
                        dst.paste(
                            GENERATE_PHOTO(msgarr[jj], FONT=FONT_PATH, MODE=modearr[jj], amm=Slice - i,
                                           H=int(608 / (Slice - i))), (0, jj * int(H / (Slice - i))))
                        rm.append(arr[jj])
                        rmm.append(msgarr[jj])
                        rmmm.append(modearr[jj])
                    for jj in range(len(rm)):
                        arr.remove(rm[jj])
                        msgarr.remove((rmm[jj]))
                        modearr.remove((rmmm[jj]))

                    file = f"{PATH}img{PPP}.jpeg"
                    All.append(file)


                    if debug == True:
                        print(Fore.GREEN + f"[GENERATED_SUCCESFULLY => {file}]" + Fore.WHITE)
                        dst.show()
                    dst.save(file, subsampling=0, quality=100)
                    PPP += 1
        if debug == True:
            print(o)
        if nosend == False:
            print(Fore.YELLOW + "[UPLOADING PHOTOS -  THIS METHOD OF SENDING CAN BE BUGGY AND NOT WORK SOMETIMES I WANT TO IMPLEMENT MORE EFFICIENT WAY OF POSTING BUT FOR NOW IT IS HOW IT IS]" + Fore.WHITE)
            cmd = "node ./poster/index.js "
            for i in All:
                cmd += i
                cmd += " "
            if debug == True:
                print(f"[EXECUTING COMMAND : {cmd}]")
            os.system(cmd)


        if noremove == False:
            print(Fore.MAGENTA + "[CLEANING]" + Fore.WHITE)
            time.sleep(2)
            for i in All:
                os.remove(i)
        if debug == False:
            CLEAR_DATA()
        print(Fore.GREEN + "[DONE]" + Fore.WHITE)
    else:
        print(Fore.MAGENTA + "[NO POSTS TODAY]" + Fore.WHITE)

SEND(debug=True,nosend=True)
