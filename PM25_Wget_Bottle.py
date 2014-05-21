#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Use Wget and Python Bottle Webframework

#
# Note: Setup on AWS EC2 Linux Server
# http://ec2-54-255-162-192.ap-southeast-1.compute.amazonaws.com:5888/shanghai/
# http://ec2-54-255-162-192.ap-southeast-1.compute.amazonaws.com:5888/shanghai/pm25
# http://ec2-54-255-162-192.ap-southeast-1.compute.amazonaws.com:5888/shanghai/json

import os , sys, re , random, json
from bottle import route, run

def query(city):
    count = 0
    data = {'city':city}
    url = 'http://aqicn.org/city/%s/' % city 
    print "[URL]:%s" % url
    # wget aqicn data, save it to tmpfile
    tmpfile = "/dev/shm/%s.txt" % ('').join(random.sample('1234567890zyxwvutsrqponmlkjihgfedcba',6))
    print "[TEMPFILE]=%s" % tmpfile
    cmd="/usr/bin/wget %s -O %s" % (url,tmpfile)
    os.system(cmd)
    #parse
    html = open(tmpfile,'r').read().split('</td>')
    pattern = re.compile("<td id='(\w+)'(.*?)align=center>(\d+)", re.I|re.S)
    
    #<td id='cur_pm25' class='tdcur' style='font-weight:bold;font-size:11px;' align=center>194
    for line in html:
        match = pattern.search(line)
        if match and count < 33:
           count = count + 1
           #print line
           #print match.group(1), match.group(3)
           data[match.group(1)] = match.group(3)
    
    #return dict
    return data

@route('/')
def index():
    return ("Tornado PM25 Query WebServer By Yang Sen C")

@route('/:cityname')
def index(cityname='shanghai'):
    data = query(cityname)
    return "<br>RealTime AQI of %s <br><br>PM2.5:  Cur=%s Min=%s Max=%s" % (cityname.capitalize(), data['cur_pm25'],data['min_pm25'], data['max_pm25'])

@route('/:cityname/pm25')
def index(cityname='shanghai'):
    return query(cityname)['cur_pm25']

@route('/:cityname/json')
def index(cityname='shanghai'):
    return json.dumps( query(cityname), skipkeys=True )

if __name__=="__main__":
   run(host='ec2-54-255-162-192.ap-southeast-1.compute.amazonaws.com', port=5888)