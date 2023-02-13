#!/usr/bin/env python3
import struct
from typing import List

class ModButton:
    fmt ='@ccccc'
    def __init__(self, data_bytes):
        fields = struct.unpack(self.fmt, data_bytes)
        (self._type,
        self._beh,
        self._cc,
        self._max,
        self._min) = fields
    
    def __str__(self):
        return ', ' '\n'.join("%s: %s" % item for item in sorted(self.__dict__.items(), key=lambda i: i[0])) 

    def pack(self) -> bytes:
        return struct.pack(fmt, 
        self._type,
        self._beh,
        self._cc,
        self._max,
        self._min)


class TransportButton:
    fmt = '@ccccc'
    def __init__(self, data_bytes):
        fields = struct.unpack(self.fmt, data_bytes)
        (self._type,
        self._cc,
        self._beh,
        self._mmc_id,
        self._mmc_cmd) = fields

    def __str__(self):
        return ', ' '\n'.join("%s: %s" % item for item in sorted(self.__dict__.items(), key=lambda i: i[0])) 

    def pack(self) -> bytes:
        return struct.pack(fmt, 
        self._type,
        self._cc,
        self._beh,
        self._mmc_id,
        self._mmc_cmd)


class Scene:
    fmt = '@c12s5s5s19s9sc9s9s9s9s9sc9sc9sc9sc9s9s9s9s9s18sc5s5s5s5s5s5s'

    def __init__(self, data_bytes):
        fields = struct.unpack(self.fmt, data_bytes)
        (self._scene_channel,
        self._scene_name,
        self._mod1_raw,
        self._mod2_raw,
        self._unknown,
        self._comm_group_cc,
        self._pad,
        self._knobs_ena,
        self._knobs_cc,
        self._knobs_max,
        self._knobs_min,
        self._slide_ena,
        self._slide_pad1,           
        self._slide_cc,
        self._slide_pad2,
        self._slide_max,
        self._slide_pad3,
        self._slide_min,
        self._slide_pad4,
        self._button_type,
        self._button_cc,
        self._button_beh,
        self._button_max,
        self._button_min,
        self._unknown2,
        self._tran_common_cc,
        self._tran1_raw,
        self._tran2_raw,
        self._tran3_raw,
        self._tran4_raw,
        self._tran5_raw,
        self._tran6_raw ) = fields

        self._tran1 = TransportButton(self._tran1_raw)
        self._tran2 = TransportButton(self._tran2_raw)
        self._tran3 = TransportButton(self._tran3_raw)
        self._tran4 = TransportButton(self._tran4_raw)
        self._tran5 = TransportButton(self._tran5_raw)
        self._tran6 = TransportButton(self._tran6_raw)

        self._mod1 = ModButton(self._mod1_raw)
        self._mod2 = ModButton(self._mod2_raw)

    def __str__(self):
        return ', ' '\n'.join("%s: %s" % item for item in sorted(self.__dict__.items(), key=lambda i: i[0])) 

    def pack(self) -> bytes:
        return struct.pack(fmt, 
        self._scene_channel,
        self._scene_name,
        self._mod1.pack(),
        self._mod2.pack(),
        self._unknown,
        self._comm_group_cc,
        self._pad,
        self._knobs_ena,
        self._knobs_cc,
        self._knobs_max,
        self._knobs_min,
        self._slide_ena,
        self._slide_pad1,           
        self._slide_cc,
        self._slide_pad2,
        self._slide_max,
        self._slide_pad3,
        self._slide_min,
        self._slide_pad4,
        self._button_type,
        self._button_cc,
        self._button_beh,
        self._button_max,
        self._button_min,
        self._unknown2,
        self._tran_common_cc,
        self._tran1.pack(),
        self._tran2.pack(),
        self._tran3.pack(),
        self._tran4.pack(),
        self._tran5.pack(),
        self._tran6.pack())

    @classmethod
    def split_scenes(cls, data: list) -> list:
        if len(data) < 0x400:
            raise ValueError("scene data too small")
        for chunk in cls.chunks(data, 222):
            if len(chunk) == 222:
                yield cls(bytes([x for x in chunk]))
        
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]


if __name__ == '__main__':
    with open("result.hex", "rb") as binary_file:
        bytedata = binary_file.read()
        #data =['0x0', '0x53', '0x43', '0x45', '0x4e', '0x45', '0x20', '0x31', '0x0', '0x0', '0x0', '0x0', '0x0', '0x1', '0x0', '0x1', '0x7f', '0x0', '0x1', '0x0', '0x2', '0x7f', '0x0', '0x0', '0xb2', '0xbd', '0x52', '0x6e', '0xe4', '0xfd', '0x19', '0x0', '0x6c', '0x5', '0x1', '0x0', '0x2', '0x2', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x1', '0x1', '0x1', '0x1', '0x1', '0x1', '0x1', '0x1', '0x1', '0xe', '0xf', '0x10', '0x11', '0x12', '0x13', '0x14', '0x15', '0x16', '0x7f', '0x7f', '0x7f', '0x7f', '0x7f', '0x7f', '0x7f', '0x7f', '0x7f', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x1', '0x1', '0x1', '0x1', '0x1', '0x1', '0x1', '0x1', '0x1', '0x64', '0x3', '0x4', '0x5', '0x6', '0x7', '0x8', '0x9', '0xa', '0xb', '0x0', '0x7f', '0x7f', '0x7f', '0x7f', '0x7f', '0x7f', '0x7f', '0x7f', '0x7f', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x6e', '0x1', '0x1', '0x1', '0x1', '0x1', '0x1', '0x1', '0x1', '0x1', '0x17', '0x18', '0x19', '0x1a', '0x1b', '0x1c', '0x1d', '0x1e', '0x1f', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x7f', '0x7f', '0x7f', '0x7f', '0x7f', '0x7f', '0x7f', '0x7f', '0x7f', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x10', '0x1', '0x2f', '0x0', '0x7f', '0x4', '0x1', '0x2d', '0x0', '0x7f', '0x2', '0x1', '0x30', '0x0', '0x7f', '0x3', '0x1', '0x31', '0x0', '0x7f', '0x1', '0x1', '0x2e', '0x0', '0x7f', '0x0', '0x1', '0x2c', '0x0', '0x7f', '0x5' ]
        #bytedata = bytes([int(x,0) for x in data])
        scene = Scene(bytedata)
        print(scene.__dict__)