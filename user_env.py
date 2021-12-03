import os
import pickle
import cfg
from pathlib import Path

env = os.environ.copy()

env_file = Path(cfg.ENV_FILE)

if not env_file.exists():
    env_file.touch()

with open(env_file, 'wb') as f:
    pickle.dump(env, f)
