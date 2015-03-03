#!/usr/bin/env python3
## monitor.py for  in /home/eax/dev/vigilate/labeip/monitor_intra
## 
## Made by eax
## Login   <soules_k@epitech.net>
## 
## Started on  Wed Feb 25 02:46:08 2015 eax
## Last update Tue Mar  3 02:33:56 2015 eax
##

import sys
import time
import datetime
import json
import requests
import os.path
import getpass
import signal
import asyncio
from bs4 import BeautifulSoup
from hangout import MyHangBot

intra_session = requests.Session()

def get_creds():
    user = None
    pwd = None
    if os.path.isfile("creds"):
        with open("creds") as f:
            user, pwd = f.read().strip().split(" ", 1)

    if not user or not pwd:
        print("There is no `creds` file. Asking the user.")
        user = raw_input("User:")
        pwd = getpass.getpass("Password:")
        r = None
        while r != "n" and r != "y":
            if r != None:
                print("Please write 'y' or 'n'")
            r = raw_input("Save it in `creds` file ? [y/n]:")
        if r == "y":
            with open("creds", "w") as f:
                f.write("%s %s" % (user, pwd))

    return user, pwd

def login_get_token_fields(page):
    parser = BeautifulSoup(page)
    form = parser.find("form", attrs={"id": "login_form"})
    token = form.find("input", attrs={"name": "data[_Token][key]"})
    fields = form.find("input", attrs={"name": "data[_Token][fields]"})

    return (token.attrs["value"], fields.attrs["value"])

def send_login_form(token, fields):
    global intra_session
    login, password = get_creds()
    post_data = {"_method": "POST",
                 "data[User][login]": login,
                 "data[User][password]": password,
                 "data[_Token][fields]": fields,
                 "data[_Token][key]": token}
    
    r = intra_session.post("https://eip.epitech.eu/users/login", data=post_data)
    return parse_login_response(r.text)
    

def do_login():
    global intra_session
    r = intra_session.get("https://eip.epitech.eu/")
    token, fields = login_get_token_fields(r.text)
    if not send_login_form(token, fields):
        exit("Sending login failed.")
    
        

def get_wall():
    r = intra_session.get("https://eip.epitech.eu/projects/view/777")
    return r.text

def parse_wall(f):
    parser = BeautifulSoup(f)
    wall = parser.find('div', attrs={"id": "wall"})

    res = []
    
    for item in parser.find_all("div", attrs={"class": "accordion-group"}):
        header = item.find("div", attrs={"class": "accordion-heading"})
        inner = item.find("div", attrs={"class": "accordion-body"})
        date = inner.div.blockquote.small
        mark = inner.div.blockquote.find("small", attrs={"class": "mark-followup"})
        if "par" in date.text:
            strdate = date.text.strip().split("par", 1)[0].strip()
        else:
            strdate = date.text.strip().split("by", 1)[0].strip()


        ts = time.mktime(datetime.datetime.strptime(strdate, "%d/%m/%Y %H:%M").timetuple())
        title = header.find("h5").text
        marktxt = None
        if mark:
            marktxt = mark.text.strip().replace(" ", "")

        res.append({"name": title, "time": ts, "mark": marktxt})
    return res

def update_saved(data):
    with open("savedlastinfo", "w") as f:
        f.write(json.dumps(data))

def check_last_comment(data):
    savedlastinfo = None
    changed = False
    open("savedlastinfo", "a+").close()
    with open("savedlastinfo") as f:
        try:
            savedlastinfo = json.load(f)
        except:
            if not f.read():
                print("Empty saved info")
            else:
                print("savedlastinfo does not contain a valid json")

    if not savedlastinfo:
        update_saved(data)
        return
    
    sorted(data, key=lambda x: x["time"])
    sorted(savedlastinfo, key=lambda x: x["time"])

    msg = "No change since last time"
    if data[0]["time"] > savedlastinfo[0]["time"]:
        changed = True
        if len(data) == len(savedlastinfo):
            msg =  "The comment for '%s' has been modified" % data[0]["name"]
        elif len(data) > len(savedlastinfo):
            mark = "without a mark"
            if data[0]["mark"]:
                mark = "(%s)" % data[0]["mark"]
            msg = "The comment for '%s' has been added %s" % (data[0]["name"], mark)

    update_saved(data)
    return changed, msg
    
def parse_login_response(data):
    parser = BeautifulSoup(data)
    login_msg_failed = parser.find("div", attrs={"id": "authMessage"})
    if login_msg_failed:
        exit("Login failed: %s" % login_msg_failed.text)
    return True


def send_hangout_msg(msg):
    bot = MyHangBot()
    if not bot.login():
        exit()

    bot.set_connect_msg(open("hangout_room").read().strip(), msg)
    
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, lambda: bot.stop())
    loop.add_signal_handler(signal.SIGTERM, lambda: bot.stop())

    loop.run_until_complete(bot.client.connect())


if __name__ == "__main__":

    print("Login...")
    do_login()
    
    print("Getting wall...")
    w = get_wall()

    res = parse_wall(w)
    if not res:
        exit("Couldn't properly parse wall page.")
    ret = check_last_comment(res)
    if not ret:
        exit("First run")
    status,msg = ret
    if status:
        print("sending msg: %s" % msg)
        send_hangout_msg(msg)
        

