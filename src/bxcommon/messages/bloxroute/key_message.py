import struct

from bxcommon.constants import HDR_COMMON_OFF, NETWORK_NUM_LEN
from bxcommon.messages.bloxroute.bloxroute_message_type import BloxrouteMessageType
from bxcommon.messages.bloxroute.message import Message
from bxcommon.utils.crypto import KEY_SIZE, SHA256_HASH_LEN
from bxcommon.utils.object_hash import ObjectHash


class KeyMessage(Message):
    MESSAGE_TYPE = BloxrouteMessageType.KEY

    def __init__(self, msg_hash=None, key=None, network_num=None, buf=None):
        if buf is None:
            assert len(key) == KEY_SIZE
            self.buf = bytearray(HDR_COMMON_OFF + SHA256_HASH_LEN + KEY_SIZE + NETWORK_NUM_LEN)

            off = HDR_COMMON_OFF
            self.buf[off:off + SHA256_HASH_LEN] = msg_hash.binary
            off += SHA256_HASH_LEN
            self.buf[off:off + KEY_SIZE] = key
            off += KEY_SIZE
            struct.pack_into("<L", self.buf, off, network_num)
            off += NETWORK_NUM_LEN

            super(KeyMessage, self).__init__(self.MESSAGE_TYPE, off - HDR_COMMON_OFF, self.buf)
        else:
            assert not isinstance(buf, str)
            self.buf = buf
            self._memoryview = memoryview(self.buf)

        self._key = None
        self._msg_hash = None
        self._network_num = None

    def msg_hash(self):
        if self._msg_hash is None:
            self._msg_hash = ObjectHash(self._memoryview[HDR_COMMON_OFF:HDR_COMMON_OFF + SHA256_HASH_LEN])
        return self._msg_hash

    def key(self):
        if self._key is None:
            off = HDR_COMMON_OFF + SHA256_HASH_LEN
            self._key = self._memoryview[off:off + KEY_SIZE]
        return self._key

    def network_num(self):
        if self._network_num is None:
            off = HDR_COMMON_OFF + SHA256_HASH_LEN + KEY_SIZE
            self._network_num, = struct.unpack_from("<L", self.buf, off)

        return self._network_num