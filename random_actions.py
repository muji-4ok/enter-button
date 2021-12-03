import os
import random

import cfg

sfx_filenames = os.listdir(cfg.SFX_DIR)

random_actions = []
weights = []

for sound in sfx_filenames:
    random_actions += [cfg.sound_play_function(str(cfg.SFX_DIR / sound))]
    weights += [cfg.SOUND_ACTION_WEIGHT]

links = [
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'https://www.youtube.com/watch?v=sAn7baRbhx4',
    'https://moodle.phystech.edu'
]

for link in links:
    random_actions += [cfg.open_link(link)]
    weights += [cfg.VIDEO_ACTION_WEIGHT]

random_actions += [cfg.shutdown_action]
weights += [cfg.SHUTDOWN_ACTION_WEIGHT]


def exec_random_action():
    random_action = random.choices(random_actions, weights=weights)[0]
    random_action()


exec_random_action()
