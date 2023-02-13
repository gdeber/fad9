#!/usr/bin/env python3

import mido
import time
import hexdump
import logging
from . import FadMessages, FadElements

SCENE_LENGTH = 222

class Fad9:

    def __init__(self, portname:str):
        self._inport = mido.open_input(portname)
        self._outport = mido.open_output(portname)
        time.sleep(1)
        self._print_msg()

    def enter_setup(self):
        self._send_msg(FadMessages.HS1)
        self._send_msg(FadMessages.HS2)
        self._receive_one()
        self._receive_one()

    def get_scenes_data(self) -> list:
        self._send_msg(FadMessages.CMD_READ_SCENE)
        self._receive_one()
        self._receive_one()
        _full_data = []
        for scene in range(4):
            scene_data = []
            for i in range(SCENE_LENGTH):
                self._send_msg(FadMessages.CMD_READ_BYTE)
                ans = self._receive_one()
                if (ans is not None):
                    bytar = ans.bytes()
                    if bytar[0] == 0x9b:
                        packed = ( bytar[1] << 4 ) | (bytar[2])
                        scene_data.append(packed)
                    else:
                        logging.debug(f"RECEIVED: {ans.hex()}")

            #_full_data.append(scene_data)
            _full_data+=scene_data
                
            logging.debug([hex(s) for s in scene_data])
            logging.debug("********  END  *********")
            logging.debug(hexdump.hexdump(bytearray(scene_data)))
        return _full_data

    def get_full_dump(self) -> list:
        self._send_msg(FadMessages.CMD_READ_SCENE)
        self._receive_one()
        self._receive_one()
        _full_data = []
        for i in range(0x400):
            self._send_msg(FadMessages.CMD_READ_BYTE)
            ans = self._receive_one()
            if (ans is not None):
                bytar = ans.bytes()
                if bytar[0] == 0x9b:
                    packed = ( bytar[1] << 4 ) | (bytar[2])
                    _full_data.append(packed)
                else:
                    logging.debug(f"RECEIVED: {ans.hex()}")
        return _full_data

    def send_scenes_data(self, scene_data:list):
        if len(scene_data) < 0x400:
            raise ValueError("scene data too small")
        
        self._send_msg(FadMessages.CMD_READ_SCENE)
        self._receive_one()
        for idx, byte_to_send in enumerate(scene_data):
            high, low = byte_to_send >> 4, byte_to_send & 0x0F
            _write_msg = mido.Message.from_bytes([0x90, high, low])
            if idx == 0x200:
                msg = self._receive_one()
                if msg != FadMessages.CMD_READ_SCENE:
                    logging.error(f"message received: {msg.hex()}")
                    logging.error("Expecting Read Scene message")

            elif idx == 0x400:
                if self._receive_one() != FadMessages.CMD_END:
                    logging.error(f"message received: {msg.hex()}")
                    logging.error("Expecting End message")

        logging.info("Done Writing")

    def _print_msg(self):
        while (msg := self._inport.poll()) is not None:
            logging.debug(f"RECEIVED: {msg.hex()}")

    def _receive_one(self):
        msg = self._inport.receive()
        logging.debug(f"RECEIVED: {msg.hex()}")
        return msg

    def _send_msg(self, message):
        logging.debug(f"SEND: {message.hex()}")
        self._outport.send(message)

    def close(self):
        _end = FadMessages.CMD_END
        self._send_msg(_end)
        self._inport.close()
        self._outport.close()