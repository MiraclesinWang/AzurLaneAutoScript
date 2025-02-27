from module.campaign.campaign_base import CampaignBase
from module.map.map_base import CampaignMap
from module.map.map_grids import SelectedGrids, RoadGrids
from module.logger import logger
from campaign.campaign_main.campaign_12_1 import Config as ConfigBase

MAP = CampaignMap()
MAP.shape = 'I7'
MAP.camera_data = ['D2', 'D5', 'F2', 'F5']
MAP.camera_data_spawn_point = ['D2', 'D5']
MAP.map_data = """
    ++ MB ME ME ++ -- ME Me --
    ++ -- Me -- Me -- Me -- ++
    MB ME ++ ME SP ME -- ME ++
    MB __ ME -- SP ++ ++ __ Me
    ++ -- -- Me ME -- ME -- ME
    -- ME ME ++ -- -- Me ME --
    ME -- Me -- ME ME -- ++ ++
"""
MAP.weight_data = """
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
"""
MAP.spawn_data = [
    {'battle': 0, 'enemy': 3},
    {'battle': 1, 'enemy': 2},
    {'battle': 2, 'enemy': 1},
    {'battle': 3, 'enemy': 1},
    {'battle': 4, 'enemy': 1},
    {'battle': 5},
    {'battle': 6, 'boss': 1},
]
A1, B1, C1, D1, E1, F1, G1, H1, I1, \
A2, B2, C2, D2, E2, F2, G2, H2, I2, \
A3, B3, C3, D3, E3, F3, G3, H3, I3, \
A4, B4, C4, D4, E4, F4, G4, H4, I4, \
A5, B5, C5, D5, E5, F5, G5, H5, I5, \
A6, B6, C6, D6, E6, F6, G6, H6, I6, \
A7, B7, C7, D7, E7, F7, G7, H7, I7, \
    = MAP.flatten()


class Config(ConfigBase):
    ENABLE_AUTO_SEARCH = False


class Campaign(CampaignBase):
    MAP = MAP
    s3_enemy_count = 0

    def check_s3_enemy(self):
        if self.battle_count == 0:
            self.s3_enemy_count = 0
        elif self.battle_count >= 5:
            self.withdraw()

        current = self.map.select(is_enemy=True, enemy_scale=2) \
            .add(self.map.select(is_enemy=True, enemy_scale=1)) \
            .count
        logger.attr('S2_enemy', current)

        if self.s3_enemy_count >= self.config.C122MediumLeveling_LargeEnemyTolerance and current == 0:
            self.withdraw()

    def battle_0(self):
        self.check_s3_enemy()
        if self.clear_enemy(scale=(2,), genre=['light', 'main', 'treasure', 'enemy', 'carrier']):
            return True
        if self.clear_enemy(scale=(1,)):
            return True
        if self.clear_enemy(scale=(3,), genre=['light', 'carrier', 'enemy', 'treasure', 'main']):
            self.s3_enemy_count += 1
            return True

        return self.battle_default()
