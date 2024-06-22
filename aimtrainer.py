import pyglet
from random import randint
import math
import time

from pickle import dump
import threading
from datetime import datetime
import json



window  = None
t  = 0
init = False
start = -1
debounce = -1
score = 0 
latencies = []
x,y = 0,0




def speed(tab):
    if len(tab) == 0: return 0
    s = 0
    for i in range(len(tab)):s = s + tab[i]
    return s / len(tab)
def end(): 
    global latencies,score,window,t
    e= {}
    e['date']  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    e["score"] =  score
    e['speed'] = speed(latencies)
    e['time'] = t
    F = open('history.dat','ab')
    dump(e,F)
    F.close()
    window.close() 


def run():
    global x, y, debounce,latencies,start,init,score,window,t
    F = open('settings.json','r')
    e =  json.load(F)
    F.close()
    
    t = e['time']
    r = e['radius']

    window = pyglet.window.Window(fullscreen=e['fullscreen'])
    batch  = pyglet.graphics.Batch()

    

    x = randint(0, window.width  - r)
    y = randint(0, window.height - r)




    @window.event
    def on_mouse_press(cx, cy, button, modifiers):
        global x, y, debounce,latencies,start,init,score
        k = time.time() 
        d = math.sqrt((cx - x) ** 2 + (cy - y) ** 2)

        if d < r:
            x = randint(r, window.width  - r)
            y = randint(r, window.height - r)

            if init :
                latencies.append(time.time() - debounce)
                score = score + 1 
            else :
                start = k
                init  = True 

            debounce = k 

        else : 
            if init:  score = score - 1  


    @window.event
    def on_draw():
        a = pyglet.shapes.Circle(x, y, r, color=(55, 55, 255), batch=batch)
        window.clear()
        batch.draw()
    


    T = threading.Timer(e['time'],end)
    T.start()  
    pyglet.app.run() 
if __name__=='__main__':
    run()
 
 

