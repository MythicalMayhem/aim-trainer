from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication,QMessageBox ,QTableWidgetItem
import json 
from pickle import load,dump 
import subprocess
 
app = QApplication([])
w = loadUi('mainmenu.ui')


def displayHistory():
    tab = w.table
    F = open('history.dat','rb')
     
    tab.setRowCount(0)
    k = 0
    while True:
        try:
            e = load(F)
            tab.insertRow(k)
            tab.setItem(k,0,QTableWidgetItem(str(e['date'])))
            tab.setItem(k,1,QTableWidgetItem(str(e['score'])))
            tab.setItem(k,1,QTableWidgetItem(str(e['time'])))
            tab.setItem(k,3,QTableWidgetItem(str(e['speed'])))
            k = k + 1        
        except:
            F.close()
            break


def start():
    F = open('settings.json','w')

    e = {}
    e['radius'] = int(w.radius.text()) or 10 
    e['time'] = float(w.time.text()) or 30.0
    e['fullscreen'] = w.fullscreen.isChecked() or False 

    json.dump(e,F)

    F.close()

    subprocess.run('python aimtrainer.py')
 
displayHistory()
w.refresh.clicked.connect(displayHistory)
w.start.clicked.connect(start)
w.show()
app.exec()