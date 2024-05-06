#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import platform
import sys
import logging

from config import Config
from hubitat import Hubitat
from listener import Listener
from mapper import Mapper

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

SUPPORTED_PYTHON_MAJOR = 3
SUPPORTED_PYTHON_MINOR = 7

if sys.version_info < (SUPPORTED_PYTHON_MAJOR, SUPPORTED_PYTHON_MINOR):
    raise Exception(
        f"Python version {SUPPORTED_PYTHON_MAJOR}.{SUPPORTED_PYTHON_MINOR} or later required. Current version: {platform.python_version()}."
    )

try:
    config = Config("config.toml", "hubitat_enocean").load()
    logging.info("HELLOO!")

    main_conf = config["main"]
    logging.getLogger().setLevel(logging.getLevelName(main_conf["log_verbosity"]))

    hubitat = Hubitat(config["hubitat"])
    hubitat.get_all_devices()
    mapper = Mapper(config["mapper"], hubitat)
    listener = Listener(config["enocean"], hubitat, mapper)

    # blocking call
    listener.run()

except Exception as e:
    logging.exception(e)
    exit(1)
