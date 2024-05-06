# support annotations in older versions of Python
from __future__ import annotations

import logging

# https://github.com/danielorf/pyhubitat
from pyhubitat import MakerAPI

class Device:
    def __init__(self, conf: dict) -> None:
        self.name: str = f"'{conf['label']}' ({conf['id']})"

    def __str__(self) -> str:
        return self.name


class Hubitat:
    def __init__(self, conf: dict):
        hub = f"{conf['url'].rstrip('/')}/apps/api/{conf['app_id']}"
        logging.info(f"Connecting to hubitat Maker API app {hub}")
        self._api = MakerAPI(conf["token"], hub)
        self._devices_cache: dict[int, Device] = None

    def has_device(self, id: int) -> bool:
        return id in self._devices_cache

    def get_all_devices(self) -> dict[int, Device]:
        if self._devices_cache is None:
            logging.debug("Refreshing all devices cache")
            all_devices = self._api.list_devices_detailed()
            try:
                self._devices_cache = {
                    int(x["id"]): Device(x)
                    for x in all_devices
                    if x["type"] == "Virtual Switch"
                }
            except Exception:
                raise Exception(f"Unable to load the list of devices using Hubitat's response: {all_devices}")
            for device in self._devices_cache.values():
                logging.info(f"Found Hubitat virtual switch device {device}.")

        return self._devices_cache

    def set_switch(self, id: int, on: bool) -> None:
        command: str = "on" if on else "off"
        device: Device = self._devices_cache[id]
        logging.info(f"Sending command {command} to Hubitat device {device}")
        self._api.send_command(id, command)
