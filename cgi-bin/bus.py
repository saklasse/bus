#!/usr/bin/python3
# coding: utf-8
import os
print("Content-type:text/html\n\n")
print("")

#print ('<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">')
#print ("")
import sys
import base64
import urllib.request
from urllib.parse import unquote, quote
from html.parser import HTMLParser
from time import strftime, localtime
import time
from datetime import datetime
import re

#print( '<a class="weatherwidget-io" href="https://forecast7.com/en/69d6518d96/tromso/" data-label_1="TROMSØ" data-label_2="WEATHER" data-theme="original" >TROMSØ WEATHER</a>')
#print( "<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);}}(document,'script','weatherwidget-io-js');</script>" )

print( '<div style="background-image: url(\'http://flux.phys.uit.no/musmag/trod.gif\'); -webkit-background-size: cover; -moz-background-size: cover; -o-background-size: cover; background-size: cover;">' ) 
print( "<h1>" )
currentTime = strftime("%H:%M", localtime())
print( currentTime )
splitTime = currentTime.split(":")
timeInMinutes = int(splitTime[0]) * 60 + int(splitTime[1])
#print('<img src=http://flux.phys.uit.no/musmag/trod.gif style="height: 22vh; vertical-align: bottom;">')
print( "</h1>" )
#request = urllib.request.Request('https://rp.tromskortet.no/scripts/TravelMagic/TravelMagicWE.dll/svar?lang=en&from=Skippergata+%28Troms%C3%B8%29&dep1=1&Date='+strftime("%d.%m.%Y", localtime()) +'&Time=' + strftime("%H%%3A%M", localtime()))
request = urllib.request.Request('https://rp.tromskortet.no/scripts/TravelMagic/TravelMagicWE.dll/svar?lang=en&from=Alaskasvingen+%28Troms%C3%B8%29&dep1=1&Date='+strftime("%d.%m.%Y", localtime()) +'&Time=' + strftime("%H%%3A%M", localtime()))
result = urllib.request.urlopen(request)
resulttext = result.read().decode('utf-8')
resulttext = unquote(resulttext, encoding='utf-8')
goodClass = 0
busTimes = []
busRoute = []


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global goodClass
        global busTimes
        global busRoute
        global timeInMinutes
        if len(attrs) > 0:
            if attrs[0][0] == 'class':
                if 'departurelist-destination' in attrs[0][1]:
                    goodClass = 2
                elif 'departurelist-time' in attrs[0][1]:
                    goodClass = 3
                elif 'departurelist-linename' in attrs[0][1]:
                    goodClass = 1

#    def handle_endtag(self, tag):
#        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        global goodClass
        global busTimes
        global busRoute
        data = data.replace('\\r\\n', '')
        if goodClass > 0:
            if goodClass == 2:
#                print(data.encode().decode('unicode-escape').encode('latin1').decode('utf-8'))
                busRoute[0] = busRoute[0] + ' ' + data.encode().decode('unicode-escape').encode('latin1').decode('utf-8').strip()

            elif goodClass == 3:
                busRoute.append(data.strip())
                busTimes.append(busRoute)
                busRoute = []
            else:
                busRoute.append(data.strip())
        goodClass = 0

parser = MyHTMLParser()
parser.feed(resulttext)

busTimes.sort()
lastCount = 0
lastItem = ''
currentItems = []
for item in busTimes:
    if lastItem != item[0]:
        lastCount = 0
        lastItem = item[0]
    else:
        lastCount+=1

    if lastCount < 2:
        currentItems.append(item)

print('<table class="center">')
for x in sorted(currentItems, key=lambda x: x[1]):
    print('<tr>')
    print('<td>')
    print(x[0])
    print('</td>')
    departuresSplit = x[1].strip().split(":")
    if ((int(departuresSplit[0]) * 60 + int(departuresSplit[1]) ) - int(timeInMinutes)) <= 5:
        print('<td style="color:red;">' + x[1] + "</td>")
    else:
        print('<td>' + x[1] + '</td>')
    print('<tr>')
print('</table>')
print("</div>")
#        print(quote(item[0].encode('utf-8')), quote(item[1].encode('utf-8')))
