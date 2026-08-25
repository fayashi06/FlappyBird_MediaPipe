import pygame
import sys
import math
import random
import cv2

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# =========================================================
# INITIALIZATION
# =========================================================

pygame.init()

try:
    pygame.mixer.init()
    SOUND_ENABLED = True
except pygame.error:
    SOUND_ENABLED = False


WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GINGER - Dynamic World")

clock = pygame.time.Clock()


# =========================================================
# MUSIC
# =========================================================

MUSIC_FILE = "sounds/brainrot.wav"

music_on = True

if SOUND_ENABLED:
    try:
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
    except (pygame.error, FileNotFoundError):
        print("WARNING: brainrot.wav not found.")


# =========================================================
# SOUND EFFECTS
# =========================================================

def load_sound(filename, volume=0.5):

    if not SOUND_ENABLED:
        return None

    try:

        sound = pygame.mixer.Sound(
            f"sounds/{filename}"
        )

        sound.set_volume(volume)

        return sound

    except (pygame.error, FileNotFoundError):

        print(
            f"WARNING: sounds/{filename} not found."
        )

        return None


flap_sound = load_sound(
    "flap.wav",
    0.45
)

point_sound = load_sound(
    "point.wav",
    0.55
)

hit_sound = load_sound(
    "hit.wav",
    0.65
)

game_over_sound = load_sound(
    "game_over.wav",
    0.65
)

coin_sound = load_sound(
    "coin.wav",
    0.55
)


def play_sound(sound):

    if sound is not None:
        sound.play()


# =========================================================
# COLORS
# =========================================================

WHITE = (255, 255, 255)
BLACK = (20, 20, 25)

RED = (255, 60, 60)

ORANGE = (255, 150, 25)
DARK_ORANGE = (210, 100, 10)

SUN_YELLOW = (255, 220, 60)
SUN_LIGHT = (255, 240, 150)

CLOUD_WHITE = (255, 255, 255)

GRASS = (95, 190, 75)
GRASS_DARK = (55, 150, 60)

PIPE_GREEN = (70, 180, 70)
PIPE_DARK = (50, 150, 50)

BUTTON_GREEN = (70, 180, 90)
BUTTON_DARK = (40, 130, 60)

GRAY = (100, 100, 100)

COIN_YELLOW = (255, 205, 40)
COIN_ORANGE = (235, 150, 10)


# =========================================================
# GINGER SKINS
# =========================================================

SKINS = [

    {
        "name": "CLASSIC",
        "body": (210, 55, 45),
        "light": (240, 80, 60),
        "wing": (165, 40, 35)
    },

    {
        "name": "BLUE",
        "body": (45, 120, 220),
        "light": (80, 160, 255),
        "wing": (30, 80, 170)
    },

    {
        "name": "GREEN",
        "body": (50, 180, 80),
        "light": (90, 220, 110),
        "wing": (30, 130, 55)
    },

    {
        "name": "PURPLE",
        "body": (150, 70, 210),
        "light": (190, 110, 240),
        "wing": (100, 40, 150)
    },

    {
        "name": "DARK",
        "body": (45, 45, 55),
        "light": (90, 90, 100),
        "wing": (20, 20, 25)
    },

    {
        "name": "FIRE",
        "body": (255, 80, 20),
        "light": (255, 170, 30),
        "wing": (180, 40, 10)
    }
]


current_skin = 0

skin_message = ""
skin_message_timer = 0


# =========================================================
# MEDIAPIPE
# =========================================================

MODEL_PATH = "models/hand_landmarker.task"

base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(
    options
)


# =========================================================
# CAMERA
# =========================================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print(
        "ERROR: Camera could not be opened!"
    )

    pygame.quit()
    sys.exit()


# =========================================================
# HAND CONTROL
# =========================================================

FLAP_THRESHOLD = 0.50

previous_hand_y = 0.60


# =========================================================
# GINGER
# =========================================================

bird_x = 200
bird_y = 300

bird_width = 52
bird_height = 45

bird_velocity = 0

GRAVITY = 0.5
FLAP_STRENGTH = -9


# =========================================================
# WING ANIMATION
# =========================================================

wing_angle = 0
wing_direction = 1


# =========================================================
# WORLD
# =========================================================

background_offset = 0


# =========================================================
# STARS
# =========================================================

stars = []

