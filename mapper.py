# support annotations in older versions of Python
from __future__ import annotations

import logging
from hubitat import Hubitat

class Mapping:
    def __init__(self, enocean_id: int, enocean_button: str, label: str, hubitat_id: int) -> None:
        self.enocean_id = enocean_id
        self.enocean_button = enocean_button
        self.label = label
        self.hubitat_id = hubitat_id

# Maps an EnOcean button to a Hubitat virtual device
class Mapper:

    def __init__(self, conf: list[dict], hubitat: Hubitat) -> None:
        self._mapping: dict[str, Mapping] = dict()
        for label, entry in conf.items():
            mapping = Mapping(int(entry['enocean_id']), entry['enocean_button'], label, int(entry['hubitat_id']))
            key = self.get_key(mapping.enocean_id, mapping.enocean_button)
            name = f"{key};name={mapping.label}"
            if hubitat.has_device(mapping.hubitat_id):
                logging.debug(f"Mapping EnOcean {name} to Hubitat Id {mapping.hubitat_id}")
                self._mapping[key] = mapping
            else:
                logging.warn(f"Cannot map EnOcean {name} to Hubitat Id {mapping.hubitat_id} as device not exposed to MakerAPI")

    def get_key(self, id: int, button: str) -> str:
        return f"id={id};button={button}"

    def get_mapping(self, id: int, button: str) -> Mapping:        
        return self._mapping.get(self.get_key(id, button), None)
        

