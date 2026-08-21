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

import numpy as np
#SRC: https://stackoverflow.com/questions/10261440/how-can-i-make-a-greyscale-copy-of-a-surface-in-pygame
def greyscale(surface: pygame.Surface):
    arr = pygame.surfarray.array3d(surface)
    # calulates the avg of the "rgb" values, this reduces the dim by 1
    mean_arr = np.mean(arr, axis=2)
    # restores the dimension from 2 to 3
    mean_arr3d = mean_arr[..., np.newaxis]
    # repeat the avg value obtained before over the axis 2
    new_arr = np.repeat(mean_arr3d[:, :, :], 3, axis=2)
    # return the new surface
    return pygame.surfarray.make_surface(new_arr)


def lerp(val1,val2,am):
    return val1 + (val2-val1)*am

def secondsToTime(s): return f"{int(s/3600)}h {int(s/60)-60*int(s/3600)}m {int(s)-60*int(s/60)}s"