for _ in range(80):

    stars.append(
        {
            "x": random.randint(
                0,
                WIDTH
            ),
            "y": random.randint(
                0,
                HEIGHT - 100
            ),
            "size": random.randint(
                1,
                3
            ),
            "speed": random.uniform(
                0.2,
                0.8
            )
        }
    )


# =========================================================
# SPACE STARS
# =========================================================

space_stars = []

for _ in range(50):

    space_stars.append(
        {
            "x": random.randint(
                0,
                WIDTH
            ),
            "y": random.randint(
                0,
                HEIGHT
            ),
            "size": random.randint(
                1,
                4
            )
        }
    )


# =========================================================
# PIPES
# =========================================================

pipe_width = 80

BASE_PIPE_SPEED = 4
MAX_PIPE_SPEED = 8

pipe_speed = BASE_PIPE_SPEED

pipe_gap = 180

pipe_x = WIDTH

pipe_gap_y = random.randint(
    180,
    380
)

pipe_passed = False


# =========================================================
# SCORE
# =========================================================

score = 0


# =========================================================
# LIVES
# =========================================================

lives = 3


# =========================================================
# HIGH SCORE
# =========================================================

high_score = 0

HIGH_SCORE_FILE = "high_score.txt"

try:

    with open(
        HIGH_SCORE_FILE,
        "r"
    ) as file:

        high_score = int(
            file.read()
        )

except:

    high_score = 0


# =========================================================
# COINS
# =========================================================

coins = 0

COINS_FILE = "coins.txt"

try:

    with open(
        COINS_FILE,
        "r"
    ) as file:

        coins = int(
            file.read()
        )

except:

    coins = 0


coin_x = WIDTH + 200
coin_y = 300

coin_radius = 15

coin_active = False

coin_rotation = 0


# =========================================================
# PARTICLES
# =========================================================

coin_particles = []


def create_coin_particles(x, y):

    for _ in range(12):

        angle = random.uniform(
            0,
            math.pi * 2
        )

        speed = random.uniform(
            1,
            4
        )

        coin_particles.append(
            {
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": 30
            }
        )


def update_coin_particles():

    for particle in coin_particles[:]:

        particle["x"] += particle["vx"]

        particle["y"] += particle["vy"]

        particle["life"] -= 1

        if particle["life"] <= 0:

            coin_particles.remove(
                particle
            )


def draw_coin_particles():

    for particle in coin_particles:

        pygame.draw.circle(
            screen,
            COIN_YELLOW,
            (
                int(particle["x"]),
                int(particle["y"])
            ),
            3
        )


# =========================================================
# GAME STATES
# =========================================================

MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

game_state = MENU


# =========================================================
# FONTS
# =========================================================

title_font = pygame.font.Font(
    None,
    70
)

medium_font = pygame.font.Font(
    None,
    35
)

small_font = pygame.font.Font(
    None,
    25
)

score_font = pygame.font.Font(
    None,
    50
)


# =========================================================
# BUTTONS
# =========================================================

start_button = pygame.Rect(
    300,
    350,
    200,
    70
)

restart_button = pygame.Rect(
    300,
    400,
    200,
    65
)

mute_button = pygame.Rect(
    650,
    520,
    120,
    50
)


# =========================================================
# WORLD MODE
# =========================================================

def get_world_mode():

    if score < 10:

        return "DAY"

    elif score < 20:

        return "SUNSET"

    elif score < 30:

        return "NIGHT"

    else:

        return "SPACE"


# =========================================================
# DRAW DAY
# =========================================================

def draw_day():

    screen.fill(
        (135, 206, 250)
    )


# =========================================================
# DRAW SUNSET
# =========================================================

def draw_sunset():

    screen.fill(
        (235, 135, 105)
    )

    # Sunset gradient-like layers

    pygame.draw.rect(
        screen,
        (245, 160, 100),
        (
            0,
            180,
            WIDTH,
            130
        )
    )

    pygame.draw.rect(
        screen,
        (255, 190, 110),
        (
            0,
            310,
            WIDTH,
            100
        )
    )

    # Sun

    pygame.draw.circle(
        screen,
        (255, 190, 70),
        (
            680,
            330
        ),
        55
    )


# =========================================================
# DRAW NIGHT
# =========================================================

def draw_night():

    screen.fill(
        (25, 35, 80)
    )

    # Moon

    pygame.draw.circle(
        screen,
        (245, 245, 210),
        (
            680,
            100
        ),
        50
    )

    pygame.draw.circle(
        screen,
        (25, 35, 80),
        (
            700,
            85
        ),
        45
    )

    # Stars

    for star in stars:

        twinkle = random.choice(
            [True, False]
        )

        size = star["size"]

        if twinkle:

            size += 1

        pygame.draw.circle(
            screen,
            WHITE,
            (
                int(star["x"]),
                int(star["y"])
            ),
            size
        )


