# Fly-A-Plane ![plane](https://github.com/user-attachments/assets/4846b14a-6018-489b-a785-c903d9b66265)

Fly-A-Plane via Python

The provided code implements a simple 2D game called "Fly A Plane" using Pygame. The `settings.py` file defines game settings like window dimensions and frame rate. In `main.py`, the game initializes Pygame, sets up the window, clock, and background music, and manages the game state. The main loop updates the game state, handles user input (quitting and jumping), spawns obstacles, updates and draws sprites, checks collisions, and displays the score.

The `sprites.py` file defines the sprite classes. The `BG` class manages the scrolling background, and the `Ground` class handles the scrolling ground. The `Plane` class manages the player's plane, including animation, movement, rotation, and jump sound effects. The `Obstacle` class handles obstacles, including their positioning, movement, and removal when off-screen.

The game starts by creating a `Game` class instance and running its `run` method, entering the main loop where the player controls the plane to jump and avoid obstacles while the background and ground scroll. The score is based on the survival time without collisions.

Modules and Libraries, Object-Oriented Programming (OOP), Event Handling, Game Loop, Image and Sound Handling, File Handling, Sprite Management, Collision Detection, Display and Rendering and more utilized.
