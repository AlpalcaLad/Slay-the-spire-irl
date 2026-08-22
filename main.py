from qreader import QReader
import cv2
import time
from multiprocessing import Process,Queue,freeze_support
import qr_read
from gameFile import *
import keyboard
import os

class manager():
    def __init__(self):
        #image processing variables
        self.prevImage = None
        self.oldCards = {}
        self.keepFor = 60*4 #how many ticks before card can be replayed
        self.cam = cv2.VideoCapture(0)
        self.fps = 120
        self.laplaceThresh = 1000

        #imported module setup
        self.r = qr_read.reader()
        self.queryConn = self.r.setupThread()
        self.g = game()
        #no multithreading for pygame
        self.gameConn = self.g.setup() #regular array

        #misc variables
        self.startTime = time.time()
        self.elapsedTime = 0
        self.awaiting = False

    def reset(self):
        pygame.quit()
        c.target = None
        self.g = game()
        self.gameConn = self.g.setup()

    def main(self):
        while True:
            self.elapsedTime=time.time()-self.startTime
            #print(self.elapsedTime)
            self.tick()
            self.g.waitTick(self.fps)

    def tick(self):
        #card reading
        if not self.awaiting:
            self.awaiting=True
            ret, frame = self.cam.read()

            #self.prevImage = frame
            #cv2.imshow("feed",frame)
            self.queryConn.send(frame)
        else:
            if self.queryConn.poll():
                received = list(self.queryConn.recv())
                for c in received:
                    if c is not None:
                        if c not in self.oldCards:
                            if c == "reset":
                                self.reset()
                                break
                            self.gameConn.append(c)
                            self.oldCards[c]=self.keepFor
                        else:
                            self.oldCards[c]=self.keepFor

                self.awaiting=False

        try:
            self.g.mainloop()
        except Exception as e:
            print(e)
            #if repeated errors we should auto restart

        toRemove = []
        for c in self.oldCards:
            self.oldCards[c]-=1
            if self.oldCards[c]<=0:
                toRemove.append(c)
        for r in toRemove:
            self.oldCards.pop(r)
        #print(self.oldCards)

if __name__=="__main__":
    m = manager()
    m.main()