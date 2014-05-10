import pygame as pg


#TODO: put the key bindings to a modifiable list
class Controls:
    '''Handles the movement of the character'''
    movement_key_order = []
    shell=None
    #I think this should work without much error handling
    def __init__(self,shell):
        self.shell=shell    

    def reset(self):
        self.movement_key_order = []
        
    def add_key(self,key):
        self.movement_key_order.append(key)
        
    def remove_key(self,key):
        try:
            self.movement_key_order.remove(key)
        except: #error is thrown if the list is empty
            pass
        
    def current_key(self):
        if len(self.movement_key_order) == 0:
            return "NONE"
        else:
            return self.movement_key_order[len(self.movement_key_order)-1] 
        
    def handle_key_event(self,event):
        '''Handles the key event, returns the key pressed before the new event'''
        old_key=self.current_key()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:          
                self.add_key("DOWN")
            elif event.key == pg.K_w:                
                self.add_key("UP")
            elif event.key == pg.K_a:                    
                self.add_key("LEFT")                 
            elif event.key == pg.K_d:                  
                self.add_key("RIGHT")
            elif event.key == pg.K_t:
                self.shell.interprator()
        elif event.type == pg.KEYUP:
            if event.key == pg.K_s:
                self.remove_key("DOWN")
            elif event.key == pg.K_w:
                self.remove_key("UP")             
            elif event.key == pg.K_a:
                self.remove_key("LEFT")              
            elif event.key == pg.K_d:
                self.remove_key("RIGHT")
        return old_key
    
    def is_movement_key(self,key):
        '''Checks if the key event is a movement key'''
        if key == pg.K_s or key == pg.K_a or key == pg.K_w or key == pg.K_d:
            return True
        else:
            return False
                
class MenuControls:
    '''Handles the menu navigation'''
    def handle_event(self,event):
        pass

    def check_open_menu(self,key):
        '''Checks if the pressed key opens a menu. If so, return the name of the menu to be opened, otherwise 0'''
        if key == pg.K_i:
            return "Inventory"
        elif key == pg.K_m:
            return "Map"
        else:
            return 0
