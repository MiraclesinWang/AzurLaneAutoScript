from ..campaign_war_archives.campaign_base import CampaignBase
from module.map.map_base import CampaignMap
from module.map.map_grids import SelectedGrids, RoadGrids
from module.logger import logger
from .c1 import Config as ConfigBase

MAP = CampaignMap('C3')
MAP.shape = 'I7'
MAP.camera_data = ['D2', 'D5', 'F2', 'F5']
MAP.camera_data_spawn_point = ['F2']
MAP.map_data = """
    -- -- -- MS -- -- SP ++ ++
    Me -- -- -- ++ -- -- ++ ++
    -- ME ME ME ++ -- -- -- SP
    -- -- -- __ -- -- -- -- --
    -- MS Me -- MB -- ++ ++ --
    -- -- ++ MS -- -- -- -- MS
    -- ME ++ -- MB -- ME -- --
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
    {'battle': 0, 'enemy': 2, 'siren': 2},
    {'battle': 1, 'enemy': 1, 'siren': 1},
    {'battle': 2, 'enemy': 2, 'siren': 1},
    {'battle': 3, 'enemy': 1},
    {'battle': 4, 'enemy': 2},
    {'battle': 5, 'enemy': 1, 'boss': 1},
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
    # ===== Start of generated config =====
    MAP_SIREN_TEMPLATE = ['Swordfish']
    MOVABLE_ENEMY_TURN = (1,)
    MAP_HAS_SIREN = True
    MAP_HAS_MOVABLE_ENEMY = True
    MAP_HAS_MAP_STORY = False
    MAP_HAS_FLEET_STEP = True
    MAP_HAS_AMBUSH = False
    # ===== End of generated config =====

    STAR_REQUIRE_3 = 0
    MAP_SWIPE_MULTIPLY = 1.626
    MAP_SWIPE_MULTIPLY_MINITOUCH = 1.572


class Campaign(CampaignBase):
    MAP = MAP

    def get_map_clear_percentage(self):
        """
        map clear here is shorter than normal, about 70% at max

        Returns:
            float: 0 to 1.
        """
        return super().get_map_clear_percentage() * 1.4

    def battle_0(self):
        if not self.map_is_clear_mode:
            for grid in self.map:
                grid.may_siren = True

        if self.clear_siren():
            return True

        return self.battle_default()

    def battle_5(self):
        return self.fleet_boss.clear_boss()
