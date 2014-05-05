import pygame as pg
import pytmx
import os

class Obstacle(pg.sprite.Sprite):
    '''This class includes the coordinates (and possibly objects) that are impassable)'''
    def __init__(self,obstacle_object,tmx_map,cam_pos):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(obstacle_object.x,obstacle_object.y,obstacle_object.width,obstacle_object.height)
        self.image = tmx_map.getTileImageByGid(obstacle_object.gid)

        self.rect.x -= cam_pos[0]
        if self.image:
            self.rect.y -= cam_pos[1]+tmx_map.tileheight #Corrects the idiotic choice of origin in Tiled (for polygones top left corner as anticipated, but for images the bottom one...vittu mita paskaa)
        else:
            self.rect.y -= cam_pos[1]
        
class Item(pg.sprite.Sprite):
    properties = None
    '''This class includes the information of the items on the level'''
    def __init__(self,item,tmx_map,cam_pos):
        pg.sprite.Sprite.__init__(self)
        self.image = tmx_map.getTileImageByGid(item.gid)

        #Size of the item
        self.rect = self.image.get_rect()
        #Correct the position
        self.rect.x = item.x-cam_pos[0]
        self.rect.y = item.y-tmx_map.tileheight-cam_pos[1] #item.height corrects the stupid choice of origin in Tiled 

        self.properties=item.__dict__
        #cut off the extra crap
        for i in ['parent','height','width','gid','visible','y','x','rotation']:
            self.properties.pop(i)

class Level:
    '''Level superclass, not to be used directly'''
    tmx_map = None
    player = None
    character_list = None
    item_list = None
    camera_position=None
    obstacles=None
    controller=None
    sounds=None
    
    def __init__(self,player,map_name,ctrl,sounds):
        self.player = player
        self.controller = ctrl
        self.sounds = sounds
        self.character_list = pg.sprite.Group()
        self.character_list.add(self.player)
        
        #Load the map
        self.tmx_map = pytmx.load_pygame(os.path.join(os.path.dirname(__file__),map_name), pixelalpha=True)
        self.camera_position=[0,0]

        #get obstacles
        self.obstacles=pg.sprite.Group()
        for i in self.tmx_map.objectgroups[0]:
            self.obstacles.add(Obstacle(i,self.tmx_map,self.camera_position))

        #Get items in the level
        self.item_list=pg.sprite.Group()
        for i in self.tmx_map.objectgroups[1]:
            self.item_list.add(Item(i,self.tmx_map,self.camera_position))
            
    def update(self):
        """ Update everything in this level."""
        self.character_list.update(self)
        
        #update the position of the camera and items  
        map_width=self.tmx_map.width*self.tmx_map.tilewidth
        map_height=self.tmx_map.height*self.tmx_map.tileheight
      
        if (self.player.rect.x<200 and self.camera_position[0]+self.player.rect.x-200 >= 0) or (self.player.rect.right > 600 and self.camera_position[0]+self.player.rect.right+200<map_width): #The right side limit has to take from screen size!
            if self.player.rect.x<200:
                delta_x=self.player.rect.x-200
            else:
                delta_x=self.player.rect.right-600
            self.camera_position[0] += delta_x
            self.player.rect.x -= delta_x

            #update items and obstacles (TODO: A COMMON SPRITE GROUP FOR ALL THE OBJECTS IN THE LEVEL)
            sprites=self.item_list.sprites()         
            for i in sprites:
                i.rect.x -=delta_x
            sprites=self.obstacles.sprites()         
            for i in sprites:
                i.rect.x -=delta_x                
        if (self.player.rect.y<200 and self.camera_position[1]+self.player.rect.y-200 >= 0) or (self.player.rect.bottom > 400 and self.camera_position[1]+self.player.rect.bottom+200<map_height): #The right side limit has to take from screen size!
            if self.player.rect.y<200:
                delta_y=self.player.rect.y-200
            else:
                delta_y=self.player.rect.bottom-400
            self.camera_position[1] += delta_y
            self.player.rect.y -= delta_y
                
            #update items and obstacles (TODO: A COMMON SPRITE GROUP FOR ALL THE OBJECTS IN THE LEVEL)
            sprites=self.item_list.sprites()         
            for i in sprites:
                i.rect.y -=delta_y
            sprites=self.obstacles.sprites()         
            for i in sprites:
                i.rect.y -=delta_y    

        
    def draw(self, screen):
        """ Draw everything on this level. """
        #Draw background and foreground
        layer = self.tmx_map.getTileLayerByName("Background")#CHANGE THE CODE TO USE LAYER NAMES INSTEAD OF INDICES 
        for i in range(self.camera_position[0]//self.tmx_map.tilewidth,(screen.get_width()+self.camera_position[0])//self.tmx_map.tilewidth+1):
            for j in range(self.camera_position[1]//self.tmx_map.tileheight,(screen.get_height()+self.camera_position[1])//self.tmx_map.tileheight+1):
                image = self.tmx_map.getTileImage(i, j, 0)
                screen.blit(image, [i*self.tmx_map.tilewidth-self.camera_position[0],j*self.tmx_map.tileheight-self.camera_position[1]])
                image = self.tmx_map.getTileImage(i, j, 1)
                if not image == 0:
                    screen.blit(image, [i*self.tmx_map.tilewidth-self.camera_position[0],j*self.tmx_map.tileheight-self.camera_position[1]])                

        #Draw obstacles
        for i in self.obstacles:
            if not i.image == 0:
                screen.blit(i.image, [i.rect.x,i.rect.y])                
        
        # Draw all the sprite lists that we have
        self.item_list.draw(screen)
        self.character_list.draw(screen)
        
        #Draw the top layer
        for i in range(self.camera_position[0]//self.tmx_map.tilewidth,(screen.get_width()+self.camera_position[0])//self.tmx_map.tilewidth+1):
            for j in range(self.camera_position[1]//self.tmx_map.tileheight,(screen.get_height()+self.camera_position[1])//self.tmx_map.tileheight+1):
                image = self.tmx_map.getTileImage(i, j, 2)
                if not image == 0:
                    screen.blit(image, [i*self.tmx_map.tilewidth-self.camera_position[0],j*self.tmx_map.tileheight-self.camera_position[1]])
                    
    def handle_key(self,event):
            old_key=self.controller.handle_key_event(event)
            if event.type == pg.KEYDOWN:
                if old_key == "NONE" and self.controller.is_movement_key(event.key):
                    self.sounds.audio["walk"].play(-1)
                self.player.start_moving(self.controller.current_key())
            if event.type == pg.KEYUP:
                if(self.controller.current_key()=="NONE"):
                    self.player.stop_moving(old_key)
                    self.sounds.audio["walk"].stop()
                self.player.start_moving(self.controller.current_key())
                
    def passivate(self):
        '''To be used when changing to menus'''
        self.player.stop_moving(self.controller.current_key())
        self.sounds.audio["walk"].stop()  
        self.controller.reset()
      
class TestLevel(Level):
    
    def __init__(self,player,ctrl,sounds):
        Level.__init__(self,player,"test.tmx",ctrl,sounds)
        
class TestLevel2(Level):
    
    def __init__(self,player,ctrl,sounds):
        Level.__init__(self,player,"test2.tmx",ctrl,sounds)
