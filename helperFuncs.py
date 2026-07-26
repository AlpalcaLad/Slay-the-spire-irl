import pygame

def textMulti(g,textArray,cntr,backbox=True,adjustCenterHeight=False):
    """Draws multiple lines of text around a center"""
    fnts = []
    stats = []
    height = 0
    width = 0
    padding = 8

    #first pass build all the lines and measure them
    for t in textArray:
        fnt = g.eventFont.render(
            t, True, (255,255,255)
        )
        stat = fnt.get_rect()
        stats.append(stat)
        fnts.append(fnt)
        width = max(width,stat.width)
        height += stat.height+4

    if adjustCenterHeight:
        cntr=(cntr[0],cntr[1]-height//2)

    #draw backbox
    if backbox:
        pygame.draw.rect(g.screen,(40,40,40),(
                cntr[0]-width//2-padding,
                cntr[1]-height//2-padding,
                width+padding,
                height+padding
            ), 
        border_radius=8)

    #second pass draw all the lines in correct positions
    curY = cntr[1]-height/2
    for f,s in zip(fnts,stats):
        g.screen.blit(
            f,
            (cntr[0]-s.width//2,curY)
        )
        curY += s.height+4

def drawTextOutlined(g,text,pos,outcol,incol):
    offset = -g.font.size("text")[0]/2

    #background
    g.screen.blit(
        g.font.render(
            text,True,outcol
        ),
        (pos[0]-1+offset,pos[1]-1)
    )
    g.screen.blit(
        g.font.render(
            text,True,outcol
        ),
        (pos[0]+1+offset,pos[1]-1)
    )
    g.screen.blit(
        g.font.render(
            text,True,outcol
        ),
        (pos[0]+1+offset,pos[1]+1)
    )
    g.screen.blit(
        g.font.render(
            text,True,outcol
        ),
        (pos[0]-1+offset,pos[1]+1)
    )

    #foreground
    g.screen.blit(
        g.font.render(
            text,True,incol
        ),
        (pos[0]+offset,pos[1])
    )