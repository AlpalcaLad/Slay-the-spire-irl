from qreader import QReader
import cv2
import time
from multiprocessing import Process,Queue,freeze_support
import qr_read
import keyboard
import os

class game():
    def __init__(self):
        self.oldCards = []
        self.r = qr_read.reader()
        self.queryConn = self.r.setupThread()
        self.startTime = time.time()
        self.elapsedTime = 0
        self.awaiting = False

    def main(self):
        while True:
            time.sleep(0.001)
            self.elapsedTime=time.time()-self.startTime
            #print(self.elapsedTime)
            self.tick()

    def tick(self):
        if not self.awaiting:
            self.awaiting=True
            self.queryConn.send("./testdata/QRcodes1.png" if keyboard.is_pressed("n") else "./testdata/QRcodes2.png")
        else:
            if self.queryConn.poll():
                recieved = self.queryConn.recv()
                print(recieved)
                self.awaiting=False

if __name__=="__main__":
    g = game()
    g.main()