import pygame as pg
import os
from controller import Controls 

class Character(pg.sprite.Sprite):
    name=None
    animations=None #contains all the animations
    animation_types=["stand","walk"]
    orientations = ["front","back","left","right"]    
    current_animation=None #should the facing direction be separated from this?
    animation_counter=None

    velocity=None
    
    def __init__(self,name):
        pg.sprite.Sprite.__init__(self)
        self.name=name
        self.animations={}        
        self.animation_counter=0
        self.velocity=[0,0]

        self.load_animations()
        self.current_animation=["stand","front"]
        self.image = self.animations[self.current_animation[0]][self.current_animation[1]][0]
        #Get the sprite boundaries
        self.rect = self.image.get_rect()
        
    def load_animations(self):
        '''Loads the animations stored in character/graphics/ as individual pictures with filename format name_animationtype_direction_framenumber.png'''
        ANIMATION_LENGTH=4
        for i in self.animation_types:
            self.animations[i]={}
            for j in self.orientations:
                self.animations[i][j]=[]
                for k in range(ANIMATION_LENGTH):
                    self.animations[i][j].append(pg.image.load(os.path.join(os.path.dirname(__file__),"graphics",self.name+"_"+i+"_"+j+"_"+str(k)+".png")).convert_alpha())
                    
    def update(self,level):
        #Change the frames of the animation
        self.animation_counter += 1
        if self.animation_counter == 40:
            self.animation_counter = 0
        self.image=self.animations[self.current_animation[0]][self.current_animation[1]][(4*self.animation_counter)//40]
        
        #Update the position
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]         
        
        #check for collisions
        collision_list = pg.sprite.spritecollide(self, level.obstacles, False)
        for i in collision_list:
            # If moving right, align the right side of the character to the left side of the object
            if self.velocity[0] > 0:
                self.rect.right = i.rect.left
            elif self.velocity[0] < 0:
                #The opposite
                self.rect.left = i.rect.right
            # Same for y-direction
            if self.velocity[1] > 0:
                self.rect.bottom = i.rect.top
            elif self.velocity[1] < 0:
                self.rect.top = i.rect.bottom            

        collision_list = pg.sprite.spritecollide(self, level.character_list, False)
        for i in collision_list:
            if not i.name == self.name: 
                # If moving right, align the right side of the character to the left side of the object
                if self.velocity[0] > 0:
                    self.rect.right = i.rect.left
                elif self.velocity[0] < 0:
                    #The opposite
                    self.rect.left = i.rect.right
                # Same for y-direction
                if self.velocity[1] > 0:
                    self.rect.bottom = i.rect.top
                elif self.velocity[1] < 0:
                    self.rect.top = i.rect.bottom            



    def start_moving(self,dir):
        #TODO: get rid of the constants
        if dir == "DOWN":
            self.velocity=[0,2]
            self.current_animation=["walk","front"] 
        elif dir == "UP":
            self.velocity=[0,-2]
            self.current_animation=["walk","back"]
        elif dir == "LEFT":
            self.velocity=[-2,0]
            self.current_animation=["walk","left"]
        elif dir == "RIGHT":
            self.velocity=[2,0]
            self.current_animation=["walk","right"]
            
    def stop_moving(self,dir):
        if dir == "DOWN" and self.velocity[1]>0:    
            self.velocity=[0,0]
            self.current_animation=["stand","front"]            
        elif dir == "UP" and self.velocity[1]<0:
            self.velocity=[0,0]
            self.current_animation=["stand","back"]   
        elif dir == "LEFT" and self.velocity[0]<0:
            self.velocity=[0,0]
            self.current_animation=["stand","left"] 
        elif dir == "RIGHT" and self.velocity[0]>0:
            self.velocity=[0,0]
            self.current_animation=["stand","right"] 

class Player(Character):
    inventory = None
    rect_interact=None #used for the interacting with the environment 
    def __init__(self):
        Character.__init__(self,"player")
        self.inventory = pg.sprite.Group()
        self.rect_interact=pg.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        
    def update(self,level):
        Character.update(self,level)
        #pick up items
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

    def __init__(self,name,texts,pos,cam_pos):
        Character.__init__(self,name)
        self.rect.x=pos[0]
        self.rect.y=pos[1]

        self.rect_original=self.rect.copy()    
    
        self.rect.x-=cam_pos[0]
        self.rect.y-=cam_pos[1]

        if not len(texts):
            self.speech_texts=["..."]
        else:
            self.speech_texts=texts

        self.text_index=len(self.speech_texts)-1 #Set to the last text, so the speak function return the first one at first call.

    def update(self,level):
        Character.update(self,level)

    def speak(self,direction='front'):
        self.text_index=(self.text_index+1)%len(self.speech_texts)
        #Change the facing direction 
        self.current_animation[1]=direction
        self.image=self.animations[self.current_animation[0]][self.current_animation[1]][(4*self.animation_counter)//40]

        return self.speech_texts[self.text_index]
