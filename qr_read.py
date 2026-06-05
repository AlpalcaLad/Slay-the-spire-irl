from qreader import QReader
import cv2
import time
from multiprocessing import Process,Pipe

class reader():
    def __init__(self):
        self.qr = QReader()
        self.metrics = True
        self.cards = []

    def readCodes(self,img):
        texts = self.qr.detect_and_decode(image=img)
        return texts
    
    def fromImage(self,path):
        start = time.time()
        texts = self.readCodes(cv2.cvtColor(cv2.imread(path),cv2.COLOR_BGR2RGB))
        end = time.time()
        print("Read in " + str(end-start) + "s")
        return texts
    
    def writeToFile(self,img,writePath):
        texts = self.readCodes(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        f = open(writePath,"w")
        f.write(", ".join(texts))
        f.close()
        
    def readThread(self, conn):
        while True:
            time.sleep(0.01)
            imgToProcess = conn.recv()
            if imgToProcess is not None:
                #start = time.time()
                conn.send(self.readCodes(cv2.cvtColor(cv2.imread(imgToProcess),cv2.COLOR_BGR2RGB)))
                #print(str(time.time()-start) + " seconds to process")

    def setupThread(self):
        parentConn, childConn = Pipe()
        p = Process(target=self.readThread,args=(childConn,))
        p.start()
        return parentConn

if __name__ == "__main__":
    r = reader()
    print(r.fromImage("./testdata/QRcodes1.png"))