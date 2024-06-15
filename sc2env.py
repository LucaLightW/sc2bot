import random

import gym
from gym import spaces
import numpy as np
import subprocess
import pickle
import time
import os


class Sc2Env(gym.Env):
	"""Custom gym env"""
	def __init__(self):
		super(Sc2Env, self).__init__()

		# if u have more actions then change this
		self.action_space = spaces.Discrete(6)
		# map stats for gym
		self.observation_space = spaces.Box(low = 0, high = 255, shape = (224, 224, 3), dtype = np.uint8)


	def step(self, action):
		wait_action = True

		while wait_action:
			#print('step: wait action')

			try:
				with open('state_rwd_action.pkl', 'rb') as f:
					state_rwd_action = pickle.load(f)

					# wait for action
					if state_rwd_action['action'] is not None:
						wait_action = True

					# if there is action then write it
					else:
						wait_action = False
						state_rwd_action['action'] = action

						with open('state_rwd_action.pkl', 'wb') as f:
							pickle.dump(state_rwd_action, f)

			except Exception as e:
				print(f"step: wait action: exception{e}")
				pass

		wait_state = True

		while wait_state:
			print('step: wait state')

			try:
				if os.path.getsize('state_rwd_action.pkl') > 0:
					with open('state_rwd_action.pkl', 'rb') as f:
						state_rwd_action = pickle.load(f)

						# wait for state
						if state_rwd_action['action'] is None:
							wait_state = True

						# if there is already: return state, reward, done.
						else:
							state = state_rwd_action['state']
							reward = state_rwd_action['reward']
							done = state_rwd_action['done']
							wait_state = False

			except Exception as e:

				wait_state = True
				map = np.zeros((224, 224, 3), dtype = np.uint8)
				rand_num = random.randint(0, 5)
				data = {'state': map, 'reward': 0, 'action': rand_num, 'done': False}

				with open('state_rwd_action.pkl', 'wb') as f:
					pickle.dump(data, f)

				state = map
				reward = 0
				done = False
				action = rand_num

		info = {}
		return state, reward, done, info


	def reset(self):
		print('reset')
		map = np.zeros((224, 224, 3), dtype = np.uint8)
		data = {'state': map, 'reward': 0, 'action': None, 'done': False}

		with open('state_rwd_action.pkl', 'wb') as f:
			pickle.dump(data, f)

		subprocess.Popen(['C:\\Users\\suatb\\miniconda3\\envs\\sc2botint\\python.exe', 'bot.py'])
		return map


