###### \# Ginger — Flappy Bird with Hand Gesture Control

###### 

###### Ginger is a gesture-controlled Flappy Bird-style game developed with Python, Pygame, and MediaPipe.

###### 

###### Instead of using a keyboard or mouse, the player controls Ginger using hand movements captured through a camera. The project combines computer vision with a classic arcade-style game to create an interactive and fun gaming experience.

###### 

###### \## Project Overview

###### 

###### The main character, Ginger, is a custom Flappy Bird-style character that flies through obstacles while the player controls its movement using hand gestures.

###### 

###### The game includes:

###### 

###### \* Hand gesture-based flight control

###### \* Real-time hand tracking using MediaPipe

###### \* Animated game environment

###### \* Moving clouds and background elements

###### \* Obstacles and collision detection

###### \* Coin collection system

###### \* Score and high-score tracking

###### \* Increasing game speed as the score increases

###### \* Character skin changes during gameplay

###### \* Background music

###### \* Sound effects for different game events

###### \* Mute functionality

###### \* Game start and game-over sounds

###### \* Countdown effects

###### \* Camera and hand-tracking test programs

###### 

###### \## Technologies Used

###### 

###### \* \*\*Python\*\*

###### \* \*\*Pygame\*\* — game development and graphics

###### \* \*\*MediaPipe\*\* — real-time hand tracking

###### \* \*\*OpenCV\*\* — camera input and computer vision

###### \* \*\*NumPy\*\* — numerical processing

###### 

###### \## How It Works

###### 

###### The camera captures the player's hand movements. MediaPipe detects and tracks the hand landmarks in real time.

###### 

###### The detected hand position is then processed by the game controller and converted into movement commands for Ginger.

###### 

###### This allows the player to control the bird without touching the keyboard.

###### 

###### \## Game Features

###### 

###### \### Hand Gesture Control

###### 

###### Ginger's movement is controlled through the player's hand position detected by the camera.

###### 

###### \### Dynamic Difficulty

###### 

###### The game becomes faster as the player achieves higher scores. This gradually increases the difficulty and makes longer gameplay more challenging.

###### 

###### \### Skin Changes

###### 

###### Ginger's appearance changes during gameplay as the score increases, adding a visual progression system.

###### 

###### \### Coins

###### 

###### Players can collect coins while flying through the level. A separate coin sound effect is included for collection feedback.

###### 

###### \### Sound System

###### 

###### The project includes several sound effects and background audio, including:

###### 

###### \* Flap sound

###### \* Coin collection sound

###### \* Point/score sound

###### \* Collision sound

###### \* Game-over sound

###### \* Start sound

###### \* Countdown sound

###### \* Background music

###### 

###### A mute option is also available so the player can turn the audio on or off.

###### 

###### \### Score System

###### 

###### The game keeps track of the player's score and stores the high score locally.

###### 

###### \## Project Structure

###### 

###### ```text

###### FlappyBird\_MediaPipe/

###### │

###### ├── game.py

###### ├── hand\_controller.py

###### ├── hand\_tracking.py

###### ├── create\_brainrot.py

###### ├── create\_coin\_sound.py

###### ├── create\_sounds.py

###### ├── coins.txt

###### ├── high\_score.txt

###### │

###### ├── models/

###### │   └── hand\_landmarker.task

###### │

###### ├── sounds/

###### │   ├── brainrot.wav

###### │   ├── coin.wav

###### │   ├── countdown.wav

###### │   ├── flap.wav

###### │   ├── game\_over.wav

###### │   ├── hit.wav

###### │   ├── point.wav

###### │   └── start.wav

###### │

###### ├── test\_camera.py

###### ├── test\_hand\_model.py

###### ├── test\_mediapipe.py

###### └── test\_pygame.py

###### ```

###### 

###### \## Installation

###### 

###### Clone the repository:

###### 

###### ```bash

###### git clone https://github.com/fayashi06/FlappyBird\_MediaPipe.git

###### cd FlappyBird\_MediaPipe

###### ```

###### 

###### Create and activate a virtual environment:

###### 

###### ```bash

###### python -m venv .venv

###### ```

###### 

###### Windows:

###### 

###### ```bash

###### .venv\\Scripts\\activate

###### ```

###### 

###### Install the required packages:

###### 

###### ```bash

###### pip install pygame mediapipe opencv-python numpy

###### ```

###### 

###### \## Running the Game

###### 

###### Run:

###### 

###### ```bash

###### python game.py

###### ```

###### 

###### Make sure your camera is available and working before starting the game.

###### 

###### \## Controls

###### 

###### The primary control method is hand movement detected through the camera.

###### 

###### The game also provides an in-game mute option for controlling the sound.

###### 

###### \## Purpose

###### 

###### The project was created to explore the combination of \*\*game development, computer vision, and human-computer interaction\*\*.

###### 

###### It demonstrates how real-time hand tracking can be integrated into a Python game to create a controller-free gaming experience.

###### 

###### \## Future Improvements

###### 

###### Possible future improvements include:

###### 

###### \* More character skins

###### \* Additional levels

###### \* More obstacle types

###### \* Improved gesture recognition

###### \* Online leaderboards

###### \* More interactive environments

###### \* Additional game modes

###### 

###### 

