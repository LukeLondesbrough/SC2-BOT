#SC2 Python Bot
from sc2.bot_ai import BotAI # Parent AI class you inherit from
from sc2.data import Difficulty, Race
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2 import maps

class WORKERRUSH(BotAI):
    async def on_step(self, iteration:int):
      if iteration == 0 :
            for worker in self.workers:
                worker.attack(self.enemy_start_locations[0])
            print(f"The Iteration is {iteration}")
run_game(
    maps.get("AutomatonLE"),
    [Bot(Race.Terran, WORKERRUSH()),
     Computer(Race.Protoss, Difficulty.Easy)],
     realtime=False
)