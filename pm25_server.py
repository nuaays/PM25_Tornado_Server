#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Note: Setup on AWS EC2 Linux Server
# App can get the PM2.5 JSON data from the URL: http://ec*-*-*-*-*.XX-XX-X.compute.amazonaws.com:8888/{CityName}
#
import tornado.ioloop
import tornado.web

import simplejson as json
import pickle

import requests
import re
from bs4 import BeautifulSoup

class PM25:
    def __init__(self):
        self._cur_pm25 = 'N/A'  # Current PM2.5 Value
        self._min_pm25 = 'N/A'  # Min PM2.5 Value
        self._max_pm25 = 'N/A'  # Max PM2.5 Value
        self._cur_pm10 = 'N/A'  # Current PM10 Value
        self._cur_o3   = 'N/A'  #
        self._cur_no2  = 'N/A'
        self._cur_so2  = 'N/A'
        self._cur_co   = 'N/A'
        self._cur_temp = 'N/A'  # 温度  
        self._cur_dew  = 'N/A'  # 露水
        self._cur_pressure  = 'N/A' # 气压
        self._cur_humidity  = 'N/A' # 湿度
        self._cur_wind      = 'N/A' # 风力
        
    def pm25(self):
        return self._cur_pm25

    def temp(self):
        return self._cur_temp

    def key_pollutant(slef):
    	if self._cur_pm25 > self._cur_pm10:
    		return "PM2.5=%s" % self._cur_pm25
    	else:
    		return "PM10 =%s" % self._cur_pm10
    
    def getjson(self):
        data = { 'PM25':self._cur_pm25, 
                 'PM10':self._cur_pm10, 
                 'O3' :self._cur_o3, 
                 'NO2':self._cur_no2, 
                 'SO2':self._cur_so2,
                 'CO' :self._cur_co,
                 'Temperature':self._cur_temp,
                 'Dew':self._cur_dew,
                 'Pressure':self._cur_pressure,
                 'Himidity':self._cur_humidity,
                 'Wind':self._cur_wind
                }
        
        return json.dumps(data,skipkeys=True)

    def run(self, city):
        url = 'http://aqicn.org/city/%s/' % city   #http://aqicn.org/city/shanghai/
        print "URL:%s" % url
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text)
            self._cur_pm25 = soup.findAll(align="center", id=re.compile("cur_pm25"))[0].text
            self._min_pm25 = soup.findAll(align="center", id=re.compile("min_pm25"))[0].text
            self._max_pm25 = soup.findAll(align="center", id=re.compile("max_pm25"))[0].text
            self._cur_pm10 = soup.findAll(align="center", id=re.compile("cur_pm10"))[1].text
            self._cur_o3   = soup.findAll(align="center", id=re.compile("cur_o3"))[1].text
            self._cur_no2  = soup.findAll(align="center", id=re.compile("cur_no2"))[1].text
            self._cur_so2  = soup.findAll(align="center", id=re.compile("cur_so2"))[1].text
            self._cur_co   = soup.findAll(align="center", id=re.compile("cur_co"))[1].text
            self._cur_temp = soup.findAll(align="center", id=re.compile("cur_t"))[1].text
            self._cur_dew  = soup.findAll(align="center", id=re.compile("cur_d"))[1].text
            self._cur_pressure = soup.findAll(align="center", id=re.compile("cur_p"))[1].text
            self._cur_humidity = soup.findAll(align="center", id=re.compile("cur_h"))[1].text
            self._cur_wind     = soup.findAll(align="center", id=re.compile("cur_w"))[1].text
        else:
            print "[Error] Failed in querying the AQI of %s From %s " % (city, url)
        

class MainHandler(tornado.web.RequestHandler):  
    def get(self):  
        self.write("Tornado PM25 Query WebServer By Yang Sen C")

class QueryPM25(tornado.web.RequestHandler):  
    def get(self, city):
        query = PM25()
        query.run(city)
        self.write("<br>The RealTime AQI of %s <br>" % city.capitalize() )
        print query.pm25()
        self.write( "<br>PM2.5=%s, Temperature=%s<br>" % (query.pm25(), query.temp() ) )
        self.write( '<br>Key Pollutant is %s <br>' % query.key_pollutant() )
        self.write( query.getjson() )
        
        
application = tornado.web.Application( [  (r"/",MainHandler),  (r"/([a-z]*)",QueryPM25)] )  

if __name__=="__main__":  
    application.listen(8888)  
    tornado.ioloop.IOLoop.instance().start() 