# =========================================================
# DRAW SPACE
# =========================================================

def draw_space():

    screen.fill(
        (8, 5, 30)
    )

    # Stars

    for star in space_stars:

        pygame.draw.circle(
            screen,
            WHITE,
            (
                int(star["x"]),
                int(star["y"])
            ),
            star["size"]
        )

    # Planet

    pygame.draw.circle(
        screen,
        (90, 50, 180),
        (
            680,
            130
        ),
        60
    )

    pygame.draw.ellipse(
        screen,
        (180, 100, 230),
        (
            610,
            110,
            140,
            35
        ),
        5
    )


# =========================================================
# DRAW WORLD
# =========================================================

def draw_world():

    mode = get_world_mode()

    if mode == "DAY":

        draw_day()

    elif mode == "SUNSET":

        draw_sunset()

    elif mode == "NIGHT":

        draw_night()

    else:

        draw_space()


# =========================================================
# SUN
# =========================================================

def draw_sun():

    if get_world_mode() != "DAY":
        return

    sun_x = 680
    sun_y = 100

    pygame.draw.circle(
        screen,
        SUN_LIGHT,
        (
            sun_x,
            sun_y
        ),
        65
    )

    pygame.draw.circle(
        screen,
        SUN_YELLOW,
        (
            sun_x,
            sun_y
        ),
        45
    )


# =========================================================
# CLOUD
# =========================================================

def draw_cloud(
    x,
    y,
    scale=1
):

    pygame.draw.circle(
        screen,
        CLOUD_WHITE,
        (
            int(x),
            int(y)
        ),
        int(25 * scale)
    )

    pygame.draw.circle(
        screen,
        CLOUD_WHITE,
        (
            int(
                x + 30 * scale
            ),
            int(
                y - 10 * scale
            )
        ),
        int(32 * scale)
    )

    pygame.draw.circle(
        screen,
        CLOUD_WHITE,
        (
            int(
                x + 65 * scale
            ),
            int(y)
        ),
        int(25 * scale)
    )

    pygame.draw.ellipse(
        screen,
        CLOUD_WHITE,
        (
            int(
                x - 5 * scale
            ),
            int(y),
            int(
                75 * scale
            ),
            int(
                30 * scale
            )
        )
    )


# =========================================================
# MOVING CLOUDS
# =========================================================

def draw_moving_clouds():

    if get_world_mode() not in [
        "DAY",
        "SUNSET"
    ]:
        return

    clouds = [

        (100, 120, 1.0),

        (450, 90, 0.8),

        (700, 190, 1.1),

        (300, 210, 0.7)
    ]

    for x, y, scale in clouds:

        moving_x = (
            x
            - background_offset * 0.5
        )

        if moving_x < -150:

            moving_x += WIDTH + 200

        draw_cloud(
            moving_x,
            y,
            scale
        )


# =========================================================
# GROUND
# =========================================================

def draw_ground():

    ground_y = HEIGHT - 55

    if get_world_mode() == "SPACE":

        pygame.draw.rect(
            screen,
            (40, 25, 70),
            (
                0,
                ground_y,
                WIDTH,
                55
            )
        )

    elif get_world_mode() == "NIGHT":

        pygame.draw.rect(
            screen,
            (35, 90, 55),
            (
                0,
                ground_y,
                WIDTH,
                55
            )
        )

    else:

        pygame.draw.rect(
            screen,
            GRASS,
            (
                0,
                ground_y,
                WIDTH,
                55
            )
        )

    pygame.draw.rect(
        screen,
        GRASS_DARK,
        (
            0,
            ground_y,
            WIDTH,
            8
        )
    )


# =========================================================
# PIPES
# =========================================================

