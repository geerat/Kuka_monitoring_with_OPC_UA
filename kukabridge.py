#DO NOT ALTER THIS FILE! 



































































































import paho.mqtt.client as mqtt
import sys
from threading import Thread
from time import sleep
from inspect import signature
import struct

try:
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
except:
    print("tkinter not installed on system. In case of further warnings or error no messageboxes will be displayed.")


        
class KUKABridge:
    

    def newdata(self):
        if self.newdatacb:
            if self.callback_len_par==0:
                self.newdatacb()
            if self.callback_len_par==1:
                self.newdatacb(self.axisdata)
            if self.callback_len_par==2:
                self.newdatacb(self.axisdata,self.status)
        else:
            self.new_data_available=True

    def get_axisdata():
       return self.axisdata
       


    def register_callback(self, cb):
        sig=signature(cb)
        self.callback_len_par=len(sig.parameters)
        self.newdatacb=cb   

    def mqttackcheck(self):
        #print("About to check")
        if not self.MQTTAck:
            print("!!!!!!!!!!!NOT ABLE TO LINK AGAINST KUKA BRIDGE!!!!!!!! TERMINATE !!!!! Contact assignment tutor !!!!!!!!!!")
            try:
                messagebox.showwarning('Error','Connection to the networked/virtual KUKA controller could not be established. Contact assignment tutor. Please close the program')
            except:
                pass
            exit()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self,client, userdata, flags, rc):    

        client.subscribe(self.bp+self.rg+self.gr+"/KUKA/Status/+")
        client.subscribe(self.bp+self.rg+self.gr+"/KUKA/Status")
        client.subscribe(self.bp+self.rg+self.gr+"/KUKA/Axis_Act")
      
        client.publish(self.bp+self.rg+self.gr+"/KUKA/Admin","Connect")      
        client.publish(self.bp+self.rg+self.gr+"/KUKA/Port",self.port)
       
    # The callback for when a PUBLISH message is received from the server.
    def on_message(self,client, userdata, msg):
        #print (msg.topic)
        #print (msg.payload)
        if not hasattr(self.axisdata,'newdatacb'):
            pass           
        self.NewDataArrived=True
        slist=msg.topic.split("/")
        if slist[-1]=="ACK":
            self.MQTTAck=True
            #print ("Acknowledged")
        elif slist[-1]=="Axis_Act":            
            self.axisdata=struct.unpack('7f',msg.payload)
            self.newdata()
        elif slist[-1]=="Status":
            self.status=str(msg.payload,'utf-8')
            self.newdata()
            if self.status=="Stopped":
                pass
                #print(self.status)
            #print(self.status)
        else:
            print("argh")
            pass

    def ryba(self,port):       
        def karp(numerek):
            liczba=0
            for literka in numerek:
                liczba+=int(literka)
            return liczba
        
        if port.isnumeric():           
            if not (int(port[4])==0) and not (int(port[-3])==0) and (int(port[2:4])/int(port[4]))==(int(port[-5:-3])/int(port[-3])) and karp(port[:-2])==int(port[-2:]):
                self.gr=str(int(((int(port[2:4])/int(port[4]))+(int(port[-5:-3])/int(port[-3])))/2)).zfill(2)                
                return
        self.MQTTAck=False
        self.mqttackcheck()
                
        
    def __init__(self, port):
        self.axisdata= None
        self.status= None
        self.new_data_available= False

        self.callback_len_par=0
        self.newdatacb= None

        self.gr="Unassigned"
        self.ryba(port)
        
        self.programname = ""
        self.status="Idle"
        self.port=port
        self.bp="ICom/"
        self.MQTTAck=False
        self.rg="Group"
        self.myThread = Thread(target=self.myTimer, args=([2]))
        self.myThread.setDaemon(True)
        self.myThread.start()
        self.notstopped=True
        self.client=mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.will_set("ICom/"+self.rg+self.gr+"/KUKA/Admin","Offline")
        self.client.username_pw_set("uoa709","lisms709")     
        self.client.connect("130.216.216.47", 1883, 60)
        #print("About to loop")
        self.client.loop_start()
        #print("Controller initialised")
        sleep(1)
  
        
    def myTimer(self, seconds):        
        sleep(seconds)
        self.mqttackcheck()

    def Start(self):    
        self.client.publish(self.bp+self.rg+self.gr+"/KUKA/Admin","Start")
        
    def Stop(self):
        self.client.publish(self.bp+self.rg+self.gr+"/KUKA/Admin","Stop")
        
    def updatedata(self):        
        pass
    def LoadProgram(self, name):
        self.programname=name
        self.client.publish(self.bp+self.rg+self.gr+"/KUKA/LoadProgram",name)
        #print(name.strip().lower()=="Step1_1.src".strip().lower())
        #print(name.strip().lower())
        #print("Step1_1.src".strip().lower())
        if name.strip().lower()=="Step1_1.src".strip().lower():
            sleep(0.1)
            return True
        else:
            sleep(0.1)
            return False

def main():
    #Quick main for testing purposes
    from kukabridge import KUKABridge
    kuka=KUKABridge("error")
    
if __name__=="__main__":
   main()