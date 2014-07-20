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

    position=None #used for improved character movement (2-element float list)
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

        self.position=[0,0]     

        self.velocity=[0,0]
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
        old_pos=[round(self.position[0]),round(self.position[1])]
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]         

        self.rect_original.x = round(self.position[0])
        self.rect_original.y = round(self.position[1])

        self.rect=self.rect_original.copy()
        self.rect.x-=level.camera_position[0]
        self.rect.y-=level.camera_position[1]
        
        #check for collisions
        collision_list = pg.sprite.spritecollide(self, level.obstacles, False)
        for i in collision_list:
            collision_position=self.rect_original.copy()

            #test if moving the character back in the x-direction solves the collision. If so, stop the movement in the x-direction
            self.rect_original.x = old_pos[0]
            if not pg.Rect.colliderect(self.rect_original,i.rect_original):
                self.position[0] = old_pos[0]
                self.velocity[0]=0
            else:
                #test the same in the y-direction
                self.rect_original=collision_position.copy()
                self.rect_original.y=old_pos[1]                
                if not pg.Rect.colliderect(self.rect_original,i.rect_original):
                    self.position[1] = old_pos[1]
                    self.velocity[1]=0
                else:
                    #Otherwise move both
                    self.rect_original=collision_position.copy()
                    self.position[0] = old_pos[0]
                    self.position[1] = old_pos[1]
                    self.rect_original.x = old_pos[0]
                    self.rect_original.y = old_pos[1]
                    self.velocity=[0,0]

        collision_list = pg.sprite.spritecollide(self, level.character_list, False)
        for i in collision_list:
            if not i.name == self.name: 
                collision_position=self.rect_original.copy()

                #test if moving the character back in the x-direction solves the collision. If so, stop the movement in the x-direction
                self.rect_original.x = old_pos[0]

                if not pg.Rect.colliderect(self.rect_original,i.rect_original):
                    self.position[0] = old_pos[0]
                    self.velocity[0]=0
                else:
                    #test the same in the y-direction
                    self.rect_original=collision_position.copy()
                    self.rect_original.y=old_pos[1]
                    if not pg.Rect.colliderect(self.rect_original,i.rect_original):
                        self.position[1] = old_pos[1]
                        self.velocity[1]=0
                    else:
                        #Otherwise move both
                        self.rect_original=collision_position.copy()
                        self.position[0] = old_pos[0]
                        self.position[1] = old_pos[1]
                        self.rect_original.x = old_pos[0]
                        self.rect_original.y = old_pos[1]
                        self.velocity=[0,0]
        #Prevent the character going over the borders of the level
        if self.rect_original.x < 0:
            self.rect_original.x = 0
            self.position[0] = self.rect_original.x
        elif self.rect_original.right > level.level_size[0]: #The right side limit has to be taken from screen size!
            self.rect_original.right = level.level_size[0]             
            self.position[0] = self.rect_original.x
        if self.rect_original.y < 0:
            self.rect_original.y = 0
            self.position[1] = self.rect_original.y
        elif self.rect_original.bottom > level.level_size[1]:
            self.rect_original.bottom = level.level_size[1]            
            self.position[1] = self.rect_original.y
        
        self.rect=self.rect_original.copy()
        self.rect.x-=level.camera_position[0]
        self.rect.y-=level.camera_position[1]

    def start_moving(self, movement_key_order):
        '''Sets the velocity and the movement animation for the character.
        input: list of the directions the character is going
        output: none
        '''
        #TODO: get rid of the constants
        self.current_animation[0]='stand' #default if no movement(s)

        movement_direction=[0,0]
        for dir in movement_key_order:
            if dir == "LEFT":
                self.current_animation=["walk","left"]
                movement_direction[0] = -1 
            elif dir == "RIGHT":
                self.current_animation=["walk","right"]
                movement_direction[0] = 1
            if dir == "DOWN":
                self.current_animation=["walk","front"]
                movement_direction[1] = 1 
            elif dir == "UP":
                self.current_animation=["walk","back"]
                movement_direction[1] = -1 

        if movement_direction[0] and movement_direction[1]:
            #If the character is moving diagonally, normalize the components with 1/sqrt(2)
            #Doesn't function properly, because positions of sprites can't be altered by a fraction of a pixel.
            #Maybe fixed in the future

            speed=0.7071*self.MAX_SPEED
            self.velocity=[movement_direction[0]*speed,movement_direction[1]*speed]

            #self.velocity=[movement_direction[0]*self.MAX_SPEED,movement_direction[1]*self.MAX_SPEED]            
        else:
            self.velocity=[movement_direction[0]*self.MAX_SPEED,movement_direction[1]*self.MAX_SPEED]



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
        self.position=[0,0]
        
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
    start_x = None #initial position, to keep NPC in area
    start_y = None
    npc_leash = None #NPC leash length (in px)

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
        self.start_x = pos[0]
        self.start_y = pos[1]

        self.rect_original=self.rect.copy()
        self.position=[float(self.rect_original.x),float(self.rect_original.y)]    
    
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
        self.npc_leash = 150 #to keep NPC in area

    def update(self,level):
        '''The overloaded update method.
        input: current Level object
        output: none
        '''
        Character.update(self,level)       

        self.frame_counter += 1

        #Controls the random movement of the NPC
        if self.frame_counter == 5*60 and self.current_animation[0]=='stand':
            directions=['UP','DOWN','LEFT','RIGHT']
            # keep NPC in initial area
            if self.rect_original.x > self.start_x +self.npc_leash:
                self.start_moving(['LEFT'])
            elif self.rect_original.x < self.start_x -self.npc_leash:
                self.start_moving(['RIGHT'])
            elif self.rect_original.y > self.start_y +self.npc_leash:
                self.start_moving(['UP'])
            elif self.rect_original.y < self.start_y -self.npc_leash:
                self.start_moving(['DOWN'])
            else:
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
