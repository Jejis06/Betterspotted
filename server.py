from flask import Flask,redirect,render_template,request
from flask_ngrok import run_with_ngrok
import requests
import json,os
import time,random
from modules import *
import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

checkDataBase()

creds = GET_CREDS()

TIME = creds['SERVER_SETTINGS'][0]["POSTING_TIME"]
HOUR = TIME[0]
MINUTE = TIME[1]



atexit.register(lambda: scheduler.shutdown())


NAME = creds['SERVER_SETTINGS'][0]["NAME"]
DESC = creds['SERVER_SETTINGS'][0]["DESC"]

app = Flask(__name__)
#run_with_ngrok(app)
#Sessions = []
PAYLOADS = dict()
MAX_CONNECTIONS = int(creds['SERVER_SETTINGS'][0]["MAX_CONNECTIONS_PER_DAY"])#specifies how much opinions one user can share


def check_da_time():
    ct = datetime.datetime.now()
    if (ct.hour == HOUR and ct.minute == MINUTE):
        global PAYLOADS
        PAYLOADS = dict()
        SEND()
        #CLEAR_DATA()

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_da_time, trigger="interval", seconds=60)
scheduler.start()


@app.route('/')
def red():
    return redirect('/send')


@app.route('/send',methods=["GET"])
def main():



    ip = request.remote_addr

    #for i in Sessions:
        #if i["parent"] == ip:
            #Sessions.remove(i)

    RAND = random.randint(0, 4 * 256)
    #d = {"parent": ip, "verify": RAND}
    #Sessions.append(d)

    return render_template("index.html",name=NAME,desc=DESC,rand=RAND)

@app.route("/recvdata" , methods=["POST"])
def recv_data():

    global PAYLOADS
    payload = request.form
    verify = payload["verify"]
    data = payload["data"]

    ip = request.remote_addr

    tm = int(time.time() * 1000)#czas w milisekundach



    #print(Sessions)


    #check all sesions
   # CAN = False
    #for i in Sessions:
       # if i["parent"] == ip:
          #  if int(i["verify"]) == int(verify):
             #   CAN = True
          #  Sessions.remove(i)

    # Cenzura
    if CENSOR(data)["check"] == True:
        CAN = True
    else:
        CAN = False
    if CAN == True:
        #weryfikacja
        try:
            a = int(PAYLOADS[ip])
            if a >= MAX_CONNECTIONS:
                print(f"[MAX CONNECTIONS FROM USER {ip}]")
                return "[MAX CONNECTIONS TRY TOMORROW]"
            else:
                PAYLOADS[ip] = a + 1


        except:
            PAYLOADS[ip] = 1

        print(f"[VALID CONNECTIONS TODAY {PAYLOADS}]")
        #EPICKI SYSTEM DO MOJEJ MAZY DANYCH

        o = {
            'born_ms':tm,
            'parent':ip,
            'data':data,
            'mode':CENSOR(data)['mode']
        }


        #checking
        checkDataBase()
        if open("data.json","r").read() == "":
            a = open("data.json","w").write("[]")


        #writing
        with open("data.json", "r+") as file:
            d = json.load(file)
            d.append(o)
            file.seek(0)
            json.dump(d, file,indent = 6)
        print(f"[SUCCESS => {ip}]")
        return "[SUCCESS]"
    else:
        print(f"[INVALID TOKEN - {ip}]")
        return f"[INVALID TOKEN]"


    return "[SUCCESS]"


def START_SERVER():
    app.run(host="0.0.0.0" ,port=int(creds['SERVER_SETTINGS'][0]["PORT"]))
    #app.run()