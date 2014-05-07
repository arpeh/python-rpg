import pygame as pg
import os

class TextSprite(pg.sprite.Sprite):
    def __init__(self,font,text,pos):
        pg.sprite.Sprite.__init__(self)
        self.image=font.render(text,True,[0,0,0])
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]

class Menu:
    '''This is the super class from which all the menus are derived'''
    bg_image=None
    menu_items=None
    texts=None
    rect=None
    
    def __init__(self,bg_filename):
        self.bg_image=pg.image.load(os.path.join(os.path.dirname(__file__),bg_filename)).convert_alpha()
        self.rect=self.bg_image.get_rect()
        #center menu
        self.rect.center=(400,300)
        
        #Init menu item list
        self.menu_items=pg.sprite.Group()
        
        #Init list of the rendered menu texts
        self.texts=pg.sprite.Group()
        
    def draw(self,screen):
        screen.blit(self.bg_image,[self.rect.x,self.rect.y])
        self.texts.draw(screen)
        
    def update(self):
        pass
        
class Inventory(Menu):
    player = None
    
    def __init__(self,player):
        Menu.__init__(self,'inventory.png')
        self.player = player
        self.description_font=pg.font.Font(None,25)
        
    def draw(self,screen):
        Menu.draw(self,screen)
        #Get the list of sprites
        sprite_list=self.player.inventory.sprites()

        #Changes the item positions for inventory screen
        for i in range(len(sprite_list)):
            sprite_list[i].rect.x=self.rect.x+25+34*(i%10)
            sprite_list[i].rect.y=self.rect.y+50+34*(i//10)
            
        self.player.inventory.draw(screen)
        self.texts.draw(screen)
        self.texts=pg.sprite.Group()
        
    def update(self):
        Menu.update(self)
        
        #check if the mouse is over an menu item
        mouse_position=pg.mouse.get_pos()
        sprite_list=self.player.inventory.sprites()
        for i in sprite_list:
            if mouse_position[0] >= i.rect.left and mouse_position[0] <= i.rect.right:
                if mouse_position[1] >= i.rect.top and mouse_position[1] <= i.rect.bottom:
                    self.texts.add(TextSprite(self.description_font,i.properties['name']+' ('+i.properties['type']+')',[self.rect.left+50,self.rect.bottom-50]))

class TextBox(Menu):
    '''The text box that opens at the bottom of the screen, when someone speaks or player reads a sign, et cetera.'''
    def __init__(self):
        Menu.__init__(self,'textbox.png')
        self.rect.bottom=550
        self.text_font=pg.font.Font(None,50)
        
    def set_text(self,text):
        self.texts.empty()
        self.texts.add(TextSprite(self.text_font,text,[self.rect.left+25,self.rect.top+25]))#TODO: support for multiline text
    
    def update(self):
        Menu.update(self) 

class Map(Menu):

    pointer=None
    pointer_rect=None
    level_positions=None
    current_level_name=None

    def __init__(self):
        Menu.__init__(self,'map.png')
	self.pointer=pg.image.load(os.path.join(os.path.dirname(__file__),'map_pointer.png')).convert_alpha()
	self.pointer_rect=self.pointer.get_rect()
        #set the coordinates of the levels on the map (TODO: load these from a file)
        self.level_positions={}
	self.level_positions['TestLevel']=(self.rect.x+230,self.rect.y+375)
	self.level_positions['TestLevel2']=(self.rect.x+290,self.rect.y+400)

    def update(self,level):
        Menu.update(self)
	self.current_level_name=level

    def draw(self,screen):
	Menu.draw(self,screen)
	self.pointer_rect.center=self.level_positions[self.current_level_name]
	screen.blit(self.pointer,[self.pointer_rect.x,self.pointer_rect.y]) 

