import cv2
import numpy as np
import segno

qrcodes = [
    #characters
    "cocktail",
    "driver",
    "beermaster",
    "winecon",
    #strikes/defends
    "strikeA1",
    "strikeA2",
    "strikeA3",
    "strikeA4",
    "defendA1",
    "defendA2",
    "defendA3",
    "defendA4",
    #admin
    "endturn",
    "reset",
    "killall"
    #cocktail mixer cards
    #designated driver cards
    #beermaster cards
    #wine connosieur cards
    #misc cards
    #enemies
    #events
]

A4pages = []
A4image = np.ones((2480,3508,3),dtype=np.uint8)*255

def overlay(img: cv2.typing.MatLike,subimg: cv2.typing.MatLike,x: int,y: int,caption:str=""):
    s = subimg.shape
    img[y:y+s[0],x:x+s[1]]=subimg
    if caption != "":
        tSize, _ = cv2.getTextSize(caption,cv2.FONT_HERSHEY_SIMPLEX,1,2)
        cv2.putText(img,caption,(x+s[0]//2-tSize[0]//2,y+s[1]+35),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)

def cvSegno(text):
    mat = np.array(segno.make_qr(text).matrix)
    mat = np.uint8(mat * 255)
    mat = cv2.resize(
        mat, (0,0), fx = 14, fy = 14, interpolation=cv2.INTER_NEAREST
    )
    return cv2.cvtColor(mat,cv2.COLOR_GRAY2BGR)

border = 20
x = border
y = border
offset = 100
blankPage = True
for t in qrcodes:
    imToOverlay = cvSegno(t)
    overlay(A4image,imToOverlay,x,y,caption=t)
    blankPage = False
    x+=imToOverlay.shape[0]+offset
    if x > 3508 - 20 - imToOverlay.shape[0]:
        x = 20
        y += imToOverlay.shape[1]+offset
        if y > 2480 - 20 - imToOverlay.shape[1]:
            #new page
            A4pages.append(A4image)
            A4image = np.ones((2480,3508,3),dtype=np.uint8)*255
            blankPage = True
            x = border
            y = border

if not blankPage:
    A4pages.append(A4image)

# cv2.imshow("img",cv2.resize(
#         A4image, (0,0), fx=0.4,fy=0.4
#     )
# )
for i in range(len(A4pages)):
    cv2.imwrite("./testdata/QRcodes"+str(i)+".png",A4pages[i])
#cv2.waitKey(0)
cv2.destroyAllWindows()