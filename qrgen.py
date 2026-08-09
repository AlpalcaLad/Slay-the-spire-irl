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
    #     set 2
    "strikeB1",
    "strikeB2",
    "strikeB3",
    "strikeB4",
    "defendB1",
    "defendB2",
    "defendB3",
    "defendB4",
    #     set 3
    "strikeC1",
    "strikeC2",
    "strikeC3",
    "strikeC4",
    "defendC1",
    "defendC2",
    "defendC3",
    "defendC4",
    #admin
    "endturn",
    "reset",
    "killall",
    "remove",
    "togglepvp",
    #cocktail mixer cards
    "clearstrng2",
    "lemonup2",
    "downhat2",
    "bumpflv2",
    "seesun2",
    "redmoon2",
    "schnapp2",
    "bluemoon2",
    "rumaway2",
    "wallop2",
    "spinbot2",
    "roulette2",
    "ridebus2",
    "tastetest2",
    "keyingred2",
    "sealappr2",
    "keepitfl2",
    "getstartA2",
    "getstartB2",
    #designated driver cards
    "supplybag4",
    "notforme4",
    "carry4",
    "hitnrun4",
    "goodstuff4",
    "raidtrunk4",
    "responsible4",
    "offerlift4",
    "cherrypck4",
    "soberfoc4",
    "wakeup4",
    "linestom4",
    "checkin4",
    "maybeoneA4",
    "maybeoneB4",
    "rulesbroke4",
    "believeA4",
    "believeB4",
    "freshenup4",
    #beermaster cards
    "alcrage1",
    "coronaA1",
    "coronaB1",
    "brewdog1",
    "inchsA1",
    "inchsB1",
    "peroni1",
    "relaxing1",
    "ontap1",
    "catchupA1",
    "catchupB1",
    "chug1",
    "snakebite1",
    "wingman1",
    "beerjack1",
    "ringfire1",
    "splitg1",
    "hellsraise1",
    "tackychun1",
    "finisher1",
    #wine connosieur cards
    "grapetime3",
    "fruitarom3",
    "grape3",
    "royalgam3",
    "snobbery3",
    "vinyard3",
    "grapevin3",
    "bottleup3",
    "grapedan3",
    "cheesebrd3",
    "floralarom3",
    "herbalarom3",
    "minerarom3",
    "pourheart3",
    "onemoreg3",
    "sommelierA3",
    "sommelierB3",
    "grapetrap3",
    "grapeshot3",
    "bottlesmk3",
    #misc cards
    #enemies
    #    bosses
    "boss",
    #    elites
    "lagavulin",
    "gianthead",
    "terroreel",
    "skulkcol",
    "byrdonis",
    #    regular
    "nibbit",
    "cultistA",
    "cultistB",
    "cultistC",
    "slaverA",
    "slaverB",
    "slaverC",
    "thiefA",
    "thiefB",
    "orbwalker",
    "vineshamb",
    "fossilstlk",
    "frogknight",
    "leafslime",
    "mawler",
    #events
    "pubquiz",
    "a1",
    "a2",
    "a3",
    "a4",
    #potions
    "potWeak",
    "potStrength",
    "potDraw",
    "potVuln",
    "potTipsy",
    "potSafe",
    "potEnergy",
    "potExhaust",
    "potDamage",
    "potRMaxHP",
    "potRStrength",
    "PotRDamage",
    "potRScore",
    "potRStun",
    "potRRemove"
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
    if x > 3508 - border - imToOverlay.shape[0]:
        x = border
        y += imToOverlay.shape[1]+offset
        if y > 2480 - border - imToOverlay.shape[1]:
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

# pdfPath = "./testdata/QRcodes.pdf"
# from PIL import Image
# images = []

for i in range(len(A4pages)):
    cv2.imwrite("./testdata/QRcodes"+str(i)+".png",A4pages[i])
    # cv2.imwrite("./testdata/QRcodes"+str(i)+".png",cv2.rotate(A4pages[i],cv2.ROTATE_90_CLOCKWISE))
    # images.append(Image.open("./testdata/QRcodes"+str(i)+".png"))
#cv2.waitKey(0)
cv2.destroyAllWindows()

# images[0].save(
#     pdfPath, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
# )