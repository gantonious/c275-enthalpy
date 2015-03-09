EnthalPy
========
Steven Boddez and George Antonious, CMPUT 275 Section EB1

Description
-----------
EnthalPy will be a single-player/co-op bullet hell game in the likes of Touhou and Geometry Wars. The game will feature enemies and bosses with unique bullet and moving patterns, multiple levels, controller support, and a power-up/points system. The idea is to have a fast-paced environment where the player(s) must dodge large amounts of projectiles while using their own shots to defeat enemies. Many of the concepts used in this game can be carried over from last semester’s PvPuino project.

Milestones
----------
- **March 12**: Here we will have functioning controller input, a moving character than can shoot, a sample enemy with a simple shooting pattern, hitboxes, and a health system for the character and the enemy. For now bullets will be stored in lists, and collision detection will be simple 4-side rectangular collision.
- **March 16**: Generate multiple types of enemies, walls and other obstacles that must be dodged. Enemies can be the simple type or can be boss enemies, which we would put at the end of a level.
- **March 20**: Drops: when enemies die, have a chance to drop points, extra lives or power-ups that make the player stronger in some way. Power-ups may also affect the environment (eg. slow everything down to make dodging easier.)
- **March 24**: Create levels that can be loaded or read in realtime from external files. The files would define when to spawn enemies, and which types of enemies to create.
- **March 28**: Since this is a bullet hell game, there will be many projectiles on screen at once, and checking them all for collision every frame can be slow if the number of projectiles is especially large, or if the bullet patterns are complex to begin with. Here we would like to introduce a more complex form of collision detection that will be faster than the naive algorithm we already know. This could mean something like only checking for collisions that are “likely” and skipping ones that are “unlikely”.
- **April 2**: Polish: Things like menus and level progression can be added in the late stages.
- **If we have time**: Graphics improvement and music: Because no one prefers a silent game with squares for characters over the alternative.