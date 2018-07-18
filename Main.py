import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR
# from sc2.ids.unit_typeid import NEXUS, PROBE, PYLON  #i can ignore this error

class MyBot(sc2.BotAI):
    async def on_step(self, iteration):
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.build_assim()

    async def build_workers(self):
        for nexus in self.units(NEXUS).ready.noqueue:
            if self.can_afford(PROBE):
                await self.do(nexus.train(PROBE))

    async def build_pylons(self):
        if self.supply_left < 5 and not self.already_pending(PYLON):
            nexuses = self.units(NEXUS).ready
            if nexuses.exists:
                if self.can_afford(PYLON):
                    await self.build(PYLON, near=nexuses.first)

    async def build_assim(self):
        for nexus in self.units(NEXUS).ready:
            vespenes = self.state.vespene_geyser.closer_than(25.0, nexus) #gets all the locations of the geysers within 25 units of the nexus
            for vespene in vespenes:
                if not self.can_afford(ASSIMILATOR):
                    break
                worker = self.select_build_worker(vespene.position) #choose a worker at this position
                if worker is None:
                    break
                if not self.units(ASSIMILATOR).closer_than(1.0, vespene).exists: #if there is no assimilator in the vespene geyser, build a assimilator
                    await self.do(worker.build(ASSIMILATOR, vespene))
                    await self.distribute_workers()



run_game(maps.get("(2)CatalystLE"),[
    Bot(Race.Protoss, MyBot()),
    Computer(Race.Terran, Difficulty.Easy)
    ], realtime=True)
