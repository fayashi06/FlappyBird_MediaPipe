# Ginger — Flappy Bird with Hand Gesture Control

Ginger is a gesture-controlled Flappy Bird-style game developed using **Python, Pygame, and MediaPipe**.

Instead of using a keyboard or mouse, the player controls Ginger using **hand movements captured through a camera**. The project combines computer vision with a classic arcade-style game to create an interactive and fun gaming experience.

## Project Overview

The main character, **Ginger**, is a custom Flappy Bird-style character that flies through obstacles while the player controls its movement using hand gestures.

The game includes:

* Hand gesture-based flight control
* Real-time hand tracking using MediaPipe
* Animated game environment
* Moving clouds and background elements
* Obstacles and collision detection
* Coin collection system
* Score and high-score tracking
* Increasing game speed as the score increases
* Character skin changes during gameplay
* Background music
* Sound effects for different game events
* Mute functionality
* Game start and game-over sounds
* Countdown effects
* Camera and hand-tracking test programs

## Technologies Used

* **Python** — Main programming language
* **Pygame** — Game development, graphics, and audio
* **MediaPipe** — Real-time hand tracking
* **OpenCV** — Camera input and computer vision
* **NumPy** — Numerical processing

## How It Works

The camera captures the player's hand movements in real time.

MediaPipe detects and tracks the hand landmarks. The detected hand position is then processed by the game controller and converted into movement commands for Ginger.

This allows the player to control the bird without touching the keyboard or mouse.

## Game Features

### Hand Gesture Control

Ginger's movement is controlled through the player's hand position detected by the camera.

### Dynamic Difficulty

The game becomes faster as the player achieves a higher score. The increasing speed gradually raises the difficulty and makes longer gameplay more challenging.

### Character Skin Changes

Ginger's appearance changes as the score increases, adding a visual progression system to the gameplay.

### Coins

Players can collect coins while flying through the level.

The game includes a separate coin counter and a dedicated coin collection sound effect. The coin count is reset when a new game starts.

### Sound System

The project includes background music and several sound effects for different game events:

* Flap sound
* Coin collection sound
* Point/score sound
* Collision sound
* Game-over sound
* Start sound
* Countdown sound
* Background music

A **mute option** is also available, allowing the player to turn the audio on or off during gameplay.

### Score System

The game keeps track of the player's current score and stores the **high score locally**.

The high score is preserved between game sessions, allowing players to keep track of their best performance.

The score also affects the game difficulty, with the game speed increasing as the score gets higher.

## Project Structure

```text
FlappyBird_MediaPipe/
│
├── models/
│   └── hand_landmarker.task
│
├── sounds/
│   ├── flap.wav
│   ├── coin.wav
│   ├── point.wav
│   ├── collision.wav
│   ├── game_over.wav
│   ├── start.wav
│   └── countdown.wav
│
├── high_score.txt
├── test_camera.py
├── test_hand_model.py
├── test_mediapipe.py
├── test_pygame.py
└── main.py
```

## Installation

Clone the repository:

```bash
git clone https://github.com/fayashi06/FlappyBird_MediaPipe.git
```

Navigate to the project directory:

```bash
cd FlappyBird_MediaPipe
```

Install the required libraries:

```bash
pip install pygame mediapipe opencv-python numpy
```

Make sure the `hand_landmarker.task` model is placed inside the `models` folder.

## Running the Game

Run the main Python file:

```bash
python main.py
```

Make sure your computer has a working camera, as the game uses the camera for real-time hand tracking.

## Testing

The project includes several test programs for checking the camera, MediaPipe hand tracking, and Pygame.

For example:

```bash
python test_camera.py
```

```bash
python test_hand_model.py
```

These programs can be used to verify that the required components are working correctly before running the game.

## Goal of the Project

The goal of Ginger is to demonstrate how **computer vision and real-time hand gesture recognition** can be integrated into an interactive game.

By combining **MediaPipe hand tracking** with **Pygame**, Ginger transforms a traditional Flappy Bird-style game into a touch-free gaming experience.


