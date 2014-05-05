import pygame as pg
from characters.character import *
from levels.level import *
from menus.menu import *
import os
from interprator import *
from audio.audio import *

def main():
    #initialize PyGame
    pg.init()

    #Set up the screen
    size=(800,600)
    screen=pg.display.set_mode(size)
    
    pg.display.set_caption("Python RPG")
 

    #Create the player character
    player=Player()
    #Create controller object for player 
    ctrl=Controls()
    #Load audio
    sounds=Audio()
    #Load test level
    level=TestLevel2(player,ctrl,sounds)
    #Load test menu
    menu=Inventory(player)    
    
    
    #play bg music
    sounds.music["test"].set_volume(0.5)
    sounds.music["test"].play(-1)


    #Clock object for controlling the frame rate
    clock=pg.time.Clock()

    #Main loop controls
    quit=False
    current_scene = "level"
         
    #Main loop
    while not quit:
        #Process events after this
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit = True
            elif event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                if event.key == pg.K_i and event.type == pg.KEYDOWN: #TEMPORARY SOLUTION (separate menus and levels smarter)
                    if current_scene == "level":
                        current_scene = "menu"
                        level.passivate()
                    else: 
                        current_scene = "level"
                if current_scene == "level":
                    level.handle_key(event)
                else:
                    pass
                
        #All game logic after this
        if current_scene == "level":
            level.update()
        else:
            menu.update()
            
        #Screen updates after this
        if current_scene == "level":
            level.draw(screen)
        else:
            menu.draw(screen)
        
        pg.display.flip()
        
        #Frame limit
        clock.tick_busy_loop(60) #Works better than clock.tick()
    
    pg.quit()

if __name__=="__main__":
    main()