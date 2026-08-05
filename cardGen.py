import cv2
import numpy as np

cards = [ # art, energy, name, description
    #("./cards/",1,"",[""]),
    ("./cards/grape_dance.png",1,"Grape Dance",["Add 3 [grape]s","exhaust"]),
]

A4pages = []
A4image = np.ones((2480,3508,3),dtype=np.uint8)*255

def overlay(img: cv2.typing.MatLike,subimg: cv2.typing.MatLike,x: int,y: int,caption:str=""):
    s = subimg.shape
    img[y:y+s[0],x:x+s[1]]=subimg
    if caption != "":
        tSize, _ = cv2.getTextSize(caption,cv2.FONT_HERSHEY_SIMPLEX,1,2)
        cv2.putText(img,caption,(x+s[0]//2-tSize[0]//2,y+s[1]+35),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)

def placeCard(img:cv2.typing.MatLike, card: cv2.typing.MatLike,x:int,y:int,name:str,energy:int,description:list[str]):
    pass

border = 20
x = border
y = border
offset = 410
blankPage = True
for c in cards:
    cv2.resize(cv2.imread(c[0]))
    placeCard(A4image,)