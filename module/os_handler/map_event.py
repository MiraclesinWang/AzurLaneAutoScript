from module.base.timer import Timer
from module.combat.assets import *
from module.exception import CampaignEnd
from module.handler.assets import *
from module.logger import logger
from module.os.assets import GLOBE_GOTO_MAP
from module.os_handler.assets import *
from module.os_handler.enemy_searching import EnemySearchingHandler
from module.statistics.azurstats import DropImage
from module.ui.switch import Switch

fleet_lock = Switch('Fleet_Lock', offset=(10, 120))
fleet_lock.add_status('on', check_button=OS_FLEET_LOCKED)
fleet_lock.add_status('off', check_button=OS_FLEET_UNLOCKED)


class MapEventHandler(EnemySearchingHandler):
    ash_popup_canceled = False

    def handle_map_get_items(self, interval=2, drop=None):
        if self.is_in_map():
            return False

        if self.appear(GET_ITEMS_1, interval=interval) \
                or self.appear(GET_ITEMS_2, interval=interval) \
                or self.appear(GET_ITEMS_3, interval=interval):
            if drop:
                drop.handle_add(main=self, before=2)
            self.device.click(CLICK_SAFE_AREA)
            return True
        if self.appear(GET_ADAPTABILITY, interval=interval):
            if drop:
                drop.handle_add(main=self, before=2)
            self.device.click(CLICK_SAFE_AREA)
            return True
        if self.appear(GET_MEOWFFICER_ITEMS_1, interval=interval):
            if drop:
                drop.handle_add(main=self, before=2)
            self.device.click(CLICK_SAFE_AREA)
            return True
        if self.appear(GET_MEOWFFICER_ITEMS_2, interval=interval):
            if drop:
                drop.handle_add(main=self, before=2)
            self.device.click(CLICK_SAFE_AREA)
            return True

        return False

    def handle_map_archives(self, drop=None):
        if self.appear(MAP_ARCHIVES, interval=5):
            if drop:
                drop.add(self.device.image)
            self.device.click(CLICK_SAFE_AREA)
            return True
        if self.appear_then_click(MAP_WORLD, offset=(20, 20), interval=5):
            return True

        return False

    def handle_os_game_tips(self):
        # Close game tips the first time enabling auto search
        if self.appear_then_click(OS_GAME_TIPS, offset=(20, 20), interval=3):
            return True

        return False

    def handle_ash_popup(self):
        name = 'ASH'
        # 2021.12.09
        # Ash popup no longer shows red letters, so change it to letter `Ashes Coordinates`
        if self.appear(POPUP_CONFIRM, offset=self._popup_offset) \
                and self.appear(POPUP_CANCEL, offset=self._popup_offset, interval=2) \
                and self.appear(ASH_POPUP_CHECK, offset=(20, 20)):
            POPUP_CANCEL.name = POPUP_CANCEL.name + '_' + name
            self.device.click(POPUP_CANCEL)
            POPUP_CANCEL.name = POPUP_CANCEL.name[:-len(name) - 1]
            self.ash_popup_canceled = True
            return True
        else:
            return False

    def handle_siren_platform(self):
        """
        Handle siren platform notice after entering map

        Returns:
            bool: If handled
        """
        if not self.handle_story_skip():
            return False

        logger.info('Handle siren platform')
        timeout = Timer(self.MAP_ENEMY_SEARCHING_TIMEOUT_SECOND).start()
        appeared = False
        while 1:
            self.device.screenshot()
            if self.is_in_map():
                timeout.start()
            else:
                timeout.reset()

            if self.handle_story_skip():
                timeout.reset()
                continue

            # End
            if self.enemy_searching_appear():
                appeared = True
            else:
                if appeared:
                    self.handle_enemy_flashing()
                    self.device.sleep(1)
                    logger.info('Enemy searching appeared.')
                    break
                self.enemy_searching_color_initial()
            if timeout.reached():
                logger.info('Enemy searching timeout.')
                break

        return True

    def handle_map_event(self, drop=None):
        """
        Args:
            drop (DropImage):

        Returns:
            bool: If clicked to handle any map event.
        """
        if self.handle_map_get_items(drop=drop):
            return True
        if self.handle_os_game_tips():
            return True
        if self.handle_map_archives(drop=drop):
            return True
        if self.handle_guild_popup_cancel():
            return True
        if self.handle_ash_popup():
            return True
        if self.handle_urgent_commission(drop=drop):
            return True
        if self.handle_story_skip():
            return True

        return False

    _os_in_map_confirm_timer = Timer(1.5, count=3)

    def handle_os_in_map(self):
        """
        Returns:
            bool: If is in map and confirmed.
        """
        if self.is_in_map():
            if self._os_in_map_confirm_timer.reached():
                return True
            else:
                return False
        else:
            self._os_in_map_confirm_timer.reset()
            return False

    def ensure_no_map_event(self):
        self._os_in_map_confirm_timer.reset()

        while 1:
            self.device.screenshot()

            if self.handle_map_event():
                continue

            # End
            if self.handle_os_in_map():
                break

    def os_auto_search_quit(self, drop=None, skip_first_screenshot=True):
        """
        Args:
            drop (DropImage):
            skip_first_screenshot (bool):
        """
        confirm_timer = Timer(1, count=2).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if self.appear(AUTO_SEARCH_REWARD, offset=(20, 20), interval=2):
                if drop:
                    drop.handle_add(main=self, before=4)
                self.device.click(AUTO_SEARCH_REWARD)
                self.interval_reset(AUTO_SEARCH_REWARD)
                confirm_timer.reset()
                continue
            if self.handle_map_event():
                confirm_timer.reset()
                continue
            if self.appear_then_click(GLOBE_GOTO_MAP, offset=(20, 20), interval=2):
                # Sometimes entered globe map after clicking AUTO_SEARCH_REWARD, but don't know why
                confirm_timer.reset()
                continue

            # End
            if self.is_in_map():
                if confirm_timer.reached():
                    break
            else:
                confirm_timer.reset()

    def handle_os_auto_search_map_option(self, drop=None, enable=True):
        """
        Args:
            drop (DropImage)
            enable (bool):

        Returns:
            bool: If clicked.
        """
        if self.appear(AUTO_SEARCH_OS_MAP_OPTION_OFF, offset=(5, 120)) \
                and AUTO_SEARCH_OS_MAP_OPTION_OFF.match_appear_on(self.device.image) \
                and self.info_bar_count() >= 2:
            self.device.screenshot_interval_set()
            raise CampaignEnd
        if self.appear(AUTO_SEARCH_REWARD, offset=(50, 50)):
            self.device.screenshot_interval_set()
            self.os_auto_search_quit(drop=drop)
            raise CampaignEnd
        if enable:
            if self.appear(AUTO_SEARCH_OS_MAP_OPTION_OFF, offset=(5, 120), interval=3) \
                    and AUTO_SEARCH_OS_MAP_OPTION_OFF.match_appear_on(self.device.image):
                self.device.click(AUTO_SEARCH_OS_MAP_OPTION_OFF)
                return True
        else:
            if self.appear(AUTO_SEARCH_OS_MAP_OPTION_ON, offset=(5, 120), interval=3) \
                    and AUTO_SEARCH_OS_MAP_OPTION_ON.match_appear_on(self.device.image):
                self.device.click(AUTO_SEARCH_OS_MAP_OPTION_ON)
                return True

        return False

    def handle_os_map_fleet_lock(self, enable=None):
        """
        Args:
            enable (bool): Default to None, use Campaign_UseFleetLock.

        Returns:
            bool: If switched.
        """
        # Fleet lock depends on if it appear on map, not depends on map status.
        # Because if already in map, there's no map status,
        if not fleet_lock.appear(main=self):
            logger.info('No fleet lock option.')
            return False

        if enable is None:
            enable = self.config.Campaign_UseFleetLock
        status = 'on' if enable else 'off'
        changed = fleet_lock.set(status=status, main=self)

        return changed
