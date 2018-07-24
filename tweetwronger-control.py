# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 20:56:42 2018

@author: Peter
"""

#import serial
#
#import serial.tools.list_ports

from flask import Flask, render_template, request, url_for, abort

import typecontrol as tc
import textwrap

app = Flask(__name__)

portname = ''

@app.route('/')
def index():
    return render_template('index.html', status = tc.port.isOpen())

@app.route('/findports')
def findports():    
    ports=[port.device for port in tc.serial.tools.list_ports.comports() if port[2] != 'n/a']            
    return  render_template('findports.html', ports = ports)

@app.route('/connect')
def connect():
    tc.portname  = request.args.get('port', '')
    tc.portopen()
    return render_template('connect.html', success = tc.TWconnect(),  url = url_for('index'))
    
@app.route('/disconnect')
def disconnect():
    tc.TWdisconnect()
    return render_template('disconnect.html', url = url_for('index'))

@app.route('/type')
def twtype():  
    if tc.port.is_open:
        if request.args.get('wrap',''):
            lines = textwrap.wrap(request.args.get('text', ''),int(request.args.get('width', '70')))
            text = ''
            for line in lines:
                text += line +'\n'
        else:
            text = request.args.get('text', '')
        if request.args.get('strength', ''):
            tc.TWtype(text,
                      bold = request.args.get('bold', ''),
                      underline = request.args.get('underline', ''),
                      strength = int(request.args.get('strength', '')))
        else:
            tc.TWtype(text,
              bold = request.args.get('bold', ''),
              underline = request.args.get('underline', ''))    
        return render_template('type.html')
    else:
        abort(503)
    return render_template('type.html')

@app.route('/move')
def move():
    if tc.port.is_open:
        x = request.args.get('x', '0')
        y = request.args.get('y', '0')
        if not x:
            x = 0
        if not y:
            y = 0
        tc.TWmove(int(x), int(y),)    
    return render_template('move.html')

@app.route('/setwidth')
def setwidth():
    if tc.port.is_open:
        w = request.args.get('width', '12')
        if not w:
            w = 12
        tc.TWsetwidth(int(w))    
    return render_template('setwidth.html')

if __name__ == '__main__':
   #webbrowser.open_new('http://127.0.01')
   app.run(host = '0.0.0.0', port =80)