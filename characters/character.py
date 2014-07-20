import pygame as pg
import os
from controller import Controls 
import random

class Character(pg.sprite.Sprite):
    '''Superclass for every character in the game (not to be used directly)
    '''
    name=None
    animations=None #contains all the animations

    #The possible animation types and facing directions 
    animation_types=["stand","walk"]
    orientations = ["front","back","left","right"]
    
    '''current_animation is a string list of length of 2, with the first element being the
    type of animation and the second one is the facing direction.
    '''
    current_animation=None #(should the facing direction be separated from this?)
    animation_counter=None #current frame of the animation 
    ANIMATION_LENGTH=4 #TODO: generalize

    #This contains the coordinates of the character respect to the level (self.rect for screen)
    rect_original=None    

    velocity=None #float list with 2 entries, the first is the x-velocity and the second is the y-velocity
    MAX_SPEED=None
        
    def __init__(self,name):
        '''Init
        input: the string containing the name of the character
        output: none
        '''
        pg.sprite.Sprite.__init__(self)
        self.name=name
        self.animations={}        
        self.animation_counter=0
        self.velocity=[0,0]
        self.moveX=0
        self.moveY=0
        self.MAX_SPEED=2.0

        self.load_animations()
        self.current_animation=["stand","front"] #the beginning animation
        self.image = self.animations[self.current_animation[0]][self.current_animation[1]][0]
        #Get the sprite boundaries
        self.rect = self.image.get_rect()
        self.rect_original=self.rect.copy()    
        
    def load_animations(self):
        '''Loads the animations stored in character/graphics/ as individual pictures with filename format name_animationtype_direction_framenumber.png
        input: none
        output: none
        '''
        for i in self.animation_types:
            self.animations[i]={}
            for j in self.orientations:
                self.animations[i][j]=[]
                for k in range(self.ANIMATION_LENGTH):
                    self.animations[i][j].append(pg.image.load(os.path.join(os.path.dirname(__file__),"graphics",self.name+"_"+i+"_"+j+"_"+str(k)+".png")).convert_alpha())
                    
    def update(self,level):
        '''Called every frame updating the properties of the character
        input: Level object of the current level
        output: none
        '''

        #Change the frames of the animation
        self.animation_counter += 1
        if self.animation_counter == 40: #TODO: generalize
            self.animation_counter = 0
        self.image=self.animations[self.current_animation[0]][self.current_animation[1]][(4*self.animation_counter)//40]
        
        #Update the position
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]         

        self.rect_original.x += self.velocity[0]
        self.rect_original.y += self.velocity[1]  
        
        #check for collisions
        collision_list = pg.sprite.spritecollide(self, level.obstacles, False)
        for i in collision_list:
            # Stop moving the player when collision with the object
            if self.velocity[0] > 0:
                self.rect_original.x -= self.velocity[0]
                self.velocity[0] = 0
            elif self.velocity[0] < 0:
                #The opposite
                self.rect_original.x -= self.velocity[0]
                self.velocity[0] = 0
            # Same for y-direction
            if self.velocity[1] > 0:
                self.rect_original.y -= self.velocity[1]
                self.velocity[1] = 0
            elif self.velocity[1] < 0:
                self.rect_original.y -= self.velocity[1]
                self.velocity[1] = 0
                

        collision_list = pg.sprite.spritecollide(self, level.character_list, False)
        for i in collision_list:
            if not i.name == self.name: 
                # Stop moving the player when collision with the character
                if self.velocity[0] > 0:
                    self.rect_original.x -= self.velocity[0]
                    self.velocity[0] = 0
                elif self.velocity[0] < 0:
                    #The opposite
                    self.rect_original.x -= self.velocity[0]
                    self.velocity[0] = 0
                # Same for y-direction
                if self.velocity[1] > 0:
                    self.rect_original.y -= self.velocity[1]
		    self.velocity[1] = 0
                elif self.velocity[1] < 0:
                    self.rect_original.y -= self.velocity[1]
		    self.velocity[1] = 0

        #Prevent the character going over the borders of the level
        if self.rect_original.x < 0:
            self.rect_original.x = 0
        elif self.rect_original.right > level.level_size[0]: #The right side limit has to be taken from screen size!
                self.rect_original.right = level.level_size[0]             
        if self.rect_original.y < 0:
            self.rect_original.y = 0
        elif self.rect_original.bottom > level.level_size[1]:
            self.rect_original.bottom = level.level_size[1]            

        self.rect=self.rect_original.copy()
        self.rect.x-=level.camera_position[0]
        self.rect.y-=level.camera_position[1]


    def start_moving(self, movement_key_order):
        '''Sets the velocity and the movement animation for the character.
        input: list of the directions the character is going
        output: none
        '''
        #TODO: get rid of the constants
        self.moveX = 0
        self.moveY = 0
        self.current_animation[0]='stand' #default if no movement(s)
        for dir in movement_key_order:
            if dir == "DOWN":
                self.current_animation=["walk","front"]
                self.moveY = self.MAX_SPEED
            elif dir == "UP":
                self.current_animation=["walk","back"]
                self.moveY = -self.MAX_SPEED
            if dir == "LEFT":
                self.current_animation=["walk","left"]
                self.moveX = -self.MAX_SPEED
            elif dir == "RIGHT":
                self.current_animation=["walk","right"]
                self.moveX = self.MAX_SPEED
	self.velocity=[self.moveX, self.moveY] #apply direction to move
            
    def stop_moving(self):
        '''Stops the movement of the character.
        input: none
        output: none
        '''
        self.velocity=[0,0]
        self.current_animation[0]='stand'

    def convert_direction(self,dir):
        '''Converts a facing direction to walking direction and vice versa.
        input: string
        output: string, or None if invalid input
        '''  
        if dir == 'DOWN':
            return 'front'
        elif dir == 'UP':
            return 'back'
        elif dir == 'LEFT':
            return 'left'
        elif dir == 'RIGHT':
            return 'right'

        elif dir == 'front':
            return 'DOWN'
        elif dir == 'back':
            return 'UP'
        elif dir == 'right':
            return 'RIGHT'
        elif dir == 'left':
            return 'LEFT'
        else:
            return None

