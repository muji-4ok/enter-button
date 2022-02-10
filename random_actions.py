import os

import cfg
import utils
import random

sfx_filenames = os.listdir(utils.SFX_DIR)

RANDOM_ACTIONS = []
WEIGHTS = []

for sound in sfx_filenames:
    RANDOM_ACTIONS += [('play_sound', str(utils.SFX_DIR / sound))]
    WEIGHTS += [cfg.SOUND_ACTION_WEIGHT]

links = [
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'https://moodle.phystech.edu'
]

for link in links:
    RANDOM_ACTIONS += [('open_link', link)]
    WEIGHTS += [cfg.VIDEO_ACTION_WEIGHT]

RANDOM_ACTIONS += [('shutdown', None)]
WEIGHTS += [cfg.SHUTDOWN_ACTION_WEIGHT]

RANDOM_ACTIONS += [('insult', None)]
WEIGHTS += [cfg.INSULT_ACTION_WEIGHT]

command = {
    'play_sound': lambda x: utils.play_sound(x),
    'open_link': lambda x: utils.open_link(x),
    'shutdown': lambda x: utils.shutdown_action(),
    'insult': lambda x: utils.random_insult()
}


def random_action():
    action = random.choices(RANDOM_ACTIONS, weights=WEIGHTS)[0]
    command[action[0]](action[1])


random_action()
