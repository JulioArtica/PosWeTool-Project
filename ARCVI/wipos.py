import CaseInsensitiveDict
import subprocess
import os
import time
import json
import requests



# Create context data for AR-CVI

url = "http://localhost:1026/ngsi-ld/v1/entities"
headers = {"Content-Type": "application/ld+json"}

# Initialization variables
acum = 1
only_once = 0

while only_once == 0:

    # Get position values of wipos
    wipos_values = subprocess.check_output("curl -G -X GET \
    'http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:Device:Megacal:wipos-agv-1' \
    -d 'options=keyValues'", shell=True)
    dict_wipos_values = json.loads(wipos_values)

    # Position values X and Y
    [posx,posy] = dict_wipos_values["relativePosition"]
    #print(posx)
    #print(posy)
    posx_N = (posx-1066.5)/2700
    posy_N = (posy-777.313)/5552.238

    data2 = """{
            "workParameters": {
                "type": "Property",
                "value": {
                  "type":"Reset",
                  "displayStatus":"inProgress",
                  "images":[
                      {   
                          "position":["-0.19","0.355","0.0"],
                          "width":"100.0",
                          "height":"130.0",
                          "path":"/images/Logo_SMASP.png"},
                      {   
                          "position":["-0.08","0.355","0.0"],
                          "width":"225.0",
                          "height":"90.0",      
                          "path":"/images/Logo_Megacal.png"},



                      {   
                          "position":["-0.51","0.28","0.0"],
                          "width":"500.0",
                          "height":"400.0",      
                          "path":"/images/Titulo_IZQ.png"},
                      {   
                          "position":["0.22","0.28","0.0"],
                          "width":"400.0",
                          "height":"250.0",      
                          "path":"/images/Titulo_DER.png"},

                      {   
                          "position":["0.15","0.24","0.0"],
                          "width":"170.0",
                          "height":"200.0",      
                          "path":"/images/REF.png"},

                      {   
                          "position":["0.435","0.24","0.0"],
                          "width":"250.0",
                          "height":"200.0",      
                          "path":"/images/100_DAMAGED.png"},


                      {   
                          "position":["0.08","0.210","0.0"],
                          "width":"350.0",
                          "height":"390.0",
                          "path":"/images/tem_gamma.png"},
                      {   
                          "position":["0.39","0.210","0.0"],
                          "width":"350.0",
                          "height":"390.0",
                          "path":"/images/damaged_gamma.png"},
                      {   
                          "position":["0.17","0.025","0.0"],
                          "width":"500.0",
                          "height":"890.0",
                          "path":"/images/control_inspected.png"},

                      {   
                          "position":["0.3","0.05","0.0"],
                          "width":"150.0",
                          "height":"200.0",      
                          "path":"/images/CURRENT.png"},

                      {
                          "position":["-0.64","0.22","0.0"],
                          "width":"813.0",
                          "height":"400.0",
                          "path":"/images/Layout_v3.png"},
                      { 
                          "position": [%s,%s,"0.0"],
                          "width":"100.0",
                          "height":"100.0",
                          "path":"/images/Circle_Y.jpg"}%s
                  ],
                  "pois":[

                      { 
                          "position":["-0.45","-0.14","0.0"],
                          "radius":"0.0",
                          "label":"Actual Position: %s",
                          "fill_color":{"r":"0.0","g":"0.0","b":"0.0","a":"1.0"},
                          "border_color":{"r":"1.0","g":"1.0","b":"1.0","a":"1.0"}
                          }
                  ],
                  "boxes":[
                      {
                          "position":["0.03","0.0597","0.0"],
                          "width":"0.0001",
                          "height":"0.44",
                          "label":"",
                          "fill_color":{"r":"0.7","g":"0.7","b":"0.7","a":"0.7"},
                          "border_color":{"r":"1.0","g":"1.0","b":"1.0","a":"1.0"}}
                  ]
                         
                }
            },
            "@context": [
            ]
    }"""
    data3 = """"""
    area = "Milling Zone"
    if (posy_N < 0.080 and posy_N > 0.040 and posx_N < -0.469 and posx_N > -0.497):
        data3 = """,{
                      "position":["-0.3","-0.09","0.0"],
                      "width":"300.0",
                      "height":"450.0",
                      "path":"/images/4-06/4_06_2.jpg"}"""
        area = "Turning Zone - 4-06"

    elif (posy_N < 0.185 and posy_N > 0.142 and posx_N < -0.469 and posx_N > -0.506):
        data3 = """,{
                      "position":["-0.3","-0.06","0.0"],
                      "width":"300.0",
                      "height":"450.0",
                      "path":"/images/5-01/5_01.jpg"}"""
        area = "Turning Zone - 5-01"
    elif (posy_N < 0.22 and posy_N > 0.149 and posx_N < -0.403 and posx_N > -0.447):
        data3 = """,{
                      "position":["-0.3","-0.06","0.0"],
                      "width":"300.0",
                      "height":"450.0",
                      "path":"/images/7-06/7_06.jpg"}"""
        area = "Milling Area - 7-06"
    elif (posy_N < 0.1035 and posy_N > 0.047 and posx_N < -0.3305 and posx_N > -0.361):
        data3 = """,{
                      "position":["-0.3","-0.09","0.0"],
                      "width":"300.0",
                      "height":"450.0",
                      "path":"/images/3-08/3_08_3.jpg"}"""
        area = "Turning Zone - 3-08"

    elif (posy_N < 0.2189 and posy_N > 0.1493 and posx_N < -0.312 and posx_N > -0.375):
        data3 = """,{
                      "position":["-0.3","-0.09","0.0"],
                      "width":"300.0",
                      "height":"450.0",
                      "path":"/images/8-06/8_06_1.jpg"}"""
        area = "Milling Area - 8-06"
    elif (posy_N < 0.1128 and posy_N > 0.030 and posx_N < -0.272 and posx_N > -0.3165):
        data3 = """,{
                      "position":["-0.3","-0.09","0.0"],
                      "width":"300.0",
                      "height":"450.0",
                      "path":"/images/9-06/9_06_1.jpg"}"""
        area = "Workshop Area - 9-06"
    else:
        data3 = """,{
                      "position":["-0.3","-0.09","0.0"],
                      "width":"300.0",
                      "height":"450.0",
                      "path":"/images/Vacio.png"}"""
        area = ""        
    
    resp2 = requests.patch(url, data=data2 %(str(posx_N),str(posy_N),data3,str(area)), headers=headers)
    print(resp2.status_code)
    time.sleep(2)
