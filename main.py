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
    #Load test levels (TODO: wrap levels and menus into a single class)
    level={}
    level['TestLevel']=TestLevel(player,ctrl,sounds)
    level['TestLevel2']=TestLevel2(player,ctrl,sounds)
    current_level = 'TestLevel'
    #Load test menu
    menu={}
    menu['Inventory']=Inventory(player)
    menu['TextBox']=TextBox() 
    current_menu = 'Inventory'
    
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
                if event.key == pg.K_i and event.type == pg.KEYDOWN: #TEMPORARY SOLUTION (separate menus and levels smarter and generalize)
                    if current_scene == "level":
                        current_scene = "menu"
                        current_menu = "Inventory"
                        level[current_level].passivate()
                    elif current_menu == "Inventory":  
                        current_scene = "level"
                        
                if event.key == pg.K_SPACE and event.type == pg.KEYDOWN: #TEMPORARY SOLUTION (incorporate to player controller)
                    if current_scene == "level":
                        is_msg=level[current_level].player_interact(menu["TextBox"])
                        if is_msg:
                            current_scene = "menu"
                            current_menu = "TextBox"
                            level[current_level].passivate()
                    elif current_menu == "TextBox": 
                        current_scene = "level"                
                if current_scene == "level":
                    level[current_level].handle_key(event)
                else:
                    pass
                
        #All game logic after this
        if current_scene == "level":
            level[current_level].update()
        else:
            menu[current_menu].update()

        next_level=level[current_level].check_if_change_level()
        if next_level:
            level[next_level].change_to_this_level(current_level)
            current_level=next_level
            
        #Screen updates after this
        if current_scene == "level":
            level[current_level].draw(screen)
        else:
            menu[current_menu].draw(screen)
        
        pg.display.flip()
        
        #Frame limit
        clock.tick_busy_loop(60) #Works better than clock.tick()
    
    pg.quit()

if __name__=="__main__":
    main()
