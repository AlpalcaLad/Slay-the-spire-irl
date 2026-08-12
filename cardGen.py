import cv2
import numpy as np

cards = [ # art, name, type, energy, description
    #("./cards/",1,"",[""]),
    # Wine connoisseur
    ("./art/cards/strike_wine.png","Strike", "attack", 1,["Deal 1 $Damage$"]),
    ("./art/cards/defend_wine.png","Defend", "skill", 1,["Gain 1 $Block$"]),
    ("./art/cards/grape_time.png","Grape Time", "skill", 0,["Add 1 $Grape$"]),
    ("./art/cards/fruity_aroma.png","Fruity Aroma", "skill", 1,["$Draw$3 cards", "$Discard$1 card"]),
    ("./art/cards/royal_gamble.png","Royal Gamble", "skill", 0,["Shuffle 2 $Dazed$","into draw pile", "gain 2 $energy$"]),
    ("./art/cards/snobbery.png","Snobbery", "skill", 2,["Gain 2 $block$","apply 1 $weak$", "Add 2 snobbish"]),
    ("./art/cards/grape_dance.png","Grape Dance", "skill", 1,["Add 3 $Grapes$","$Exhaust$"]),
    ("./art/cards/bottle_smack.png","Bottle Smack", "attack", 1,["Deal 3 $Damage$","$Exhaust$"]),
    ("./art/cards/grape_shot.png","Grape Shot", "power", 1,["$Grapes$hit all enemies","Add 3 $Grapes$"]),
]

from PIL import Image, ImageDraw, ImageFont

def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

def putTextPIL(img,text,pos,size,colour,outline=True,outlineColour=(0,0,0)):
    img = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    font = ImageFont.truetype("./misc/kreon.ttf",size)
    draw = ImageDraw.Draw(img)
    if outline:
        outlineDepth = 3
        draw.text((pos[0]+outlineDepth,pos[1]-outlineDepth),text,font=font,fill=outlineColour)
        draw.text((pos[0]-outlineDepth,pos[1]-outlineDepth),text,font=font,fill=outlineColour)
        draw.text((pos[0]+outlineDepth,pos[1]+outlineDepth),text,font=font,fill=outlineColour)
        draw.text((pos[0]-outlineDepth,pos[1]+outlineDepth),text,font=font,fill=outlineColour)
    draw.text(pos,text,font=font,fill=colour)
    img = np.array(img)[:, :, ::-1].copy()
    return img

A4pages = []
A4image = np.ones((2480,3508,3),dtype=np.uint8)*255

def overlay(img: cv2.typing.MatLike,subimg: cv2.typing.MatLike,x: int,y: int,caption:str=""):
    s = subimg.shape
    img[y:y+s[0],x:x+s[1]]=subimg
    if caption != "":
        tSize, _ = cv2.getTextSize(caption,cv2.FONT_HERSHEY_SIMPLEX,1,2)
        cv2.putText(img,caption,(x+s[0]//2-tSize[0]//2,y+s[1]+35),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)

def putTextPlus(img,objs,pos,size):
    font = ImageFont.truetype("./misc/kreon.ttf",size)
    hSize = 0
    x = pos[0]
    for o in objs: #(type="str"|"img",string|image, c1, c2)
        if o[0]=="str":
            hSize = font.getmask(o[1]).getbbox()[2]
            img=putTextPIL(img,o[1],(x,pos[1]),size,o[2],True,o[3])
            x += hSize + 16
        elif o[0]=="img": 
            raise NotImplementedError("Image handling not defined in description writing")
        else:
            raise Exception("Invalid arguments passed to putTextPlus: ",o)

    return img

def placeCard(img:cv2.typing.MatLike, card: cv2.typing.MatLike,x:int,y:int,name:str,ctype:str,energy:int,description:list[str]):
    overlay(img,card,x,y)

    #energy
    font = ImageFont.truetype("./misc/kreon.ttf",80)
    img = putTextPIL(img,str(energy),(x+70-font.getmask(str(energy)).getbbox()[2]//2,y+30),80,(255,255,255),True,(0,0,0))

    #name
    font = ImageFont.truetype("./misc/kreon.ttf",60)
    img = putTextPIL(img,name,(x+340-font.getmask(name).getbbox()[2]//2,y+70),60,(255,255,255),True,(0,0,0))

    #type
    font = ImageFont.truetype("./misc/kreon.ttf",45)
    img = putTextPIL(img,ctype,(x+345-font.getmask(ctype).getbbox()[2]//2,y+480),45,(255,255,255),True,(0,0,0))

    #description
    font = ImageFont.truetype("./misc/kreon.ttf",55)
    for d in description:
        keyword = False
        bbox = font.getmask(d.replace("$","")).getbbox()
        tempString = ""
        strings = []
        for c in d:
            if c=="$":
                if tempString != "":
                    strings.append(("str",tempString,(255,255,0) if keyword else (255,255,255),(0,0,0)))
                    tempString = ""
                keyword = not keyword
            else:
                tempString = tempString + c
        if tempString != "":
            strings.append(("str",tempString,(255,255,0) if keyword else (255,255,255),(0,0,0)))
        img=putTextPlus(
            img,
            strings,
            (x+345-bbox[2]//2, y + 560),
            55
        )
        y += bbox[3]+16

    return img

border = 60
negBorderX = 80
negBorderY = 140
x = border
y = border
offset = 0
blankPage = True
for c in cards:
    card=cv2.imread(c[0])
    card=cv2.resize(card,None,fx=0.5,fy=0.5) #resize
    card=card[
        negBorderY:card.shape[0]-negBorderY,
        negBorderX:card.shape[1]-negBorderX,
    ] #crop

    A4image = placeCard(A4image,card,x,y,c[1],c[2],c[3],c[4])

    blankPage = False
    x+=card.shape[1]+offset
    if x > 3508 - border - card.shape[1]:
        x = border
        y += card.shape[0]+offset
        if y > 2480 - border - card.shape[0]:
            #new page
            A4pages.append(A4image)
            A4image = np.ones((2480,3508,3),dtype=np.uint8)*255
            blankPage = True
            x = border
            y = border

if not blankPage:
    A4pages.append(A4image)

for i in range(len(A4pages)):
    cv2.imwrite("./testdata/cards"+str(i)+".png",A4pages[i])
#cv2.waitKey(0)
cv2.destroyAllWindows()