#! /usr/bin/python
#-*- coding: utf-8 -*-
#==========================================================
#Titre: timer
#
#
#Par: Paco SAMBA
#===========================================================

import threading ,time, datetime

verrou=threading.Lock()

class TimerDevice(threading.Thread):
    def __init__(self,func, *args, **kwargs):
        threading.Thread.__init__(self)
        self.func=func
        self.args=args
        self.kwargs=kwargs
        self.runable=True

    def run(self):
        while self.runable:
            verrou.acquire()
            self.func(*self.args, **self.kwargs)
            verrou.release()
                
                


    def stop(self):
        self.runable=False


 
                