def draw_pipes():

    top_height = (
        pipe_gap_y
        - pipe_gap // 2
    )

    pipe_color = PIPE_GREEN

    if get_world_mode() == "SPACE":

        pipe_color = (
            120,
            60,
            200
        )

    elif get_world_mode() == "NIGHT":

        pipe_color = (
            40,
            130,
            80
        )

    pygame.draw.rect(
        screen,
        pipe_color,
        (
            pipe_x,
            0,
            pipe_width,
            top_height
        )
    )

    pygame.draw.rect(
        screen,
        PIPE_DARK,
        (
            pipe_x - 5,
            top_height - 20,
            pipe_width + 10,
            20
        )
    )

    bottom_y = (
        pipe_gap_y
        + pipe_gap // 2
    )

    pygame.draw.rect(
        screen,
        pipe_color,
        (
            pipe_x,
            bottom_y,
            pipe_width,
            HEIGHT - bottom_y - 55
        )
    )

    pygame.draw.rect(
        screen,
        PIPE_DARK,
        (
            pipe_x - 5,
            bottom_y,
            pipe_width + 10,
            20
        )
    )


# =========================================================
# COIN
# =========================================================

def spawn_coin():

    global coin_x
    global coin_y
    global coin_active

    coin_x = WIDTH + random.randint(
        100,
        250
    )

    coin_y = random.randint(
        100,
        HEIGHT - 130
    )

    coin_active = True


def draw_coin():

    global coin_rotation

    if not coin_active:
        return

    coin_rotation += 8

    width_factor = abs(
        math.cos(
            math.radians(
                coin_rotation
            )
        )
    )

    coin_width = max(
        4,
        int(
            coin_radius
            * width_factor
        )
    )

    pygame.draw.ellipse(
        screen,
        COIN_ORANGE,
        (
            int(
                coin_x - coin_width
            ),
            int(
                coin_y - coin_radius
            ),
            int(
                coin_width * 2
            ),
            int(
                coin_radius * 2
            )
        )
    )

    pygame.draw.ellipse(
        screen,
        COIN_YELLOW,
        (
            int(
                coin_x - coin_width + 3
            ),
            int(
                coin_y - coin_radius + 3
            ),
            int(
                coin_width * 2 - 6
            ),
            int(
                coin_radius * 2 - 6
            )
        )
    )


def check_coin_collision():

    if not coin_active:

        return False

    distance = math.sqrt(
        (
            bird_x
            + bird_width // 2
            - coin_x
        ) ** 2
        +
        (
            bird_y
            + bird_height // 2
            - coin_y
        ) ** 2
    )

    return distance < 40


def collect_coin():

    global coins
    global coin_active

    coins += 1

    try:

        with open(
            COINS_FILE,
            "w"
        ) as file:

            file.write(
                str(coins)
            )

    except:

        pass

    create_coin_particles(
        coin_x,
        coin_y
    )

    play_sound(
        coin_sound
    )

    coin_active = False


# =========================================================
# PARTICLES
# =========================================================

def create_coin_particles(
    x,
    y
):

    for _ in range(12):

        angle = random.uniform(
            0,
            math.pi * 2
        )

        speed = random.uniform(
            1,
            4
        )

        coin_particles.append(
            {
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": 30
            }
        )


def update_coin_particles():

    for particle in coin_particles[:]:

        particle["x"] += particle["vx"]

        particle["y"] += particle["vy"]

        particle["life"] -= 1

        if particle["life"] <= 0:

            coin_particles.remove(
                particle
            )


def draw_coin_particles():

    for particle in coin_particles:

        pygame.draw.circle(
            screen,
            COIN_YELLOW,
            (
                int(
                    particle["x"]
                ),
                int(
                    particle["y"]
                )
            ),
            3
        )


# =========================================================
# GINGER
# =========================================================

