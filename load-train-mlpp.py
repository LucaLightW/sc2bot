# $ source ~/Desktop/sc2env/bin/activate

# so this works, so far.

from stable_baselines3 import PPO
import os
from sc2env import Sc2Env
import time

import wandb


LOAD_MODEL = "models/1718381844/1718381844.zip"
# Environment:
env = Sc2Env()

# load the model:
model = PPO.load(LOAD_MODEL, env=env)

model_name = f"{int(time.time())}"

models_dir = f"models/{model_name}/"
logdir = f"logs/{model_name}/"


conf_dict = {"Model": "load-v16s",
             "Machine": "Puget/Desktop/v18/2",
             "policy":"MlpPolicy",
             "model_save_name": model_name,
             "load_model": LOAD_MODEL
             }



# further train:
TIMESTEPS = 10000
iters = 0
while True:
	print("On iteration: ", iters)
	iters += 1
	model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
	model.save(f"{models_dir}/{TIMESTEPS*iters}")