#SC2 Python Bot
# cd sc2pythonbot/python-sc2/
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
from sc2.player import Bot, Human

class BtechHeroMarine(BotAI):
    async def on_step(self, iteration:int):
            print(f"The Iteration is {iteration}")

            if self.townhalls:
                  cc = self.townhalls.closest_to(self.start_location)
                  ccs = self.townhalls.random
                  

                  if ccs.is_idle and self.can_afford(UnitTypeId.SCV) and  ccs.assigned_harvesters < 22:
                    ccs.train(UnitTypeId.SCV)
                  elif not self.structures(UnitTypeId.SUPPLYDEPOT) and self.already_pending(UnitTypeId.SUPPLYDEPOT) == 0:
                        if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                             await self.build(UnitTypeId.SUPPLYDEPOT, self.main_base_ramp.depot_in_middle)
                  elif self.already_pending(UnitTypeId.SUPPLYDEPOT) == 0 and self.supply_left <4:
                       if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                            target_depot = self.structures(UnitTypeId.SUPPLYDEPOT).closest_to(ccs)
                            pos = ccs.position.towards(self.enemy_start_locations[0], random.randrange(8, 15))
                            await self.build(UnitTypeId.SUPPLYDEPOT, near=pos)
                        
            if self.can_afford(UnitTypeId.BARRACKS) and self.structures(UnitTypeId.BARRACKS).amount < 2 and self.already_pending(UnitTypeId.BARRACKS) < 2:
                        await self.build(UnitTypeId.BARRACKS, near=self.structures(UnitTypeId.SUPPLYDEPOT).first)
            
            
            else:  
                  if self.can_afford(UnitTypeId.COMMANDCENTER) and self.structures(UnitTypeId.COMMANDCENTER).amount < 3:
                        await self.expand_now()
            
            for scv in self.workers.idle:
                 cc = self.townhalls.closest_to(scv)
                 mineralfield = self.mineral_field.closest_to(cc)
                 scv.gather(mineralfield)


            if self.structures(UnitTypeId.BARRACKS).ready.exists:
                for rax in self.structures(UnitTypeId.BARRACKS).ready.idle:
                    if self.can_afford(UnitTypeId.MARINE):
                        rax.train(UnitTypeId.MARINE)
                  
          
            if self.units(UnitTypeId.MARINE).exists :
               protect = ccs.position
               marines = self.units(UnitTypeId.MARINE)
               for marine in marines:
                    self.do(marine.move(protect)) 


class Humanish(BotAI):
     async def on_step(self, iteration:int):
        print(f"I am a Human!!!")
     


run_game(
    maps.get("AutomatonLE"),
    [Bot(Race.Terran, BtechHeroMarine()),
     Computer(Race.Protoss, Difficulty.Hard)],
     realtime=False
)


# run_game(
#     maps.get("AutomatonLE"),
#     [Bot(Race.Terran, Humanish()),
#      Bot(Race.Terran, BtechHeroMarine())],
#      realtime=True
#      )