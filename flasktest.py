# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 20:56:42 2018

@author: Peter
"""

import serial

import serial.tools.list_ports

from flask import Flask

app = Flask(__name__)

port = 'COM3'


@app.route('/')
def hello():
    return 'Boobies!'


@app.route('/findports')
def findports():
    
    ports=[port.device for port in serial.tools.list_ports.comports() if port[2] != 'n/a']
    
    ret = 'Avalable ports:\n' 
    for port in ports:
        ret += port + '\n'
        
    return ret

@app.route('selsctport/<port>')
def selectport(port):
      ports=[p.device for p in serial.tools.list_ports.comports() if p[2] != 'n/a']
      if port in ports:
          return 'port set to: ' + port
      else:
          return 'port not found'

@app.route('/test')
def findports():
    
    port 
        
    return ret
    
    
    
    
    

if __name__ == '__main__':
   app.run()