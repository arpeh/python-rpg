python-rpg
==========

A (supposedly) steampunk-themed, cross-platform RPG, where the player learns Python and uses it to solve problems and  progress in the game.

##Prerequisities

###Python 2.7

###Pygame
http://www.pygame.org/

For tutorial, see: http://programarcadegames.com/index.php?lang=en

###Tiled and PyTMX
This game uses Tiled as the map editor, that can be found at http://www.mapeditor.org/

To getting started with Tiled, see http://gamedevelopment.tutsplus.com/tutorials/introduction-to-tiled-map-editor--gamedev-2838

The .tmx-format is handled using PyTMX library: https://github.com/bitcraft/PyTMX

##What's working so far
*Player can move around the map and pick up items*

*Levels support scrolling, obstacles and items*

*Crude inventory menu*

*Rough switching between the game and the Python shell*

##What's next
*Interaction between the shell and the game, e.g. solving problems using coding*

*Switching between levels*

*Adding NPCs to the levels*

##Quick instructions

To run the game:
  *python main.py*

####Controls:
  *WASD - move*
  
  *I - open inventory*
  
  *T - switch to shell (to switch back, type 'exit' in shell)*
