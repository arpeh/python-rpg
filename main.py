import pygame as pg
from characters.character import *
from levels.level import *
from menus.menu import *
import os
from interprator import *
from audio.audio import *
from controller import * 

def main():
    #initialize PyGame
    pg.init()

    #Set up the screen
    size=(800,600)
    screen=pg.display.set_mode(size)
    
    pg.display.set_caption("Python RPG")
 
    #Create the player character
    player=Player()
    #Create shell class
    shell=Interprator()
    #Create controller objects for player and menus
    ctrl=Controls(shell)
    menu_ctrl=MenuControls()
    #Load audio
    sounds=Audio()
    #Load test levels (TODO: wrap levels and menus into a single class)
    level={}
    level['TestLevel']=TestLevel(player,ctrl,sounds)
    level['TestLevel2']=TestLevel2(player,ctrl,sounds)
    current_level = 'TestLevel'
    #Load test menus
    menu={}
    menu['Inventory']=Inventory(player,shell)
    menu['TextBox']=TextBox() 
    menu['Map']=Map() 

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
                #Check whether any of the menu keys is pressed
                if event.type == pg.KEYDOWN:
                    menu_name=menu_ctrl.check_open_menu(event.key)
                    if menu_name:
                        if current_scene == "level":
                            current_scene = "menu"
                            current_menu = menu_name
                            level[current_level].passivate()
                        elif current_menu == menu_name:
                            menu[current_menu].on_close()  
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
            elif event.type == pg.MOUSEBUTTONDOWN:
                if current_scene == "level":
                    pass
                else:
                    menu[current_menu].handle_mouse_click(event)        
        #All game logic after this
        if current_scene == "level":
            level[current_level].update()
        else:
            if current_menu == "Map":
                menu[current_menu].update(current_level)
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
            level[current_level].draw(screen)
            menu[current_menu].draw(screen)
        
        pg.display.flip()
        
        #Frame limit
        clock.tick_busy_loop(60) #Works better than clock.tick()
    
    pg.quit()

if __name__=="__main__":
    main()
