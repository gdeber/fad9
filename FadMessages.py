import mido

HS1 = mido.Message.from_bytes([0x9b, 0x01, 0x02])
HS2 = mido.Message.from_bytes([0x9b, 0x7e, 0x7d])
RES1 = mido.Message.from_bytes([0x9b, 0x01, 0x32])  # model identification

CMD_READ_SCENE = mido.Message.from_bytes([0x9b, 0x01, 0x04])
CMD_READ_SCENE_2 = mido.Message.from_bytes([0x9b, 0x00, 0x01])

CMD_WRITE_SCENE = mido.Message.from_bytes([0x9b, 0x01, 0x03])
CMD_WRITE_SCENE_2 = mido.Message.from_bytes([0x9b, 0x00, 0x02])

CMD_END = mido.Message.from_bytes([0x9b, 0x01, 0x05])
CMD_READ_BYTE = mido.Message.from_bytes([0x9b, 0x01, 0x06])