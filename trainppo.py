from stable_baselines3 import PPO
import os
from sc2env import Sc2Env
import time

model_name = f"{int(time.time())}"
models_dir = f"models/{model_name}"
abs_models_dir = os.path.abspath(models_dir)
print(f"Saving models to: {abs_models_dir}")
log_dir = f"logs/{model_name}"


if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

env = Sc2Env()
model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_dir)
timesteps = 100000
iters = 0
while True:
    try:
        print('iteration:', iters)
        iters += 1
        model.learn(total_timesteps=timesteps, reset_num_timesteps=False, tb_log_name="PPO")
        model.save(f"{models_dir}/model_{iters}")
        print(f"Saved model to: {os.path.abspath(f'{models_dir}/model_{iters}')}")
    except Exception as e:
        print(f"An error occurred: {e}")
        break