def draw_ginger(
    x,
    y
):

    global wing_angle
    global wing_direction

    skin = SKINS[
        current_skin
    ]

    body_color = skin["body"]
    light_color = skin["light"]
    wing_color = skin["wing"]

    wing_angle += (
        2 * wing_direction
    )

    if wing_angle > 15:

        wing_direction = -1

    if wing_angle < -15:

        wing_direction = 1

    # LEFT WING

    pygame.draw.polygon(
        screen,
        wing_color,
        [
            (
                x + 8,
                y + 25
            ),
            (
                x - 25,
                y + 8
                + wing_angle
            ),
            (
                x - 18,
                y + 32
                + wing_angle
            ),
            (
                x + 12,
                y + 38
            )
        ]
    )

    # RIGHT WING

    pygame.draw.polygon(
        screen,
        wing_color,
        [
            (
                x + 42,
                y + 25
            ),
            (
                x + 75,
                y + 8
                - wing_angle
            ),
            (
                x + 68,
                y + 34
                - wing_angle
            ),
            (
                x + 38,
                y + 39
            )
        ]
    )

    # BODY

    pygame.draw.ellipse(
        screen,
        body_color,
        (
            x,
            y,
            bird_width,
            bird_height
        )
    )

    # FACE

    pygame.draw.ellipse(
        screen,
        light_color,
        (
            x + 8,
            y + 5,
            35,
            25
        )
    )

    # EYES

    pygame.draw.circle(
        screen,
        WHITE,
        (
            x + 20,
            y + 16
        ),
        10
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (
            x + 20,
            y + 17
        ),
        5
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (
            x + 36,
            y + 16
        ),
        10
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (
            x + 36,
            y + 17
        ),
        5
    )

    # ANGRY EYEBROWS

    pygame.draw.line(
        screen,
        BLACK,
        (
            x + 10,
            y + 5
        ),
        (
            x + 25,
            y + 11
        ),
        5
    )

    pygame.draw.line(
        screen,
        BLACK,
        (
            x + 31,
            y + 11
        ),
        (
            x + 46,
            y + 5
        ),
        5
    )

    # BEAK

    pygame.draw.polygon(
        screen,
        ORANGE,
        [
            (
                x + 45,
                y + 20
            ),
            (
                x + 68,
                y + 24
            ),
            (
                x + 45,
                y + 28
            )
        ]
    )

    pygame.draw.polygon(
        screen,
        DARK_ORANGE,
        [
            (
                x + 45,
                y + 28
            ),
            (
                x + 65,
                y + 28
            ),
            (
                x + 48,
                y + 34
            )
        ]
    )


# =========================================================
# MEDIAPIPE
# =========================================================

