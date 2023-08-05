import logging
from typing import Any


class Event:
    def __init__(self, event: dict[str, Any]) -> None:
        self._event = event
        self.current_hp = int(event["hitPoints"])
        self.max_hp = int(event["maxHitPoints"])
        self.heal_amount = int(event["amount"])
        self.hp_before = self.current_hp - self.heal_amount

    def hp_percent(self) -> float:
        if self.hp_before - self.max_hp > 0:
            logging.error("Higher than 100%% HP?? %s", self._event)  # noqa: WPS323
            return 100.0
        return (self.hp_before / self.max_hp) * 100

    def rp(self) -> float:
        return self._event["classResources"][0]["amount"] / 10

    def is_cast_by_player(self) -> bool:
        return self._event["classResources"][0]["max"] != 0
