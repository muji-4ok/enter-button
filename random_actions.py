import keyboard
import os
import random
from pathlib import Path
import cfg

sfx_dir = Path(cfg.SFX_DIR)
sfx_filenames = os.listdir(sfx_dir)

RANDOM_ACTIONS = []
WEIGHTS = []

for sound in sfx_filenames:
    RANDOM_ACTIONS += [cfg.SOUND_PLAY_FUNCTION(sound)]
    WEIGHTS += [cfg.SOUND_ACTION_WEIGHT]

links = [
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'https://www.youtube.com/watch?v=sAn7baRbhx4'
]

for link in links:
    RANDOM_ACTIONS += [cfg.OPEN_LINK(link)]
    WEIGHTS += [cfg.VIDEO_ACTION_WEIGHT]

RANDOM_ACTIONS += [cfg.OPEN_LINK('https://moodle.phystech.edu')]
WEIGHTS += [10]

RANDOM_ACTIONS += [cfg.SHUTDOWN]
WEIGHTS += [1]


def exec_random_action():
    random_action = random.choices(RANDOM_ACTIONS, weights=WEIGHTS)[0]
    random_action()


exec_random_action()
