import os

from wave_venture import utils


url = os.environ.get("URL", "https://daemon.wave-venture.com/api")
plotter = os.environ.get("PLOTTER", utils.find_gui_plotter())
auth_token = os.environ.get("AUTH_TOKEN", utils.find_auth_token())
