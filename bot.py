from sc2.bot_ai import BotAI  # parent class we inherit from
from sc2.data import Difficulty, Race  # difficulty for bots, race for the 1 of 3 races
from sc2.main import run_game  # function that facilitates actually running the agents in games
from sc2.player import Bot, Computer  #wrapper for whether or not the agent is one of your bots, or a "computer" player
from sc2 import maps  # maps method for loading maps to play in.
from sc2.ids.unit_typeid import UnitTypeId
import random
import cv2
import math
import numpy as np
import sys
import pickle
import time
import os


SAVE_REPLAY = True

steps = 10000
pun_steps = np.linspace(0, 1, steps)
step_pun = ((np.exp(pun_steps ** 3) / 10) - 0.1) * 10


class sc2Bot(BotAI):


    async def on_step(self, iteration: int):
        fighters = [UnitTypeId.MOTHERSHIP, UnitTypeId.ZEALOT, UnitTypeId.STALKER, UnitTypeId.SENTRY,
                    UnitTypeId.ADEPT, UnitTypeId.HIGHTEMPLAR, UnitTypeId.DARKTEMPLAR, UnitTypeId.PHOENIX,
                    UnitTypeId.ORACLE, UnitTypeId.VOIDRAY, UnitTypeId.TEMPEST, UnitTypeId.CARRIER,
                    UnitTypeId.IMMORTAL, UnitTypeId.COLOSSUS, UnitTypeId.DISRUPTOR, UnitTypeId.WARPPRISM]

        no_action = True
        while no_action:
            try:
                with open('state_rwd_action.pkl', 'rb') as f:
                    state_rwd_action = pickle.load(f)

                    if state_rwd_action['action'] is None:
                        print('No action')
                        no_action = True
                    else:
                        print('Action found')
                        no_action = False

            except Exception as e:
                print(str(e))

        await self.distribute_workers()

        action = state_rwd_action['action']
        '''
        0: expand
        1: build stargate
        2: build voidray
        3: send scout
        4: attack
        5: voidray flee
        '''


        if action == 0:
            print('haha0')
            try:

                found_something = False

                if self.supply_left < 4:
                    # build pylons

                    if self.already_pending(UnitTypeId.PYLON) == 0:
                        if self.can_afford(UnitTypeId.PYLON):
                            await self.build(UnitTypeId.PYLON, near=random.choice(self.townhalls))
                            found_some = True

                if not found_something:

                    for nexus in self.townhalls:
                        # how many worker for this nexus

                        worker_count = len(self.workers.closer_than(10, nexus))

                        if worker_count < 22:
                            if nexus.is_idle and self.can_afford(UnitTypeId.PROBE):
                                nexus.train(UnitTypeId.PROBE)
                                found_something = True

                        # do we have enough assimilators?
                        # find geysers

                        for geyser in self.vespene_geyser.closer_than(10, nexus):
                            # built one if there is no near
                            if not self.can_afford(UnitTypeId.ASSIMILATOR):
                                break

                            if not self.structures(UnitTypeId.ASSIMILATOR).closer_than(2, geyser).exists:
                                await self.build(UnitTypeId.ASSIMILATOR, geyser)
                                found_something = True
                if not found_something:
                    if self.already_pending(UnitTypeId.NEXUS) == 0 and self.can_afford(UnitTypeId.NEXUS):
                        await self.expand_now()

            except Exception as e:
                print(str(e))
                print('action 0 exception')



        elif action == 1:
            print('haha1')
            try:
                # check if all nexuses and buildings are close

                for nexus in self.townhalls:
                    # build gateway
                    if not self.structures(UnitTypeId.GATEWAY).closer_than(10, nexus).exists:
                        if self.can_afford(UnitTypeId.GATEWAY) and  self.already_pending(UnitTypeId.GATEWAY) == 0:
                            await self.build(UnitTypeId.GATEWAY, near=nexus)

                    # build cybernetics core
                    if not self.structures(UnitTypeId.CYBERNETICSCORE).closer_than(10, nexus).exists:
                        if self.can_afford(UnitTypeId.CYBERNETICSCORE) and  self.already_pending(UnitTypeId.CYBERNETICSCORE) == 0:
                            await self.build(UnitTypeId.CYBERNETICSCORE, near=nexus)

                    # build shield battery
                    if not self.structures(UnitTypeId.SHIELDBATTERY).closer_than(10, nexus).exists:
                        if self.can_afford(UnitTypeId.SHIELDBATTERY) and self.already_pending(UnitTypeId.SHIELDBATTERY) == 0:
                            await self.build(UnitTypeId.SHIELDBATTERY, near=nexus)

                    # build forge
                    if not self.structures(UnitTypeId.FORGE).exists:
                        if self.can_afford(UnitTypeId.FORGE) and  self.already_pending(UnitTypeId.FORGE) == 0:
                            await self.build(UnitTypeId.FORGE, near=nexus)

                    # build photon cannon
                    if not self.structures(UnitTypeId.PHOTONCANNON).closer_than(10, nexus).exists:
                        if self.can_afford(UnitTypeId.PHOTONCANNON) and self.already_pending(UnitTypeId.PHOTONCANNON) == 0:
                            await self.build(UnitTypeId.PHOTONCANNON, near=nexus)

                    # build twilight council
                    if not self.structures(UnitTypeId.TWILIGHTCOUNCIL).exists:
                        if self.can_afford(UnitTypeId.TWILIGHTCOUNCIL) and self.already_pending(UnitTypeId.TWILIGHTCOUNCIL) == 0:
                            await self.build(UnitTypeId.TWILIGHTCOUNCIL, near=nexus)

                    # build stargate
                    if not self.structures(UnitTypeId.STARGATE).closer_than(10, nexus).exists:
                        if self.can_afford(UnitTypeId.STARGATE) and  self.already_pending(UnitTypeId.STARGATE) == 0:
                            await self.build(UnitTypeId.STARGATE, near=nexus)

                    # build robotics facility
                    if not self.structures(UnitTypeId.ROBOTICSFACILITY).closer_than(10, nexus).exists:
                        if self.can_afford(UnitTypeId.ROBOTICSFACILITY) and self.already_pending(UnitTypeId.ROBOTICSFACILITY) == 0:
                            await self.build(UnitTypeId.ROBOTICSFACILITY, near=nexus)

                    # build templar archive
                    if not self.structures(UnitTypeId.TEMPLARARCHIVE).exists:
                        if self.can_afford(UnitTypeId.TEMPLARARCHIVE) and self.already_pending(UnitTypeId.TEMPLARARCHIVE) == 0:
                            await self.build(UnitTypeId.TEMPLARARCHIVE, near=nexus)

                    # build dark shrine
                    if not self.structures(UnitTypeId.DARKSHRINE).closer_than(10, nexus).exists:
                        if self.can_afford(UnitTypeId.DARKSHRINE) and self.already_pending(UnitTypeId.DARKSHRINE) == 0:
                            await self.build(UnitTypeId.DARKSHRINE, near=nexus)

                    # build robotics bay
                    if not self.structures(UnitTypeId.ROBOTICSBAY).exists:
                        if self.can_afford(UnitTypeId.ROBOTICSBAY) and self.already_pending(UnitTypeId.ROBOTICSBAY) == 0:
                            await self.build(UnitTypeId.ROBOTICSBAY, near=nexus)

                    # build fleet beacon
                    if not self.structures(UnitTypeId.FLEETBEACON).closer_than(10, nexus).exists:
                        if self.can_afford(UnitTypeId.FLEETBEACON) and self.already_pending(UnitTypeId.FLEETBEACON) == 0:
                            await self.build(UnitTypeId.FLEETBEACON, near=nexus)



            except Exception as e:
                print(str(e))
                print('action 1 exception')



        elif action == 2:
            print('haha2')
            try:
                # build mothership
                if self.can_afford(UnitTypeId.MOTHERSHIP) and self.structures(UnitTypeId.FLEETBEACON).ready.exists:
                    for i in self.structures(UnitTypeId.NEXUS).ready.idle:
                        i.train(UnitTypeId.MOTHERSHIP)



                # build zealot
                if self.can_afford(UnitTypeId.ZEALOT):
                    for i in self.structures(UnitTypeId.GATEWAY).ready.idle:
                        i.train(UnitTypeId.ZEALOT)

                # build stalker
                if self.can_afford(UnitTypeId.STALKER):
                    for i in self.structures(UnitTypeId.GATEWAY).ready.idle:
                        i.train(UnitTypeId.STALKER)

                # build sentry
                if self.can_afford(UnitTypeId.SENTRY):
                    for i in self.structures(UnitTypeId.GATEWAY).ready.idle:
                        i.train(UnitTypeId.SENTRY)

                # build adept
                if self.can_afford(UnitTypeId.ADEPT):
                    for i in self.structures(UnitTypeId.GATEWAY).ready.idle:
                        i.train(UnitTypeId.ADEPT)

                # build high templar
                if self.can_afford(UnitTypeId.HIGHTEMPLAR):
                    for i in self.structures(UnitTypeId.GATEWAY).ready.idle:
                        i.train(UnitTypeId.HIGHTEMPLAR)

                # build dark templar
                if self.can_afford(UnitTypeId.DARKTEMPLAR):
                    for i in self.structures(UnitTypeId.GATEWAY).ready.idle:
                        i.train(UnitTypeId.DARKTEMPLAR)



                # build phoenix
                if self.can_afford(UnitTypeId.PHOENIX):
                    for i in self.structures(UnitTypeId.STARGATE).ready.idle:
                        i.train(UnitTypeId.PHOENIX)

                # build oracle
                if self.can_afford(UnitTypeId.ORACLE):
                    for i in self.structures(UnitTypeId.STARGATE).ready.idle:
                        i.train(UnitTypeId.ORACLE)

                # build voidray
                if self.can_afford(UnitTypeId.VOIDRAY):
                    for i in self.structures(UnitTypeId.STARGATE).ready.idle:
                        i.train(UnitTypeId.VOIDRAY)

                # build tempest
                if self.can_afford(UnitTypeId.TEMPEST):
                    for i in self.structures(UnitTypeId.STARGATE).ready.idle:
                        i.train(UnitTypeId.TEMPEST)

                # build carrier
                if self.can_afford(UnitTypeId.CARRIER):
                    for i in self.structures(UnitTypeId.STARGATE).ready.idle:
                        i.train(UnitTypeId.CARRIER)



                # build immortal
                if self.can_afford(UnitTypeId.IMMORTAL):
                    for i in self.structures(UnitTypeId.ROBOTICSFACILITY).ready.idle:
                        i.train(UnitTypeId.IMMORTAL)

                # build colossus
                if self.can_afford(UnitTypeId.COLOSSUS):
                    for i in self.structures(UnitTypeId.ROBOTICSFACILITY).ready.idle:
                        i.train(UnitTypeId.COLOSSUS)

                # build disruptor
                if self.can_afford(UnitTypeId.DISRUPTOR):
                    for i in self.structures(UnitTypeId.ROBOTICSFACILITY).ready.idle:
                        i.train(UnitTypeId.DISRUPTOR)

                # build warp prism
                if self.can_afford(UnitTypeId.WARPPRISM):
                    for i in self.structures(UnitTypeId.ROBOTICSFACILITY).ready.idle:
                        i.train(UnitTypeId.WARPPRISM)



            except Exception as e:
                print(str(e))
                print('action 2 exception')



        elif action == 3:
            print('haha3')
            try:
                self.last_sent

            except:
                self.last_sent = 0

            if (iteration - self.last_sent) > 200:
                try:
                    if self.units(UnitTypeId.PROBE).idle.exists:
                        probe = random.choice(self.units(UnitTypeId.PROBE).idle)

                    else:
                        probe = random.choice(self.units(UnitTypeId.PROBE))

                    probe.attack(self.enemy_start_locations[0])
                    self.last_sent = iteration

                except Exception as e:
                    print(str(e))
                    print('action 3 exception')



        elif action == 4:
            print('haha4')
            try:

                for unit_type in fighters:
                    units = self.units(unit_type).idle

                    if units.exists:
                        units.attack(random.choice(self.enemy_start_locations))

            except Exception as e:
                print(str(e))
                print('action 4 exception')



        elif action == 5:
            print('haha5')
            try:
                for unit_type in fighters:
                    units = self.units(unit_type)

                    if units.exists:
                        units.move(self.start_location)

            except Exception as e:
                print(str(e))
                print('action 5 exception')

        map = np.zeros((224, 224, 3), dtype=np.uint8)

        # draw the minerals:
        for mineral in self.mineral_field:
            pos = mineral.position
            c = [175, 255, 255]
            fraction = mineral.mineral_contents / 1800
            if mineral.is_visible:
                # print(mineral.mineral_contents)
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]
            else:
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [20, 75, 50]

                # draw the enemy start location:
        for enemy_start_location in self.enemy_start_locations:
            pos = enemy_start_location
            c = [0, 0, 255]
            map[math.ceil(pos.y)][math.ceil(pos.x)] = c

        # draw the enemy units:
        for enemy_unit in self.enemy_units:
            pos = enemy_unit.position
            c = [100, 0, 255]
            # get unit health fraction:
            fraction = enemy_unit.health / enemy_unit.health_max if enemy_unit.health_max > 0 else 0.0001
            map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]

        # draw the enemy structures:
        for enemy_structure in self.enemy_structures:
            pos = enemy_structure.position
            c = [0, 100, 255]
            # get structure health fraction:
            fraction = enemy_structure.health / enemy_structure.health_max if enemy_structure.health_max > 0 else 0.0001
            map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]

        # draw our structures:
        for our_structure in self.structures:
            # if it's a nexus:
            if our_structure.type_id == UnitTypeId.NEXUS:
                pos = our_structure.position
                c = [255, 255, 175]
                # get structure health fraction:
                fraction = our_structure.health / our_structure.health_max if our_structure.health_max > 0 else 0.0001
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]

            else:
                pos = our_structure.position
                c = [0, 255, 175]
                # get structure health fraction:
                fraction = our_structure.health / our_structure.health_max if our_structure.health_max > 0 else 0.0001
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]

        # draw the vespene geysers:
        for vespene in self.vespene_geyser:
            # draw these after buildings, since assimilators go over them.
            # tried to denote some way that assimilator was on top, couldnt
            # come up with anything. Tried by positions, but the positions arent identical. ie:
            # vesp position: (50.5, 63.5)
            # bldg positions: [(64.369873046875, 58.982421875), (52.85693359375, 51.593505859375),...]
            pos = vespene.position
            c = [255, 175, 255]
            fraction = vespene.vespene_contents / 2250

            if vespene.is_visible:
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]
            else:
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [50, 20, 75]

        # draw our units:
        for our_unit in self.units:
            # if it is a voidray:
            if our_unit.type_id == UnitTypeId.VOIDRAY:
                pos = our_unit.position
                c = [255, 75, 75]
                # get health:
                fraction = our_unit.health / our_unit.health_max if our_unit.health_max > 0 else 0.0001
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]


            else:
                pos = our_unit.position
                c = [175, 255, 0]
                # get health:
                fraction = our_unit.health / our_unit.health_max if our_unit.health_max > 0 else 0.0001
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]

        # show map with opencv, resized to be larger:
        # horizontal flip:

        cv2.imshow('map', cv2.flip(cv2.resize(map, None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST), 0))
        cv2.waitKey(1)

        if SAVE_REPLAY:
            # save map image into "replays dir"
            cv2.imwrite(f"replays/{int(time.time())}-{iteration}.png", map)

        reward = 0

        try:
            attack_count = 0
            # iterate through our void rays:
            for voidray in self.units(UnitTypeId.VOIDRAY):
                # if voidray is attacking and is in range of enemy unit:
                if voidray.is_attacking and voidray.target_in_range:
                    if self.enemy_units.closer_than(8, voidray) or self.enemy_structures.closer_than(8, voidray):
                        # reward += 0.005 # original was 0.005, decent results, but let's 3x it.
                        reward += 0.015
                        attack_count += 1

        except Exception as e:
            print("reward", e)
            reward = 0

        if iteration % 100 == 0:
            print(f"Iter: {iteration}. RWD: {reward}. VR: {self.units(UnitTypeId.VOIDRAY).amount}")

        # write the file:
        data = {"state": map, "reward": reward, "action": None, "done": False}  # empty action waiting for the next one!

        with open('state_rwd_action.pkl', 'wb') as f:
            pickle.dump(data, f)


result = run_game(  # run_game is a function that runs the game.
    maps.get("ProximaStationLE"),  # the map we are playing on
    [Bot(Race.Protoss, sc2Bot()),  # runs our coded bot, protoss race, and we pass our bot object
     Computer(Race.Zerg, Difficulty.Hard)],  # runs a pre-made computer agent, zerg race, with a hard difficulty.
    realtime=False,  # When set to True, the agent is limited in how long each step can take to process.
)

if str(result) == "Result.Victory":
    rwd = 500
else:
    rwd = -500

with open("results.txt", "a") as f:
    f.write(f"{result}\n")

map = np.zeros((224, 224, 3), dtype=np.uint8)
observation = map
data = {"state": map, "reward": rwd, "action": None, "done": True}  # empty action waiting for the next one!
with open('state_rwd_action.pkl', 'wb') as f:
    pickle.dump(data, f)

cv2.destroyAllWindows()
cv2.waitKey(1)
time.sleep(3)
sys.exit()
