import pygame

def drawTextOutlined(g,text,pos,outcol,incol):
    #background
    g.screen.blit(
        g.font.render(
            text,True,outcol
        ),
        (pos[0]-1,pos[1]-1)
    )
    g.screen.blit(
        g.font.render(
            text,True,outcol
        ),
        (pos[0]+1,pos[1]-1)
    )
    g.screen.blit(
        g.font.render(
            text,True,outcol
        ),
        (pos[0]+1,pos[1]+1)
    )
    g.screen.blit(
        g.font.render(
            text,True,outcol
        ),
        (pos[0]-1,pos[1]+1)
    )

    #foreground
    g.screen.blit(
        g.font.render(
            text,True,incol
        ),
        (pos[0],pos[1])
    )