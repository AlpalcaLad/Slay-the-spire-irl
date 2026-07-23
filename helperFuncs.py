import pygame

def drawTextOutlined(g,text,pos,outcol,incol):
    offset = g.font.size("text")[0]

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