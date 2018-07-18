# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 16:18:01 2018

@author: Peter
"""
#imports
import serial
import serial.tools.list_ports
import time

#global vars
wheel = list('''.,-vlmjw²μf¥>¶+1234567890E£BFPSZV&YATL$R*C"D?NIU)W_=;:M'H(K/O!X§QJ%³G°¼¢½<Δ#txqΩ]@[ykphcgnrseaiduboz''')
position = 0
width = 12
perssure = 20

port = serial.Serial()
port.rts = True
port.baudrate = 4800
port.timeout = 1
portname = ''

#serial handelers
def portopen():
    if not port.is_open:
        port.port = portname
        port.open()

def portclose():
    if port.is_open:
        port.close()
#low level typewiter functions
def TWsend(data):
    for byte in data:
        n = 200
        while not port.cts :
            time.sleep(0.005)
            n -= 1
            if n < 0:
                raise NameError('Port not responding')
        port.write(byte)
        n=200
        while port.cts :
            time.sleep(0.005)
            n -= 1
            if n < 0:
                raise NameError('Port not responding')        
        n = 200
        while not port.cts:
            time.sleep(0.005)
            n -= 1
            if n < 0:
                raise NameError('Port not responding')
            port.rts = False
            port.rts = True
        
        #time.sleep(0.005)
        
def TWrec(n):
    return port.read(n)

def TWclr():
    tx = [b'\xa0',b'\x00']
    TWsend(tx)
    
def TWstart():
    tx = [b'\xa1',b'\x00']
    TWsend(tx)   
    print(TWrec(1))
    
def TWstx():
    tx = [b'\xa2',b'\x00']
    TWsend(tx)   
    print(TWrec(1)  )  
    
def TWetx():
    TWsend([b'\xa3',b'\x00'])   
    print(TWrec(1))   

def TWenq():
    tx = [b'\xa4',b'\x00']
    TWsend(tx)   
    print (TWrec(10))

def TWreset():
    TWsend([b'\x82',b'\x0f'])
#mid level typewriter functions
def TWconnect():
    port.reset_input_buffer()
    port.reset_output_buffer()
    port.rts = False
    port.rts = True
    tries = 10
    while not port.read(1) == b'\x01':
        print('waiting')
        tries -= 1
        if tries < 0:
            return 0
    TWclr()
    TWstart()
    TWenq()
    TWstx()    
    time.sleep(1)    
    TWposreset(True,True,True)
    return 1
    
def TWdisconnect():
    TWetx()
    TWclr()
      
def TWmove(x,y):
    x = int(x)
    y = int(y)
    if x:
        global position
        position = position + x
        hi = 192
        if x<0:
            hi += 32
        x = abs(x)
        x = max(min(x, 4095), 0)
        hi = hi +int(x/256)
        low= x%256
        TWsend([hi.to_bytes(1, byteorder='big'), low.to_bytes(1, byteorder='big')])
    if y:
        hi = 208
        if y<0:
            hi += 32
        y = int(abs(y))
        y = max(min(y, 4095), 0)
        hi = hi +int(y/256)
        low= y%256
        TWsend([hi.to_bytes(1, byteorder='big'), low.to_bytes(1, byteorder='big')])
        
def TWsetwidth(w):
    w = int(max(min(abs(w),255),0))
    TWsend([(128).to_bytes(1, byteorder='big'), w.to_bytes(1, byteorder='big')]) 
    global width
    width = w
        
def TWspace(s):    
    s = int(max(min(abs(s),255),0))
    TWsend([(131).to_bytes(1, byteorder='big'), s.to_bytes(1, byteorder='big')])  
    global position
    if s:
        position += s
    else:
        position += width
    
def TWbspace(s):
    s = int(max(min(abs(s),255),0))
    TWsend([(132).to_bytes(1, byteorder='big'), s.to_bytes(1, byteorder='big')]) 
    global position
    if s:
        position -= s
    else:
        position -= width
          
def TWCr():
    TWmove(-position, 16)

def TWposreset(carriage=True, typewheel=False, ribbon = False):
    r = 1
    if carriage:
        r += 2
        global position
        position = 0
    if typewheel:
        r += 4
    if ribbon:
        r += 8     
    TWsend([(130).to_bytes(1, byteorder='big'), r.to_bytes(1, byteorder='big')])

def TWtypeindex(ch, strength, right = True, move = True):
    ch = int(max(min(abs(ch),100),0))
    low = int(max(min(abs(strength),63),0))
    if not right:
        low += 64
    if move:
        low += 128
    TWsend([ch.to_bytes(1, byteorder='big'), low.to_bytes(1, byteorder='big')])   
    if move:
        global position    
        if right:           
            position += width
        else:
            position -= width 
    
def TWtype(data,strength = 20 , bold = False, underline = False):
    data = str(data)
    data= list(data)
    for c in data:
        if c == ' ':
            if bold:
                TWmove(1,0)
            if underline:
                TWtypeindex(wheel.index('_') + 1, strength, move = False)
            TWspace(0)
        elif c == '\n':
            TWCr() 
        else:
            if c in wheel:
                index = wheel.index(c) + 1
                
            else:
                index = wheel.index('?') + 1
            TWtypeindex(index, strength, move = not (bold or underline))
            if bold:
                TWmove(1,0)
                TWtypeindex(index, strength, move = not underline)
            if underline:                
                TWtypeindex(wheel.index('_') + 1, strength)
                
                
if 0:
    portname = 'COM3'
    portopen()
    TWconnect()
    time.sleep(1)
    TWdisconnect()
    portclose()