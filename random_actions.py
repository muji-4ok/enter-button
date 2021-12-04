import os

import cfg
import utils
import random

sfx_filenames = os.listdir(utils.SFX_DIR)

RANDOM_ACTIONS = []
WEIGHTS = []

for sound in sfx_filenames:
    RANDOM_ACTIONS += [utils.sound_play_function(str(utils.SFX_DIR / sound))]
    WEIGHTS += [cfg.SOUND_ACTION_WEIGHT]

links = [
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'https://www.youtube.com/watch?v=sAn7baRbhx4',
    'https://moodle.phystech.edu'
]

for link in links:
    RANDOM_ACTIONS += [utils.open_link(link)]
    WEIGHTS += [cfg.VIDEO_ACTION_WEIGHT]

RANDOM_ACTIONS += [utils.shutdown_action]
WEIGHTS += [cfg.SHUTDOWN_ACTION_WEIGHT]

random_action = random.choices(RANDOM_ACTIONS, weights=WEIGHTS)[0]
random_action()
