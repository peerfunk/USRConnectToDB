import serial
import MySQLdb
import socket
import re
from threading import Thread
from time import sleep

class DataSet:
    def __init__(self):
        pass
    @classmethod
    def grab_data(self,string):
        if string[0] == '\2' or string[1]=='\2':
            if string[0] =='\2':
                string = string[1:]
            elif string[1]=='\2':
                string = string[2:]
            ' '.join(string.split())
            return(string)
        elif string[0] == '\3':
            ende()
        else:
            return string
class DataBase:
    cnx = None
    cursor = None
    def __init__(self):
        print("New Database Connection")
        self.cnx = MySQLdb.connect(user='root', db='serial', passwd='password', host='')
        self.cursor = self.cnx.cursor()
    def write(self,ip, data):
        self.cursor.execute("""INSERT INTO serial.serial VALUES (null,null,%s,%s, null)""", ( data, ip))
        self.cnx.commit()
    def __del__(self):
        self.cursor.close()
        self.cnx.close()
        
class InterfaceHandler:
    ThreadList=[]
    BUFFER_SIZE = 1024
    def __init__(self):
        TCPips = {'192.168.10.9':8084,'192.168.10.8':20108,'192.168.10.10':20108} #Server Connector
        for key, value in TCPips.items():
            print("creating thread for: " + key)
            thread = Thread(target = self.run , args=[key,value])
            thread.daemon = False
            thread.start()
            self.ThreadList.append(thread)
    def run(self,ip,port):
        DB = DataBase()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        print("capture started")
        while(True):
            data = s.recv(self.BUFFER_SIZE).decode('ascii')
            DB.write(ip, DataSet.grab_data(data))
        s.close()
    def __del__(self):
        for thread in ThreadList:
            thread.stop()
#DB = DataBase()           
x = InterfaceHandler()
#with serial.Serial('COM1', 9600,bytesize=serial.SEVENBITS,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_TWO) as ser:
#    while 1:
#        word = ser.readline().decode('ascii')
#        DataSet.grab_data(word)

