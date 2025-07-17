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
                  
                    #train scvs up to 22 (maximum efficent mining)
                  if ccs.is_idle and self.can_afford(UnitTypeId.SCV) and  ccs.assigned_harvesters < 22:
                    ccs.train(UnitTypeId.SCV)

                    #build first depot at centre of ramp
                  elif not self.structures(UnitTypeId.SUPPLYDEPOT) and self.already_pending(UnitTypeId.SUPPLYDEPOT) == 0:
                        if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                             await self.build(UnitTypeId.SUPPLYDEPOT, self.main_base_ramp.depot_in_middle)

                    #build depot near a cc when about to be supply blocked
                  elif self.already_pending(UnitTypeId.SUPPLYDEPOT) == 0 and self.supply_left <4:
                       if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                            pos = ccs.position.towards(self.enemy_start_locations[0], random.randrange(8, 15))
                            await self.build(UnitTypeId.SUPPLYDEPOT, near=pos)
             
             
             #build 2 barracks after first supply depot           
            if self.can_afford(UnitTypeId.BARRACKS) and self.structures(UnitTypeId.BARRACKS).amount < 2 and self.already_pending(UnitTypeId.BARRACKS) < 2:
              await self.build(UnitTypeId.BARRACKS, near=self.structures(UnitTypeId.SUPPLYDEPOT).first)

            if self.can_afford(UnitTypeId.BARRACKS) and self.structures(UnitTypeId.COMMANDCENTER).amount == 3 and self.structures(UnitTypeId.BARRACKS).amount < 9 and self.already_pending(UnitTypeId.BARRACKS) < 3:
              ccs = self.townhalls.random
              pos = ccs.position.towards(self.enemy_start_locations[0], random.randrange(8, 15))
              await self.build(UnitTypeId.BARRACKS, near=pos)
            
            #expand if can afford, up to 3
            else:  
              if self.can_afford(UnitTypeId.COMMANDCENTER) and self.structures(UnitTypeId.COMMANDCENTER).amount < 3:
                await self.expand_now()
            
            
            #send idle scvs to mine
            for scv in self.workers.idle:
                 cc = self.townhalls.closest_to(scv)
                 mineralfield = self.mineral_field.closest_to(cc)
                 scv.gather(mineralfield)


            #  #build refineries
            # if self.structures(UnitTypeId.BARRACKS) and self.can_afford(UnitTypeId.REFINERY) and self.structures(UnitTypeId.REFINERY).amount < 2 and self.already_pending(UnitTypeId.REFINERY) <= 1:
            #    cc = self.townhalls.closest_to(self.start_location)
            #    vgs: Units = self.vespene_geyser.closer_than(20, cc)
            #    for vg in vgs:
            #         if self.gas_buildings.filter(lambda unit: unit.distance_to(vg) < 1):
            #             break

            #         worker: Unit = self.select_build_worker(vg.position)
            #         if worker is None:
            #             break

            #         worker.build_gas(vg)
            #         break

            #Train marines 
            if self.structures(UnitTypeId.BARRACKS).ready.exists:
                for rax in self.structures(UnitTypeId.BARRACKS).ready.idle:
                    if self.can_afford(UnitTypeId.MARINE):
                        rax.train(UnitTypeId.MARINE)
                  
            #Marine patrols between first and second most recent cc
            if self.units(UnitTypeId.MARINE).exists and self.townhalls.amount > 2:
               ccs = self.townhalls.sorted(lambda cc: cc.tag, reverse=True)
               
               marines = self.units(UnitTypeId.MARINE).idle
               
               p1 = ccs[0].position
               
               p2 = ccs[1].position
               
               patrol = p1 if (iteration // 100) % 2 == 0 else p2
               
               for marine in marines:
                    self.do(marine.attack(patrol))
            elif self.units(UnitTypeId.MARINE).exists and self.townhalls.amount == 2:
                 ccs = self.townhalls.sorted(lambda cc: cc.tag, reverse=True)

                 marines = self.units(UnitTypeId.MARINE).idle

                 p1 = ccs[0].position

                 for marine in marines:
                       self.do(marine.attack(p1))


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