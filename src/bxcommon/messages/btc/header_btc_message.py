import hashlib
import struct

from bxcommon.constants import BTC_BLOCK_HDR_SIZE, BTC_HDR_COMMON_OFF, BTC_SHA_HASH_LEN
from bxcommon.messages.btc.btc_message import BTCMessage
from bxcommon.messages.btc.btc_messages_util import btcvarint_to_int, pack_int_to_btcvarint
from bxcommon.utils.object_hash import BTCObjectHash

sha256 = hashlib.sha256


# A BlockHeader is the first 80 bytes of the corresponding block message payload
# terminated by a null byte (\x00) to signify that there are no services.
# FIXME, there's a lot of duplicate code between here and BlockBTCMessage
class BlockHeader(object):
    def __init__(self, buf=None, version=None, prev_block=None, merkle_root=None,
                 timestamp=None, bits=None, nonce=None):
        if buf is None:
            buf = bytearray(81)
            self.buf = buf
            off = 0
            struct.pack_into('<I', buf, off, version)
            off += 4
            buf[off:off + 32] = prev_block.get_little_endian()
            off += 32
            buf[off:off + 32] = merkle_root.get_little_endian()
            off += 32
            struct.pack_into('<III', buf, off, timestamp, bits, nonce)
        else:
            self.buf = buf
            self._memoryview = memoryview(buf)

        self._version = self._prev_block = self._merkle_root = None
        self._timestamp = self._bits = self._nonce = None
        self._block_hash = None
        self._txn_count = None
        self._hash_val = None

    def version(self):
        if self._version is None:
            off = 0
            self._version = struct.unpack_from('<I', self.buf, off)[0]
            off += 4
            self._prev_block = BTCObjectHash(self.buf, off, 32)
            off += 32
            self._merkle_root = self._memoryview[off:off + 32]
            off += 32
            self._timestamp, self._bits, self._nonce = struct.unpack_from('<III', self.buf, off)
            self._txn_count, size = btcvarint_to_int(self.buf, off)
        return self._version

    def prev_block(self):
        if self._version is None:
            self.version()
        return self._prev_block

    def merkle_root(self):
        if self._version is None:
            self.version()
        return self._merkle_root

    def timestamp(self):
        if self._version is None:
            self.version()
        return self._timestamp

    def bits(self):
        if self._version is None:
            self.version()
        return self._bits

    def nonce(self):
        if self._version is None:
            self.version()
        return self._nonce

    def block_hash(self):
        if self._block_hash is None:
            header = self._memoryview[:BTC_BLOCK_HDR_SIZE - 1]  # remove the tx count at the end
            raw_hash = sha256(sha256(header).digest()).digest()
            self._hash_val = BTCObjectHash(buf=raw_hash, length=BTC_SHA_HASH_LEN)
        return self._hash_val


class HeadersBTCMessage(BTCMessage):
    def __init__(self, magic=None, headers=None, buf=None):
        if buf is None:
            buf = bytearray(BTC_HDR_COMMON_OFF + 9 + len(headers) * 81)
            self.buf = buf

            off = BTC_HDR_COMMON_OFF
            off += pack_int_to_btcvarint(len(headers), buf, off)
            for header in headers:
                buf[off:off + 81] = header
                off += 81

            BTCMessage.__init__(self, magic, 'headers', off - BTC_HDR_COMMON_OFF, buf)
        else:
            self.buf = buf
            self._memoryview = memoryview(self.buf)
            self._magic = self._command = self._payload_len = self._checksum = None
            self._payload = None

        self._headers = self._header_count = self._block_hash = None

    def hash_count(self):
        if self._header_count is None:
            raise RuntimeError('FIXME')
            # FIXME buf is undefined, change to self.buf and test
            # off = BTC_HDR_COMMON_OFF
            # self._header_count, size = btcvarint_to_int(buf, off)

        return self._header_count

    def __iter__(self):
        raise RuntimeError('FIXME')
        # FIXME buf is undefined, change to self.buf and test
        # off = BTC_HDR_COMMON_OFF
        # self._header_count, size = btcvarint_to_int(buf, off)
        # off += size
        # for _ in xrange(self._header_count):
        #     yield self._memoryview[off:off + 81]
        #     off += 81