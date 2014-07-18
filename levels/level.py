import pygame as pg
import pytmx
import os
from characters.character import *

class Obstacle(pg.sprite.Sprite):
    '''This class includes the coordinates (and possibly objects) that are impassable.'''
    def __init__(self,obstacle_object,tmx_map,cam_pos):
        '''Init
        input: obstacle_object - PyTMX TiledObject
               tmx_map - PyTMX TiledMap
               cam_pos - 2-element float list
        output: none
        '''
        pg.sprite.Sprite.__init__(self)

        #Get the sprite of the obstacle (if none, None is returned)
        self.image = tmx_map.getTileImageByGid(obstacle_object.gid)

        if self.image:
            #If the object has a sprite, take its size
            self.rect = self.image.get_rect() 
            self.rect.x=obstacle_object.x
            self.rect.y=obstacle_object.y
        else:
            #Otherwise, use the dimensions of the defined rectangle
            self.rect = pg.Rect(obstacle_object.x,obstacle_object.y,obstacle_object.width,obstacle_object.height)

        self.rect_original=self.rect.copy() #Stores the object's original position

        #set the position on the screen
        self.rect.x -= cam_pos[0]
        if self.image:
            self.rect_original.y -= tmx_map.tileheight #Corrects the idiotic choice of origin in Tiled (for polygons top left corner as anticipated, but for images the bottom one...vittu mita paskaa)
            self.rect.y -= cam_pos[1]+tmx_map.tileheight 
        else:
            self.rect.y -= cam_pos[1]
        
class Item(pg.sprite.Sprite):
    properties = None
    '''This class includes the information of the items on the level'''
    def __init__(self,item,tmx_map,cam_pos):
        '''Init
        input: item - PyTMX TiledObject
               tmx_map - PyTMX TiledMap
               cam_pos - 2-element float list
        output: none
        '''
        #Get the item sprite
        pg.sprite.Sprite.__init__(self)
        self.image = tmx_map.getTileImageByGid(item.gid)

        #Size and position of the item
        self.rect = self.image.get_rect()

        #Store the original position
        self.rect_original=self.rect.copy()    
        self.rect_original.x=item.x
        self.rect_original.y=item.y-tmx_map.tileheight #item.height corrects the stupid choice of origin in Tiled

        #Set the position on the screen
        self.rect.x = item.x-cam_pos[0]
        self.rect.y = item.y-tmx_map.tileheight-cam_pos[1]  

        #Get the dictionary of the object properties
        self.properties=item.__dict__
        #cut off the extra crap
        for i in ['parent','height','width','gid','visible','y','x','rotation']:
            self.properties.pop(i)

class LevelChanger(pg.sprite.Sprite):
    '''This class includes the objects that change the level upon contact with the player'''
    next_level_name = None
    def __init__(self,changer,tmx_map,cam_pos):
        '''Init
        input: changer - PyTMX TiledObject
               tmx_map - PyTMX TiledMap
               cam_pos - 2-element float list
        output: none
        '''
        pg.sprite.Sprite.__init__(self)
        #Get the level changer's dimensions
        self.rect = pg.Rect(changer.x,changer.y,changer.width,changer.height)
        #store the original position
        self.rect_original=self.rect.copy()
        
        #Set the position on the screen
        self.rect.x -= cam_pos[0]
        self.rect.y -= cam_pos[1]

        #The name of the level the changer changes to
        self.next_level_name=changer.name
        