class Player(Character):
    '''The main character class'''
    inventory = None
    rect_interact=None #rectangle pointing to the facing direction, used for the interacting with the environment
    
    def __init__(self):
        Character.__init__(self,"player")
        self.inventory = pg.sprite.Group()
        self.rect_interact=pg.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        
    def update(self,level):
        '''The overloaded update method.
        input: current Level object
        output: none
        '''
        Character.update(self,level)
        
        #pick up items on collision
        picked_items = pg.sprite.spritecollide(self, level.item_list, True)
        if len(picked_items):
            level.sounds.audio['grab'].play()
            for i in picked_items:
                self.inventory.add(i)
                
        #update the position of the interaction rectangle according to the player's facing direction
        if(self.current_animation[1]=='front'):
            self.rect_interact.center=(self.rect.center[0],self.rect.bottom)
            self.rect_interact.top=self.rect.bottom
        elif(self.current_animation[1]=='back'):
            self.rect_interact.center=(self.rect.center[0],self.rect.top)
            self.rect_interact.bottom=self.rect.top
        elif(self.current_animation[1]=='left'):
            self.rect_interact.center=(self.rect.center[0],self.rect.center[1])
            self.rect_interact.right=self.rect.left               
        elif(self.current_animation[1]=='right'):
            self.rect_interact.center=(self.rect.center[0],self.rect.center[1])
            self.rect_interact.left=self.rect.right

class NPC(Character):
    speech_texts = None
    text_index= None
    frame_counter = None #for NPC movement

    def __init__(self,name,texts,pos,cam_pos):
        '''Init
        input: name - string of the name of the NPC
               texts - list of strings containting the speech of the NPC
               pos - 2-element float list of the initial position
               cam_pos - 2-element float list of the position of the camera
        output: none
        '''
        Character.__init__(self,name)
        self.rect.x=pos[0]
        self.rect.y=pos[1]

        self.rect_original=self.rect.copy()    
    
        self.rect.x-=cam_pos[0]
        self.rect.y-=cam_pos[1]

        #if no specific lines are given, the NPC says '...' when spoken to
        if not len(texts):
            self.speech_texts=["..."]
        else:
            self.speech_texts=texts

        #Set to the last text, so the speak function returns the first one at first call.
        self.text_index=len(self.speech_texts)-1 

        self.MAX_SPEED=1
        self.frame_counter = random.randint(0, 200) #randomize NPC movement start time

    def update(self,level):
        '''The overloaded update method.
        input: current Level object
        output: none
        '''
        Character.update(self,level)       

        self.frame_counter += 1

        #Controls the random movement of the NPC
        if self.frame_counter == 5*60 and self.current_animation[0]=='stand':
            print "npc liikkuu"
            directions=['UP','DOWN','LEFT','RIGHT']
            self.start_moving([ directions[random.randrange(len(directions))] ]) #need to be list
            self.frame_counter=0
        elif self.frame_counter == 60 and self.current_animation[0]=='walk': #TODO: This is rather stupid atm, fix
            self.stop_moving()
            self.frame_counter=0        



    def speak(self,direction='front'):
        '''Reaction of the NPC when spoken to
        input: string of direction the NPC turns to
        output: string of speech
        '''        
        self.text_index=(self.text_index+1)%len(self.speech_texts)
        #Change the facing direction 
        self.current_animation[1]=direction
        self.image=self.animations[self.current_animation[0]][self.current_animation[1]][(4*self.animation_counter)//40]
        self.stop_moving()
        return self.speech_texts[self.text_index]
