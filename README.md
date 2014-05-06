python-rpg
==========

A (supposedly) steampunk-themed, cross-platform RPG, where the player learns Python and uses it to solve problems and  progress in the game. Currently in very early phase.

##Prerequisities

###Python 2.7
https://www.python.org/

###Pygame
http://www.pygame.org/

For tutorial, see: http://programarcadegames.com/index.php?lang=en

###Tiled and PyTMX
This game uses Tiled as the map editor, that can be found at http://www.mapeditor.org/

To get started with Tiled, see http://gamedevelopment.tutsplus.com/tutorials/introduction-to-tiled-map-editor--gamedev-2838

The .tmx-format is handled using PyTMX library: https://github.com/bitcraft/PyTMX

##What's working so far
*Player can move around the map, pick up items and interact with surroundings*

*Levels support scrolling, obstacles, items and messages in form of signs.* 

*Switching between the levels is possible, travelling between the levels can be done via Tiled*

*Crude inventory menu*

*Rough switching between the game and the Python shell*

##What's next
*Interaction between the shell and the game, e.g. solving problems using coding*

*Adding NPCs to the levels*

*Map menu*

##Quick instructions

To run the game:
  *python main.py*

####Controls:
  *WASD - move*
  
  *I - open inventory*
  
  *T - switch to shell (to switch back, type 'exit' in shell)*
  
  *SPACE - interact (read signs, speak to NPC, etc.) with environment*
