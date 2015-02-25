#!/usr/bin/env python2.7
## monitor.py for  in /home/eax/dev/vigilate/labeip/monitor_intra
## 
## Made by eax
## Login   <soules_k@epitech.net>
## 
## Started on  Wed Feb 25 02:46:08 2015 eax
## Last update Wed Feb 25 04:30:46 2015 eax
##

import sys
import time
import datetime
import json
from bs4 import BeautifulSoup

def parse_html(f):
    parser = BeautifulSoup(open("eip.html"))
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
            print "The comment for '%s' has been added" % (data[0]["name"], mark)

    update_saved(data)    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit("Usage: %s eip_wall_file.html" % sys.argv[0])

    res = parse_html(open(sys.argv[1]).read())
    check_last_comment(res)

