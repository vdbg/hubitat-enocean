# from enocean.consolelogger import init_logging
import enocean.utils
from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.packet import RadioPacket
from enocean.protocol.constants import PACKET, RORG
import sys
import traceback
import logging
import queue
import logging
from hubitat import Hubitat
from mapper import Mapper, Mapping

class Listener:

    def __init__(self, conf: dict, hubitat: Hubitat, mapper: Mapper) -> None:
        self.port = conf["port"]
        self.hubitat = hubitat
        self.mapper = mapper
        self.pushed:dict[int, int] = dict()


    def handle_packet(self, packet) -> None:
        deviceId_hex = str(packet)[:11]
        deviceId_int = int(deviceId_hex.replace(':',''), 16)
        data = packet.parse_eep(0x02, 0x02)[0]         
        deviceData = packet.parsed[data]
        button = deviceData["value"]        
        mapping: Mapping = self.mapper.get_mapping(deviceId_int, button)
        if mapping:
            self.hubitat.set_switch(mapping.hubitat_id, True)
            logging.info(f"Sent push command to Hubitat id {mapping.hubitat_id} for device {mapping.label}")
            self.pushed[deviceId_int]=mapping.hubitat_id
        else:            
            if button == "Button AI":
                # button released, see what Hubitat id was previously pushed on this device
                hubitat_id = self.pushed.get(deviceId_int, -1)
                if hubitat_id == -1:
                    logging.warn(f"Received button-down signal from EnOcean device {deviceId_int} but didn't record what button was pressed before")
                else:
                    self.hubitat.set_switch(hubitat_id, False)
            else:
                logging.warn(f"Received signal from non-Hubitat mapped EnOcean device {deviceId_int}, button {button}")

    def assemble_radio_packet(self, transmitter_id):
        return RadioPacket.create(
            rorg=RORG.BS4,
            rorg_func=0x20,
            rorg_type=0x01,
            sender=transmitter_id,
            CV=50,
            TMP=21.5,
            ES='true')

    def run(self) -> None: 
        # logging.getLogger('enocean.communicators.Communicator').setLevel(logging.WARN)
        communicator = SerialCommunicator(port=self.port)
        communicator.start()

        if communicator.base_id is not None:
            logging.debug(f"The Base ID of your module is {enocean.utils.to_hex_string(communicator.base_id)}")
            communicator.send(self.assemble_radio_packet(communicator.base_id))

            while communicator.is_alive():
                try:
                    packet = communicator.receive.get(block=True, timeout=1)
                    if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.RPS:
                        self.handle_packet(packet)
                    else:
                        logging.debug(f"Ignoring packet {packet}")
                except queue.Empty:
                    continue
                except KeyboardInterrupt:
                    break
                except Exception:
                    logging.error("Failed receiving message")
                    break
        else:
            logging.error(f"Unable to connect using port {self.port}")

        if communicator.is_alive():
            communicator.stop()