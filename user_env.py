import os
import pickle
import cfg
from pathlib import Path

env = dict(os.environ.copy())

env_file = Path(cfg.ENV_FILE)

with open(env_file, 'wb') as f:
    pickle.dump(env, f)
