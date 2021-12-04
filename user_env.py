import os
import pickle
import utils
from pathlib import Path

env = dict(os.environ.copy())

env_file = Path(utils.ENV_FILE)

with open(env_file, 'wb') as f:
    pickle.dump(env, f)
