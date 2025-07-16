#SC2 Python Bot
# cd sc2pythonbot/python-sc2
# python3 .\sc2pythonbot1.py
# $env:SC2PATH="D:\StarCraft II"

# cd sc2pythonbot/python-sc2 ; $env:SC2PATH="D:\StarCraft II" ; python3 .\sc2pythonbot1.py

#Place this into powershell

from sc2.bot_ai import BotAI # Parent AI class you inherit from
from sc2.data import Difficulty, Race
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2 import maps
from sc2.ids.unit_typeid import UnitTypeId
import random

class BtechHeroMarine(BotAI):
    async def on_step(self, iteration:int):
            print(f"The Iteration is {iteration}")

            if self.townhalls:
                  cc = self.townhalls.closest_to(self.start_location)
                  

                  if cc.is_idle and self.can_afford(UnitTypeId.SCV) and  cc.assigned_harvesters < 18:
                    cc.train(UnitTypeId.SCV)
                  elif not self.structures(UnitTypeId.SUPPLYDEPOT) and self.already_pending(UnitTypeId.SUPPLYDEPOT) == 0:
                        if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                             await self.build(UnitTypeId.SUPPLYDEPOT, self.main_base_ramp.depot_in_middle)
                  elif self.structures(UnitTypeId.SUPPLYDEPOT).amount <5:
                       if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                            target_depot = self.structures(UnitTypeId.SUPPLYDEPOT).closest_to(self.enemy_start_locations[0])
                            pos = target_depot.position.towards(cc, random.randrange(8, 15))
                            await self.build(UnitTypeId.SUPPLYDEPOT, near=pos)
                        
            
            
            
            else:  
                  if self.can_afford(UnitTypeId.COMMANDCENTRE):
                        await self.expand_now()
            
            for scv in self.workers.idle:
                 cc = self.townhalls.closest_to(scv)
                 mineralfield = self.mineral_field.closest_to(cc)
                 scv.gather(mineralfield) 
run_game(
    maps.get("AutomatonLE"),
    [Bot(Race.Terran, BtechHeroMarine()),
     Computer(Race.Protoss, Difficulty.Hard)],
     realtime=True
)