import struct

from bxcommon import constants
from bxcommon.messages.message import Message
from bxcommon.utils import logger
from bxcommon.utils.object_hash import ObjectHash


class TxsMessage(Message):
    """
    Message with tx details. Reply to GetTxsMessage.
    """

    def __init__(self, txs=None, buf=None):

        """
        Constructor. Expects list of transaction details or message bytes.

        :param txs: tuple with 3 values (tx short id, tx hash, tx contents)
        :param buf: message bytes
        """

        if buf is None:
            buf = self._txs_to_bytes(txs)
            super(TxsMessage, self).__init__('txs', len(buf) - constants.HDR_COMMON_OFF, buf)
        else:
            if isinstance(buf, str):
                raise TypeError("Buffer can't be string")

            self.buf = buf
            self._memoryview = memoryview(self.buf)
            self._txs = None

    def get_txs(self):
        if self._txs is None:
            self._parse()

        return self._txs

    def _txs_to_bytes(self, txs_details):

        tx_count = len(txs_details)

        # msg_size = HDR_COMMON_OFF + tx count + (sid + hash + tx size) of each tx
        msg_size \
            = constants.HDR_COMMON_OFF + constants.UL_INT_SIZE_IN_BYTES + \
              tx_count * (constants.UL_INT_SIZE_IN_BYTES + constants.SHA256_HASH_LEN + constants.UL_INT_SIZE_IN_BYTES)

        # msg_size += size of each tx
        for tx_info in txs_details:
            msg_size += len(tx_info[2])

        buf = bytearray(msg_size)
        off = constants.HDR_COMMON_OFF

        struct.pack_into('<L', buf, off, len(txs_details))
        off += constants.UL_INT_SIZE_IN_BYTES

        for tx_info in txs_details:
            struct.pack_into('<L', buf, off, tx_info[0])
            off += constants.UL_INT_SIZE_IN_BYTES

            buf[off:off + constants.SHA256_HASH_LEN] = tx_info[1]
            off += constants.SHA256_HASH_LEN

            struct.pack_into('<L', buf, off, len(tx_info[2]))
            off += constants.UL_INT_SIZE_IN_BYTES

            buf[off:off + len(tx_info[2])] = tx_info[2]
            off += len(tx_info[2])

        return buf

    def _parse(self):
        txs = []

        off = constants.HDR_COMMON_OFF

        txs_count, = struct.unpack_from('<L', self.buf, off)
        off += constants.UL_INT_SIZE_IN_BYTES

        logger.debug("Block recovery: received {0} txs in the message.".format(txs_count))

        for tx_index in range(txs_count):
            tx_sid, = struct.unpack_from('<L', self.buf, off)
            off += constants.UL_INT_SIZE_IN_BYTES

            tx_hash = ObjectHash(self._memoryview[off:off + constants.SHA256_HASH_LEN])
            off += constants.SHA256_HASH_LEN

            tx_size, = struct.unpack_from('<L', self.buf, off)
            off += constants.UL_INT_SIZE_IN_BYTES

            tx = self._memoryview[off:off + tx_size]
            off += tx_size

            txs.append((tx_sid, tx_hash, tx))

        self._txs = txs
