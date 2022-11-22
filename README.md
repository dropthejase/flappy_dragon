# FLAPPY DRAGON


##### Introduction - A mythical take on the classic game!
This project is my attempt to learn and utilise pygame to create a version of the famous Flappy Bird game that used to be available in the Apple Appstore.


###### How to Play
Simply hit the 'Space' bar to get the dragon to jump. Avoid hitting the ice blocks, and the top and bottom of the screen.


##### Code Structure
The modules used are: pygame and random

I set most of my default values at the top, including the window dimensions and score.
Lines 27-42 enable me to render the text into the game.
The space_counter is a way to enable the first 'Space' key press to start the game
Lines 48-53 set some of the ice block's properties. As blocks are created in pairs (one top, one bottom), the block_counter is a way to control when new block pairs are created.

Below this section are the class definitions.

Below the class definitions is the main() function. This contains the instantiation of a Player object and a Block pair. Both are added into respective sprite groups which enable the use of pygame's collision detection functionality. The main() function also contains the main pygame loop. Below this, assets are 'blipped' onto their respective rects.

Note: I had to put everything within an main() function to fulfill the requirements of the CS50 criteria although ordinarily I would not have done this.

Finally under the main() function are several other functions. The add_block() function creates block pairs with randomised heights, leaving a gap width of 150 pixels for the player to guide the dragon through. Below this are some functions that return some score statistics.


##### Player Class (the dragon)
Inherits from the pygame Sprite class and sets various kinematic constants.
The update() method keeps the dragon under gravitational pull and checks for collisions
The animate() method cycles through the various dragon.png files to create the illusion of wing flapping
The jump() method helps the player jump
The check_collision() method checks for collision


##### Block Class (to create block pairs)
Inherits from the pygame Sprite class and is used to create block pairs.
The update() method calls the move() and score() methods.
The move() method controls movement of the block pairs, as well as controls when a new block pair needs creating (i.e. when the previous block pair hits the left side of the screen)
The score() method updates the score.


##### Credits
Big thank you to Michael Eramo, whose Udemy course (https://www.udemy.com/course/the-art-of-doing-video-game-creation-with-python-and-pygame/) really helped me navigate the pygame library as well as introduced me to the general structure of game design using Python

The background asset was taken from: https://www.gameart2d.com/winter-platformer-game-tileset.html

The dragon asset was designed by me using the Krita 3D app
