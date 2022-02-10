# enter-button

First run `setup.py` without root privileges to save environment variables.

Run `main.py` with root privileges (needed to capture HID). Upon receiving signal from HID sends signal to all clients.

Clients upon receiving signal run `random_actions.py` which takes actions from `utils.py`.