class Event(pg.sprite.Sprite):
    '''This class includes the events such as messages in the level'''
    properties = None
   
    def __init__(self,event,tmx_map,cam_pos):
        '''Init
        input: event - PyTMX TiledObject
               tmx_map - PyTMX TiledMap
               cam_pos - 2-element float list
        output: none
        '''
        pg.sprite.Sprite.__init__(self)

        #Get the position of the event
        self.rect = pg.Rect(event.x,event.y,event.width,event.height)

        #store the original position
        self.rect_original=self.rect.copy()
 
        #Set the position on the screen       
        self.rect.x -= cam_pos[0]
        self.rect.y -= cam_pos[1]

        #Get the dictionary of the object properties
        self.properties=event.__dict__
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
    level_changers=None
    controller=None
    sounds=None
    has_level_just_changed=None
    events_interactable=None
    scroll_rect = None
    screen_size = None
    level_size = None
    
    def __init__(self,player,map_name,ctrl,sounds):
        '''Init
        input: player - Player object
               map_name - .tmx-map filename string
               ctrl - Controller object
               sounds - Audio object
        output: none
        '''
        self.player = player
        self.controller = ctrl
        self.sounds = sounds
        self.character_list = pg.sprite.Group()
        self.character_list.add(self.player)
        self.has_level_just_changed=True
    	#TODO: Take these values from actual screen size!
    	self.screen_size = (800,600)
    	self.scroll_rect = pg.Rect(200,200,400,200)
        
        #Load the map
        self.tmx_map = pytmx.load_pygame(os.path.join(os.path.dirname(__file__),map_name), pixelalpha=True)
        self.level_size=[self.tmx_map.width*self.tmx_map.tilewidth,self.tmx_map.height*self.tmx_map.tileheight]
        self.camera_position=[0,0]

        #get obstacles
        self.obstacles=pg.sprite.Group()
        for i in self.tmx_map.objectgroups[0]:
            self.obstacles.add(Obstacle(i,self.tmx_map,self.camera_position))

        #Get items in the level
        self.item_list=pg.sprite.Group()
        for i in self.tmx_map.objectgroups[1]:
            self.item_list.add(Item(i,self.tmx_map,self.camera_position))

        #Get the level changers
        self.level_changers=pg.sprite.Group()
        for i in self.tmx_map.objectgroups[2]:
            self.level_changers.add(LevelChanger(i,self.tmx_map,self.camera_position))

        #Get interactable events (TODO: generalize to all events)
        self.events_interactable=pg.sprite.Group()
        for i in self.tmx_map.objectgroups[3]:
            new_event=Event(i,self.tmx_map,self.camera_position)
            if(new_event.properties['type']=='interact'):
                self.events_interactable.add(new_event)           

        #Get the characters
        for i in self.tmx_map.objectgroups[4]:
            texts=[]
            for j in i.__dict__:
                if j[0:len(j)-1]=="text":
                    texts.append(i.__dict__[j])
            self.character_list.add(NPC(i.name,texts,[i.x,i.y],self.camera_position))
                       
            
    def update(self):
        ''' Update everything in this level.
        input: none
        output: none
        '''
        self.character_list.update(self)
        
        #update the position of the camera and items  
        if (self.player.rect.x<self.scroll_rect.left and self.camera_position[0]+self.player.rect.x-self.scroll_rect.left >= 0) or \
	(self.player.rect.right > self.scroll_rect.right and self.camera_position[0]+self.player.rect.right+ \
	self.screen_size[0]-self.scroll_rect.right<self.level_size[0]): 
            if self.player.rect.x<self.scroll_rect.left:
                delta_x=self.player.rect.x-self.scroll_rect.left
            else:
                delta_x=self.player.rect.right-self.scroll_rect.right
            self.camera_position[0] += delta_x
            self.player.rect.x -= delta_x

          
        if (self.player.rect.y<self.scroll_rect.top and self.camera_position[1]+self.player.rect.y-self.scroll_rect.top >= 0) or \
 	(self.player.rect.bottom > self.scroll_rect.bottom and self.camera_position[1]+\
	self.player.rect.bottom+self.screen_size[1]-self.scroll_rect.bottom<self.level_size[1]): 
            if self.player.rect.y<self.scroll_rect.top:
                delta_y=self.player.rect.y-self.scroll_rect.top
            else:
                delta_y=self.player.rect.bottom-self.scroll_rect.bottom
            self.camera_position[1] += delta_y
            self.player.rect.y -= delta_y

        #update items and obstacles (TODO: A COMMON SPRITE GROUP FOR ALL THE OBJECTS IN THE LEVEL, maybe separate x and y also)
        sprites=self.item_list.sprites()         
        for i in sprites:
            i.rect.x = i.rect_original.x-self.camera_position[0]
            i.rect.y = i.rect_original.y-self.camera_position[1]
        sprites=self.obstacles.sprites()         
        for i in sprites:
            i.rect.x = i.rect_original.x-self.camera_position[0]
            i.rect.y = i.rect_original.y-self.camera_position[1]
        sprites=self.level_changers.sprites()         
        for i in sprites:
            i.rect.x = i.rect_original.x-self.camera_position[0]
            i.rect.y = i.rect_original.y-self.camera_position[1]   
        sprites=self.events_interactable.sprites()         
        for i in sprites:
            i.rect.x = i.rect_original.x-self.camera_position[0]
            i.rect.y = i.rect_original.y-self.camera_position[1]            
        sprites=self.character_list.sprites()    
        for i in sprites:
            if not i.name == 'player':      
                i.rect.x = i.rect_original.x-self.camera_position[0]
                i.rect.y = i.rect_original.y-self.camera_position[1]
        
    def draw(self, screen):
        """ Draw everything on this level on the screen.
        input: screen - PyGame surface object
        output: none 
        """
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
        '''Handles the key events.
        input: key event
        output: none
        '''
        old_key=self.controller.handle_key_event(event)
        if event.type == pg.KEYDOWN:
            if old_key == "NONE" and self.controller.is_movement_key(event.key):
                self.sounds.audio["walk"].play(-1)
            self.player.start_moving(self.controller.current_key())
        if event.type == pg.KEYUP:
            if(self.controller.current_key()=="NONE"):
                self.player.stop_moving()
                self.sounds.audio["walk"].stop()
            self.player.start_moving(self.controller.current_key())
                
    def passivate(self):
        '''To be used when changing to menus
        input: none
        output: none
        '''
        self.player.stop_moving()
        self.sounds.audio["walk"].stop()  
        self.controller.reset()

    def check_if_change_level(self):
        '''Should return the name of the next level if true, 0 otherwise'''
        next_level=pg.sprite.spritecollide(self.player,self.level_changers,False)
        #has_level_just_changed prevents the repeated changing of the levels (as the level starts at the level changer)
        if len(next_level):
            if self.has_level_just_changed:
                return 0
            else:
                return next_level[0].next_level_name
        else:
            self.has_level_just_changed=False
            return 0
        
    def change_to_this_level(self,old_level_name):
        '''Called when switching to this level.
        input: name of level switched from 
        output: none
        '''
        self.has_level_just_changed=True

        #Move the player to the level changer corresponding to the old level
        self.player.rect_original.x=0
        self.player.rect_original.y=0
        for i in self.level_changers.sprites():
            if i.next_level_name==old_level_name:
                self.player.rect_original.x=i.rect_original.x
                self.player.rect_original.y=i.rect_original.y
                break

        self.player.rect=self.player.rect_original.copy()
        
        #adjust camera position (not sure, but center might cause trouble in the future if the player sprite is of even width/height)
        self.camera_position=[self.player.rect_original.center[0]-self.screen_size[0]//2,self.player.rect_original.center[1]-self.screen_size[1]//2] 
	
	#If centering camera takes the screen outside the level, fix it:
        if self.camera_position[0]<0:
            self.camera_position[0]=0
	elif self.camera_position[0]>self.level_size[0]-self.screen_size[0]-1:
            self.camera_position[0]=self.level_size[0]-self.screen_size[0]-1

        if self.camera_position[1]<0:
	    self.camera_position[1]=0
	elif self.camera_position[1]>self.level_size[1]-self.screen_size[1]-1:
	    self.camera_position[1]=self.level_size[1]-self.screen_size[1]-1	    
	    
        self.update()

    def player_interact(self,textbox):
        '''Check the interaction between the player and level
        input: TextBox object
        output: True if a message is evoked, False otherwise'''
        for i in self.events_interactable:
            if i.rect.colliderect(self.player.rect_interact) and i.properties['name']=='message': #SUPPORTS NOW ONLY MESSAGE EVENTS
                textbox.set_text(i.properties['value'])
                return True
        for i in self.character_list:
            if (not i.name == 'player') and i.rect.colliderect(self.player.rect_interact): #SUPPORTS NOW ONLY MESSAGE EVENTS
                #Get the NPC orientation from the player's
                if self.player.current_animation[1]=='front':
                    orientation='back'
                elif self.player.current_animation[1]=='left':
                    orientation='right'
                elif self.player.current_animation[1]=='right':
                    orientation='left'
                else:
                    orientation='front'
                textbox.set_text(i.speak(orientation))
                return True
        return False

    def run_code(self,codereader,textbox):
        '''Run CodeReader objects run_code() method
        input: codereader - CodeReader object
               textbox - TextBox object
        output: True if a message is evoked, False otherwise'''

        msg = None
        for i in self.character_list:
            if (not i.name == 'player') and i.rect.colliderect(self.player.rect_interact):
                obj_dict = {}
                obj_dict[i.name] = i 
                msg=codereader.run_code(obj_dict)
                break
        
        if msg:
            textbox.set_text(msg)
            return True
        else:
            return False
    

class levelInit():

    level = {}
    current_level = 'TestLevel'

    def __init__(self, player, ctrl, sounds):
        '''Init - Initialize levels
        input: player - Player object
               ctrl - Controller object
               sounds - Audio object
        output: none
        '''

        self.level['TestLevel'] = Level(player, os.path.join(os.path.dirname(__file__),'data',"test.tmx"), ctrl, sounds)
        self.level['TestLevel2'] = Level(player, os.path.join(os.path.dirname(__file__),'data', "test2.tmx"), ctrl, sounds)
        self.level['TestLevel3'] = Level(player, os.path.join(os.path.dirname(__file__),'data', "test3.tmx"), ctrl, sounds)
        self.level['TestTownLevel'] = Level(player, os.path.join(os.path.dirname(__file__),'data', "testtown.tmx"), ctrl, sounds)

