#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Yang Sen C
# Data  : 2014/06/22

#import json
#import pickle

import requests
import re
from bs4 import BeautifulSoup
#http://omz-software.com/pythonista/docs/ios/beautifulsoup_guide.html

if __name__ == '__main__':
    city = "nanjing"
    r = requests.get('http://aqicn.org/city/%s/' % city)
    #print r.status_code  #print r.headers['content-type']   #print r.encoding   #print r.text
    if r.status_code == 200:
        soup = BeautifulSoup(r.text)
        #http://www.leeon.me/upload/other/beautifulsoup-documentation-zh.html#Iterating%20over%20a%20Tag
        cur_pm25 = soup.findAll(align="center", id=re.compile("cur_pm25"))[0].text
        print "cur_pm25=",cur_pm25
        #min_pm25 = soup.findAll(align="center", id=re.compile("min_pm25"))[0].text
        #print "min_pm25=",min_pm25
        #max_pm25 = soup.findAll(align="center", id=re.compile("max_pm25"))[0].text
        #print "max_pm25=",max_pm25
    else:
        print "NULL"
    
    
    
    
    
    
    
    
    
    
    
    
