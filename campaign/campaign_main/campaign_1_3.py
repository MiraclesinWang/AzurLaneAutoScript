from module.campaign.campaign_base import CampaignBase
from module.map.map_base import CampaignMap
from module.map.map_grids import SelectedGrids, RoadGrids
from module.logger import logger
from campaign.campaign_main.campaign_1_1 import Config

MAP = CampaignMap()
MAP.shape = 'F3'
MAP.camera_data = ['C1']
MAP.camera_data_spawn_point = ['C1']
MAP.map_data = """
    ++ ++ ++ -- MB --
    -- ME -- ME -- --
    SP -- ++ -- -- MM
"""
MAP.spawn_data = [
    {'battle': 0, 'enemy': 1, 'mystery': 1},
    {'battle': 1, 'enemy': 1},
    {'battle': 2, 'boss': 1},
]
A1, B1, C1, D1, E1, F1, \
A2, B2, C2, D2, E2, F2, \
A3, B3, C3, D3, E3, F3, \
    = MAP.flatten()


class Campaign(CampaignBase):
    MAP = MAP

    def battle_0(self):
        self.clear_all_mystery()
        return self.battle_default()

    def battle_2(self):
        self.clear_all_mystery()
        return self.clear_boss()
