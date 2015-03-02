#!/usr/bin/env python2.7
## monitor.py for  in /home/eax/dev/vigilate/labeip/monitor_intra
## 
## Made by eax
## Login   <soules_k@epitech.net>
## 
## Started on  Wed Feb 25 02:46:08 2015 eax
## Last update Mon Mar  2 18:59:34 2015 eax
##

import sys
import time
import datetime
import json
import requests
from bs4 import BeautifulSoup

intra_session = requests.Session()

def login_get_token_fields(page):
    parser = BeautifulSoup(page)
    form = parser.find("form", attrs={"id": "login_form"})
    token = form.find("input", attrs={"name": "data[_Token][key]"})
    fields = form.find("input", attrs={"name": "data[_Token][fields]"})

    return (token.attrs["value"], fields.attrs["value"])

def send_login_form(token, fields):
    global intra_session
    login = raw_input("login:")
    password = raw_input("password:")
    post_data = {"_method": "POST",
                 "data[User][login]": login,
                 "data[User][password]": password,
                 "data[_Token][fields]": fields,
                 "data[_Token][key]": token}
    
    r = intra_session.post("https://eip.epitech.eu/users/login", data=post_data)
    return True
    

def read_login():
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
        strdate = date.text.strip().split("par", 1)[0].strip()


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
    open("savedlastinfo", "a+").close()
    with open("savedlastinfo") as f:
        try:
            savedlastinfo = json.load(f)
        except:
            print "savedlastinfo does not contain a valid json"

    if not savedlastinfo:
        update_saved(data)
        return
    
    sorted(data, key=lambda x: x["time"])
    sorted(savedlastinfo, key=lambda x: x["time"])
    
    if data[0]["time"] > savedlastinfo[0]["time"]:
        if len(data) == len(savedlastinfo):
            print "The comment for '%s' has been modified" % data[0]["name"]
        elif len(data) > len(savedlastinfo):
            mark = "without a mark"
            if data[0]["mark"]:
                mark = "(%s)" % data[0]["mark"]
            print "The comment for '%s' has been added %s" % (data[0]["name"], mark)

    update_saved(data)    

if __name__ == "__main__":
    read_login()
    w = get_wall()

        
    res = parse_wall(w)
    check_last_comment(res)

