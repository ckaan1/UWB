# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 11:23:12 2015

@author: nedshelt
"""

from flask import Flask, jsonify, request
import random
import time
app = Flask(__name__)

tag0 = {'ID':0,'x':0,'y':0,'enabled':False}
tag1 = {'ID':1,'x':0,'y':0,'enabled':False}
tag2 = {'ID':2,'x':0,'y':0,'enabled':False}
tag3 = {'ID':3,'x':0,'y':0,'enabled':False}

@app.route("/location")

def get_locations():
    generateFakeData = True
    if generateFakeData:
        xO = random.uniform(45,50)
        yO = random.uniform(45,50)
        zO = random.uniform(0,1.2)
        tag0['x'] = xO
        tag0['y'] = yO
    return jsonify(tags=[tag0,tag1,tag2,tag3]) #t0=T0 , t1=T1, t2=T2, t3=T3)

@app.route("/update", methods=['GET', 'PUT'])

def updateTest():
    #return 'This page does exist'
    xyz = request.values
    print request.values     
    tag0['x'] = xyz['x']   
    tag0['y'] = xyz['y']
    tag0['enabled'] = True
    return 'got values x:{},y:{},z:{}'.format(xyz['x'],xyz['y'],xyz['z'])
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded = False)

