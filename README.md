EnthalPy
========
Steven Boddez and George Antonious, CMPUT 275 Section EB1

Description
-----------
EnthalPy will be a single-player/co-op bullet hell game in the likes of Touhou and Geometry Wars. The game will feature enemies and bosses with unique bullet and moving patterns, multiple levels, controller support, and a power-up/points system. The idea is to have a fast-paced environment where the player(s) must dodge large amounts of projectiles while using their own shots to defeat enemies. Many of the concepts used in this game can be carried over from last semester’s PvPuino project.

Installing/Running
------------------
This game was built in Python3 using pygame 1.9.2a0, pygame distributions can be found at:
http://www.pygame.org/download.shtml

This game currently supports PS3 and PS4 controllers. All controllers intended on being used must be connected to your computer before launching the game, or the game will not detect them.

To run the game, do

    python3 main.py

Gameplay
--------
**cooperative play (min 1 player):**
The objective of this game mode is to kill all enemies (outlined in black) shooting at you. If a player dies they cannot return until the next level, if all players die the stage is failed. Note friendly fire is enabled so watch out. If a level is successfully cleared, players will be prompted to lock in to play the next level. When certain enemies die they may spawn some drops as a reward:
- Yellow Drop: increases your score
- Magenta Drop: temporary grants you invincibility
- Blue Drop: temporary increases your shot size

**head to head (min 2 players):** 
The objective of this game mode is to be the last player alive on the field. The mechanics are simple, aim your shots at your opponents and try and take them out. Note bullets collide with other players bullets, so use that to your advantage.

Menu
----
Note the menu system can only be navigated by player 1 (cause no one likes people spamming different buttons at the same time). The menu can be navigated using either stick on the controller. To select press 'X', to go back press 'O'. To pause the game press the "options" button.

**player select screen:**
Players are prompted to ready up and select their color. Once players intending on playing are ready. Player 1 one should press the select button to start the game.

**level clear screen:**
If there is a next level, players will be prompted to ready up to play the next level. Once players who still want to play are readied player 1 should press the select to move on to the next level. If you don't want to play the next level and return to the main menu, launch the pause menu and return to the main menu. If there is no next level or head to head mode is being played, the players will be prompted to play again or return to the main menu.

Level Creation
--------------
Custom levels can be created using the instructions found in levels/instructions

File Descriptions
----------------
**root directory/**
- main.py: initializes the gui and runs it to launch the game
- loader.py: contains the Loader class that parses a .lvl file to determine what enemies to spawn and when to spawn them
- quadtree.py: contains the Quadtree class that is used to reduce the number of collision checks conducted
- gui.py: contains the GUI class that handles running interfaces and acts as the middle man when changing interfaces
- elements.py: contains various UI element classes used by an interface
- drawing.py: contains various drawing functions

**assets/**: contains various media used in the game

**levels/**: contains level files

**entities/** contains all code related to an Entity
- entities/entity.py: base Entity class
- entities/individuals.py: contains the Player, Enemey, and Boss classes
- entities/projectiles.py: contains various projectile classes extended from the base Projectile class
- entities/patterns.py: contains various functions that define how an Enemy should move
- entities/drops.py: contain various drop classes extended from the base Drop class

**interfaces/** contains all code related to an Interface
- interfaces/interface.py: base Interface class
- interfaces/main_menu.py: contains the Main_Menu class
- interfaces/pause_menu.py: contains the Pause_Menu class
- interfaces/level_select.py: contains the Level_Select class
- interfaces/level_clear.py: contains the Level_Clear class
- interfaces/main_game.py: contains the Main_Game class
- interfaces/legacy_game.py: contains the Legacy_Game class

Credits
-------
Original Soundtrack by Steven Boddez

Menu Background found at http://static.zerochan.net/full/45/28/1076445.jpg