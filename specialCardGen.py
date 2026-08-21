import cv2
import numpy as np

cards = [ # template, name, type, image, description, [xOff, yOff, scale]
    #region enemies
    # ["./art/cards/misc/enemyTemplate.png","cultist","enemy","./art/enemies/cultist.png",["Also $summon$ all", "other $cultists$"],[0,0,0.75]],
    # ["./art/cards/misc/enemyTemplate.png","cultist","enemy","./art/enemies/cultist.png",["Also $summon$ all", "other $cultists$"],[0,0,0.75]],
    # ["./art/cards/misc/enemyTemplate.png","cultist","enemy","./art/enemies/cultist.png",["Also $summon$ all", "other $cultists$"],[0,0,0.75]],
    # ["./art/cards/misc/enemyTemplate.png","Fossil Stalker","enemy","./art/enemies/fossil_stalker.png",[],[-55,40,1]],
    # ["./art/cards/misc/enemyTemplate.png","Frog Knight","enemy","./art/enemies/frog_knight.png",[],[0,0,0.6]],
    # ["./art/cards/misc/eliteTemplate.png","Giant Head","elite","./art/enemies/giant_head.png",[],[-65,40,0.7]],
    # ["./art/cards/misc/eliteTemplate.png","Lagavulin","elite","./art/enemies/lagavulin.png",[],[-10,0,0.7]],
    # ["./art/cards/misc/enemyTemplate.png","Leaf Slime","enemy","./art/enemies/leaf_slime.png",["Also $summon$", "$mawler$"],[0,40,0.5]],
    # ["./art/cards/misc/enemyTemplate.png","Mawler","enemy","./art/enemies/mawler.png",[],[-20,30,0.75]],
    # ["./art/cards/misc/enemyTemplate.png","Nibbit","enemy","./art/enemies/nibbit.png",[],[-40,65,0.75]],
    # ["./art/cards/misc/enemyTemplate.png","Orb Walker","enemy","./art/enemies/orb_walker.png",[],[0,40,0.75]],
    # ["./art/cards/misc/eliteTemplate.png","Skulking Colony","elite","./art/enemies/skulking_colony.png",[],[0,0,0.75]],
    # ["./art/cards/misc/enemyTemplate.png","Slaver","enemy","./art/enemies/slaverA.png",["Also $summon$ the", "other $slaver$"],[-20,40,0.75]],
    # ["./art/cards/misc/enemyTemplate.png","Slaver","enemy","./art/enemies/slaverB.png",["Also $summon$ the", "other $slaver$"],[-20,40,0.75]],
    # ["./art/cards/misc/eliteTemplate.png","Terror Eel","elite","./art/enemies/terror_eel.png",[],[-60,-30,0.9]],
    # ["./art/cards/misc/enemyTemplate.png","Thief","enemy","./art/enemies/thief.png",["Also $summon$ the", "other $thief$"],[-10,40,0.85]],
    # ["./art/cards/misc/enemyTemplate.png","Thief","enemy","./art/enemies/thief.png",["Also $summon$ the", "other $thief$"],[-10,40,0.85]],
    # ["./art/cards/misc/enemyTemplate.png","Vine Shambler","enemy","./art/enemies/vine_shambler.png",[],[0,0,0.7]],
    
    #region potions
    # ["./art/cards/misc/potionTemplate.png","Weak Pot","potion","./art/potions/weak.png",["Apply 1 $weak$"],[20,60,2.5]],
    # ["./art/cards/misc/potionTemplate.png","Strength Pot","potion","./art/potions/strength.png",["Gain 1 $strength$","$this combat$"],[20,60,2.5]],
    # ["./art/cards/misc/potionTemplate.png","Vulnerable Pot","potion","./art/potions/vulnerable.png",["Apply 1 $vulnerable$"],[20,60,2.5]],
    # ["./art/cards/misc/potionTemplate.png","Tipsy Pot","potion","./art/potions/tipsy.png",["Apply 3 $tipsy$"],[20,60,2.5]],
    # ["./art/cards/misc/potionTemplate.png","Energy Pot","potion","./art/potions/energy.png",["Gain 2 $energy$"],[20,60,2.5]],
    # ["./art/cards/misc/potionTemplate.png","Exhaust Pot","potion","./art/potions/exhaust.png",["$Exhaust$ 2 cards","in your $hand$"],[20,60,2.5]],
    # ["./art/cards/misc/potionTemplate.png","Fire Pot","potion","./art/potions/damage.png",["Deal 2 $damage$"],[20,60,2.5]],
    # ["./art/cards/misc/potionTemplate.png","Heal Pot","potion","./art/potions/heal.png",["$Heal$ 1 hp"],[20,60,2.5]],
    # ["./art/cards/misc/potionTemplate.png","Free Pot","potion","./art/potions/potFree.png",["The next card","you play is","$free$"],[20,60,2.5]],
    # ["./art/cards/misc/potionRareTemplate.png","Fruit Juice","potion","./art/potions/maxHp.png",["Gain 1 $max hp$", "$permanently$"],[20,60,2.5]],
    # ["./art/cards/misc/potionRareTemplate.png","Buff Pot","potion","./art/potions/permStrength.png",["Gain 1 $strength$", "$permanently$"],[20,60,2.5]],
    # ["./art/cards/misc/potionRareTemplate.png","Fruit Juice","potion","./art/potions/maxHp.png",["Gain 1 $max hp$", "$permanently$"],[20,60,2.5]],
    # ["./art/cards/misc/potionRareTemplate.png","A Fucking Rock","potion","./art/potions/rock.png",["Deal 6 $damage$"],[20,60,2.5]],
    # ["./art/cards/misc/potionRareTemplate.png","Score Pot","potion","./art/potions/score.png",["Gain 5 $score$"],[20,60,2.5]],
    # ["./art/cards/misc/potionRareTemplate.png","Stun Stew","potion","./art/potions/stun.png",["$Stun$ the enemy", "this turn"],[20,60,2.5]],
    # ["./art/cards/misc/potionRareTemplate.png","Excorcism","potion","./art/potions/remove.png",["$Remove$ a card", "from your deck", "$permanently$"],[20,60,2.5]],
    # ["./art/cards/misc/potionRareTemplate.png","Plating Pot","potion","./art/potions/plating.png",["Gain 2 $plating$", "$each combat$"],[20,60,2.5]],
    # ["./art/cards/misc/potionRareTemplate.png","Ritual Pot","potion","./art/potions/ritual.png",["Gain 1 $ritual$", "$this combat$"],[20,60,2.5]],
    # ["./art/cards/misc/potionRareTemplate.png","Refreshment","potion","./art/potions/fullHeal.png",["Fully $heal$"],[20,60,2.5]],
    # ["./art/cards/misc/potionRareTemplate.png","Reward Pot","potion","./art/potions/reward.png",["Pick from 5 cards", "Add 1 to deck","$permanently$"],[20,60,2.5]],

    #admin cards etc
    
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

def overlay_alpha(img: cv2.typing.MatLike, subimg: cv2.typing.MatLike, x:int, y:int):
    s = subimg.shape
    for a in range(0,s[0]):
        for b in range(0,s[1]):
            if subimg[a,b,3]>0.001:
                img[y+a,x+b]=subimg[a,b][0:3]

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

def placeCard(img:cv2.typing.MatLike, card: cv2.typing.MatLike,x:int,y:int,name:str,ctype:str,image:cv2.typing.MatLike,description:list[str],positioning:list):
    overlay(img,card,x,y)

    #image
    overlay_alpha(img,image,x+230+positioning[0],y+160+positioning[1])

    #name
    font = ImageFont.truetype("./misc/kreon.ttf",60)
    img = putTextPIL(img,name,(x+350-font.getmask(name).getbbox()[2]//2,y+70),60,(255,255,255),True,(0,0,0))

    #type
    font = ImageFont.truetype("./misc/kreon.ttf",38)
    img = putTextPIL(img,ctype,(x+350-font.getmask(ctype).getbbox()[2]//2,y+480),38,(255,255,255),True,(0,0,0))

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
        y += 70#bbox[3]+16

    return img

border = 60
negBorderX = 75
negBorderY = 140
x = border
y = border
offset = 2
blankPage = True

import os

for c in cards:
    card=cv2.imread(c[0])
    card=cv2.resize(card,None,fx=0.5,fy=0.5) #resize
    card=card[
        negBorderY:card.shape[0]-negBorderY,
        negBorderX:card.shape[1]-negBorderX,
    ] #crop

    A4image = placeCard(A4image,card,x,y,c[1],c[2],cv2.resize(cv2.imread(c[3],cv2.IMREAD_UNCHANGED),None,fx=c[5][2],fy=c[5][2]),c[4],c[5])

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
    cv2.imwrite("./testdata/specialCards"+str(i)+".png",A4pages[i])
#cv2.waitKey(0)
cv2.destroyAllWindows()