def get_hand_data():

    success, frame = camera.read()

    if not success:

        return None, None

    frame = cv2.flip(
        frame,
        1
    )

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    result = detector.detect(
        mp_image
    )

    hand_y = None

    if result.hand_landmarks:

        hand = result.hand_landmarks[0]

        index_finger = hand[8]

        hand_y = index_finger.y

        pixel_x = int(
            index_finger.x
            * frame.shape[1]
        )

        pixel_y = int(
            index_finger.y
            * frame.shape[0]
        )

        cv2.circle(
            frame,
            (
                pixel_x,
                pixel_y
            ),
            10,
            (0, 255, 0),
            -1
        )

        cv2.putText(
            frame,
            f"Y: {hand_y:.2f}",
            (
                15,
                30
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    return hand_y, frame


# =========================================================
# CAMERA PREVIEW
# =========================================================

def draw_camera_preview(
    frame
):

    if frame is None:

        return

    preview_width = 200
    preview_height = 150

    small_frame = cv2.resize(
        frame,
        (
            preview_width,
            preview_height
        )
    )

    small_frame = cv2.cvtColor(
        small_frame,
        cv2.COLOR_BGR2RGB
    )

    camera_surface = pygame.surfarray.make_surface(
        small_frame.swapaxes(
            0,
            1
        )
    )

    camera_x = 580
    camera_y = 20

    pygame.draw.rect(
        screen,
        BLACK,
        (
            camera_x - 4,
            camera_y - 4,
            preview_width + 8,
            preview_height + 8
        )
    )

    screen.blit(
        camera_surface,
        (
            camera_x,
            camera_y
        )
    )


# =========================================================
# COLLISION
# =========================================================

def check_collision():

    bird_rect = pygame.Rect(
        bird_x + 5,
        bird_y + 5,
        bird_width - 10,
        bird_height - 10
    )

    top_rect = pygame.Rect(
        pipe_x,
        0,
        pipe_width,
        pipe_gap_y
        - pipe_gap // 2
    )

    bottom_y = (
        pipe_gap_y
        + pipe_gap // 2
    )

    bottom_rect = pygame.Rect(
        pipe_x,
        bottom_y,
        pipe_width,
        HEIGHT
        - bottom_y
        - 55
    )

    ground_rect = pygame.Rect(
        0,
        HEIGHT - 55,
        WIDTH,
        55
    )

    return (
        bird_rect.colliderect(
            top_rect
        )
        or
        bird_rect.colliderect(
            bottom_rect
        )
        or
        bird_rect.colliderect(
            ground_rect
        )
        or
        bird_y < 0
    )


# =========================================================
# LIVES
# =========================================================

def draw_lives():

    for i in range(3):

        x = 25 + i * 40
        y = 90

        color = (
            RED
            if i < lives
            else GRAY
        )

        pygame.draw.circle(
            screen,
            color,
            (
                x,
                y
            ),
            12
        )

        pygame.draw.circle(
            screen,
            color,
            (
                x + 14,
                y
            ),
            12
        )

        pygame.draw.polygon(
            screen,
            color,
            [
                (
                    x - 10,
                    y + 5
                ),
                (
                    x + 7,
                    y + 28
                ),
                (
                    x + 24,
                    y + 5
                )
            ]
        )


# =========================================================
# MUSIC BUTTON
# =========================================================

def draw_music_button():

    if music_on:

        color = BUTTON_GREEN

        text = "MUSIC ON"

    else:

        color = RED

        text = "MUSIC OFF"

    pygame.draw.rect(
        screen,
        color,
        mute_button,
        border_radius=10
    )

    text_surface = pygame.font.Font(
        None,
        22
    ).render(
        text,
        True,
        WHITE
    )

    screen.blit(
        text_surface,
        (
            mute_button.centerx
            - text_surface.get_width() // 2,
            mute_button.centery
            - text_surface.get_height() // 2
        )
    )


def toggle_music():

    global music_on

    music_on = not music_on

    if SOUND_ENABLED:

        if music_on:

            pygame.mixer.music.set_volume(
                0.25
            )

        else:

            pygame.mixer.music.set_volume(
                0
            )


# =========================================================
# HIGH SCORE
# =========================================================

def update_high_score():

    global high_score

    if score > high_score:

        high_score = score

        try:

            with open(
                HIGH_SCORE_FILE,
                "w"
            ) as file:

                file.write(
                    str(high_score)
                )

        except:

            pass


# =========================================================
# RESET GAME
# =========================================================

def reset_game():

    global bird_y
    global bird_velocity
    global pipe_x
    global pipe_gap_y
    global score
    global lives
    global pipe_passed
    global background_offset
    global previous_hand_y
    global game_state
    global coin_active
    global pipe_speed
    global current_skin
    global skin_message
    global skin_message_timer

    bird_y = 300

    bird_velocity = 0

    pipe_x = WIDTH

    pipe_gap_y = random.randint(
        180,
        380
    )

    score = 0

    lives = 3

    pipe_speed = BASE_PIPE_SPEED

    current_skin = 0

    skin_message = ""

    skin_message_timer = 0

    pipe_passed = False

    background_offset = 0

    previous_hand_y = 0.60

    coin_active = False

    coin_particles.clear()

    spawn_coin()

    game_state = PLAYING


# =========================================================
# FLAP
# =========================================================

def flap():

    global bird_velocity

    bird_velocity = FLAP_STRENGTH

    play_sound(
        flap_sound
    )


# =========================================================
# MENU
# =========================================================

def draw_menu():

    title = title_font.render(
        "GINGER",
        True,
        SKINS[0]["body"]
    )

    screen.blit(
        title,
        (
            WIDTH // 2
            - title.get_width() // 2,
            80
        )
    )

    subtitle = medium_font.render(
        "DYNAMIC WORLD",
        True,
        BLACK
    )

    screen.blit(
        subtitle,
        (
            WIDTH // 2
            - subtitle.get_width() // 2,
            160
        )
    )

    draw_ginger(
        375,
        230
    )

    mouse_position = pygame.mouse.get_pos()

    button_color = (
        BUTTON_DARK
        if start_button.collidepoint(
            mouse_position
        )
        else BUTTON_GREEN
    )

    pygame.draw.rect(
        screen,
        button_color,
        start_button,
        border_radius=15
    )

    start_text = medium_font.render(
        "START",
        True,
        WHITE
    )

    screen.blit(
        start_text,
        (
            start_button.centerx
            - start_text.get_width() // 2,
            start_button.centery
            - start_text.get_height() // 2
        )
    )

    instruction = small_font.render(
        "Raise your hand to fly!",
        True,
        BLACK
    )

    screen.blit(
        instruction,
        (
            WIDTH // 2
            - instruction.get_width() // 2,
            445
        )
    )

    keyboard = small_font.render(
        "SPACE = flap     M = music",
        True,
        BLACK
    )

    screen.blit(
        keyboard,
        (
            WIDTH // 2
            - keyboard.get_width() // 2,
            480
        )
    )

    best_text = small_font.render(
        f"BEST SCORE: {high_score}",
        True,
        BLACK
    )

    screen.blit(
        best_text,
        (
            WIDTH // 2
            - best_text.get_width() // 2,
            515
        )
    )

    draw_music_button()


# =========================================================
# GAME OVER
# =========================================================

def draw_game_over():

    overlay = pygame.Surface(
        (
            WIDTH,
            HEIGHT
        ),
        pygame.SRCALPHA
    )

    overlay.fill(
        (
            0,
            0,
            0,
            160
        )
    )

    screen.blit(
        overlay,
        (
            0,
            0
        )
    )

    game_over_text = title_font.render(
        "GAME OVER",
        True,
        WHITE
    )

    screen.blit(
        game_over_text,
        (
            WIDTH // 2
            - game_over_text.get_width() // 2,
            120
        )
    )

    final_score = medium_font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(
        final_score,
        (
            WIDTH // 2
            - final_score.get_width() // 2,
            215
        )
    )

    best_text = medium_font.render(
        f"Best Score: {high_score}",
        True,
        SUN_YELLOW
    )

    screen.blit(
        best_text,
        (
            WIDTH // 2
            - best_text.get_width() // 2,
            265
        )
    )

    skin_text = medium_font.render(
        f"Skin: {SKINS[current_skin]['name']}",
        True,
        WHITE
    )

    screen.blit(
        skin_text,
        (
            WIDTH // 2
            - skin_text.get_width() // 2,
            315
        )
    )

    mouse_position = pygame.mouse.get_pos()

    button_color = (
        BUTTON_DARK
        if restart_button.collidepoint(
            mouse_position
        )
        else BUTTON_GREEN
    )

    pygame.draw.rect(
        screen,
        button_color,
        restart_button,
        border_radius=15
    )

    restart_text = medium_font.render(
        "RESTART",
        True,
        WHITE
    )

    screen.blit(
        restart_text,
        (
            restart_button.centerx
            - restart_text.get_width() // 2,
            restart_button.centery
            - restart_text.get_height() // 2
        )
    )

    draw_music_button()


# =========================================================
# MAIN LOOP
# =========================================================

running = True

while running:

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if mute_button.collidepoint(
                event.pos
            ):

                toggle_music()

            elif game_state == MENU:

                if start_button.collidepoint(
                    event.pos
                ):

                    reset_game()

            elif game_state == GAME_OVER:

                if restart_button.collidepoint(
                    event.pos
                ):

                    reset_game()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False

            elif event.key == pygame.K_m:

                toggle_music()

            elif event.key == pygame.K_SPACE:

                if game_state == MENU:

                    reset_game()

                elif game_state == PLAYING:

                    flap()

                elif game_state == GAME_OVER:

                    reset_game()

            elif event.key == pygame.K_r:

                if game_state == GAME_OVER:

                    reset_game()


    # =====================================================
    # CAMERA
    # =====================================================

    hand_y, camera_frame = get_hand_data()


    # =====================================================
    # MENU
    # =====================================================

    if game_state == MENU:

        draw_day()

        draw_sun()

        draw_moving_clouds()

        draw_ground()

        draw_menu()

        draw_camera_preview(
            camera_frame
        )


    # =====================================================
    # PLAYING
    # =====================================================

    elif game_state == PLAYING:

        # -------------------------------------------------
        # HAND CONTROL
        # -------------------------------------------------

        if hand_y is not None:

            if (
                hand_y < FLAP_THRESHOLD
                and previous_hand_y >= FLAP_THRESHOLD
            ):

                flap()

            previous_hand_y = hand_y


        # -------------------------------------------------
        # GRAVITY
        # -------------------------------------------------

        bird_velocity += GRAVITY

        bird_y += bird_velocity


        # -------------------------------------------------
        # PIPE
        # -------------------------------------------------

        pipe_x -= pipe_speed


        if pipe_x < -pipe_width:

            pipe_x = WIDTH

            pipe_gap_y = random.randint(
                180,
                380
            )

            pipe_passed = False

            spawn_coin()


        # -------------------------------------------------
        # SCORE
        # -------------------------------------------------

        if (
            not pipe_passed
            and pipe_x + pipe_width < bird_x
        ):

            score += 1

            # Speed increases every 5 points

            pipe_speed = min(
                BASE_PIPE_SPEED
                + (score // 5),
                MAX_PIPE_SPEED
            )

            # Skin changes every 5 points

            new_skin = min(
                score // 5,
                len(SKINS) - 1
            )

            if new_skin != current_skin:

                current_skin = new_skin

                skin_message = (
                    "NEW SKIN: "
                    + SKINS[
                        current_skin
                    ]["name"]
                )

                skin_message_timer = 120

            play_sound(
                point_sound
            )

            pipe_passed = True

            update_high_score()


        # -------------------------------------------------
        # MESSAGE
        # -------------------------------------------------

        if skin_message_timer > 0:

            skin_message_timer -= 1


        # -------------------------------------------------
        # COIN
        # -------------------------------------------------

        if coin_active:

            coin_x -= pipe_speed

            if coin_x < -50:

                spawn_coin()


        if check_coin_collision():

            collect_coin()


        update_coin_particles()


        # -------------------------------------------------
        # BACKGROUND MOVEMENT
        # -------------------------------------------------

        background_offset += pipe_speed


        # -------------------------------------------------
        # COLLISION
        # -------------------------------------------------

        if check_collision():

            play_sound(
                hit_sound
            )

            lives -= 1

            bird_y = 300

            bird_velocity = 0

            pipe_x = WIDTH

            pipe_gap_y = random.randint(
                180,
                380
            )

            pygame.time.delay(
                200
            )

            if lives <= 0:

                update_high_score()

                play_sound(
                    game_over_sound
                )

                game_state = GAME_OVER


        # -------------------------------------------------
        # WORLD
        # -------------------------------------------------

        draw_world()

        draw_sun()

        draw_moving_clouds()

        draw_pipes()

        draw_coin()

        draw_coin_particles()

        draw_ground()

        draw_ginger(
            bird_x,
            bird_y
        )

        draw_camera_preview(
            camera_frame
        )


        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        title = title_font.render(
            "GINGER",
            True,
            SKINS[
                current_skin
            ]["body"]
        )

        screen.blit(
            title,
            (
                20,
                15
            )
        )


        # -------------------------------------------------
        # SCORE
        # -------------------------------------------------

        score_text = score_font.render(
            str(score),
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (
                WIDTH // 2
                - score_text.get_width() // 2,
                20
            )
        )


        # -------------------------------------------------
        # WORLD MODE TEXT
        # -------------------------------------------------

        mode = get_world_mode()

        if mode == "DAY":

            mode_text = "☀ DAY"

        elif mode == "SUNSET":

            mode_text = "🌅 SUNSET"

        elif mode == "NIGHT":

            mode_text = "🌙 NIGHT"

        else:

            mode_text = "🌌 SPACE"


        mode_surface = small_font.render(
            mode_text,
            True,
            WHITE
        )

        screen.blit(
            mode_surface,
            (
                20,
                65
            )
        )


        # -------------------------------------------------
        # SPEED
        # -------------------------------------------------

        speed_text = small_font.render(
            f"SPEED: {pipe_speed}",
            True,
            WHITE
        )

        screen.blit(
            speed_text,
            (
                20,
                195
            )
        )


        # -------------------------------------------------
        # COINS
        # -------------------------------------------------

        coin_text = medium_font.render(
            f"COINS: {coins}",
            True,
            COIN_YELLOW
        )

        screen.blit(
            coin_text,
            (
                20,
                230
            )
        )


        # -------------------------------------------------
        # LIVES
        # -------------------------------------------------

        draw_lives()


        # -------------------------------------------------
        # BEST
        # -------------------------------------------------

        best_text = small_font.render(
            f"BEST: {high_score}",
            True,
            WHITE
        )

        screen.blit(
            best_text,
            (
                20,
                270
            )
        )


        # -------------------------------------------------
        # SKIN MESSAGE
        # -------------------------------------------------

        if skin_message_timer > 0:

            message_surface = medium_font.render(
                skin_message,
                True,
                SUN_YELLOW
            )

            message_surface.set_alpha(
                min(
                    255,
                    skin_message_timer * 3
                )
            )

            screen.blit(
                message_surface,
                (
                    WIDTH // 2
                    - message_surface.get_width() // 2,
                    120
                )
            )


        # -------------------------------------------------
        # MUSIC
        # -------------------------------------------------

        draw_music_button()


    # =====================================================
    # GAME OVER
    # =====================================================

    elif game_state == GAME_OVER:

        draw_world()

        draw_sun()

        draw_moving_clouds()

        draw_ground()

        draw_ginger(
            bird_x,
            bird_y
        )

        draw_camera_preview(
            camera_frame
        )

        draw_game_over()


    # =====================================================
    # DISPLAY
    # =====================================================

    pygame.display.flip()

    clock.tick(60)


# =========================================================
# CLEANUP
# =========================================================

camera.release()

detector.close()

if SOUND_ENABLED:

    pygame.mixer.music.stop()

pygame.quit()

sys.exit()