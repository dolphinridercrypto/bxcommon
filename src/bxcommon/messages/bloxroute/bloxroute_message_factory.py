import struct

from bxcommon import constants
from bxcommon.messages.abstract_message_factory import AbstractMessageFactory
from bxcommon.messages.bloxroute.ack_message import AckMessage
from bxcommon.messages.bloxroute.bloxroute_message_type import BloxrouteMessageType
from bxcommon.messages.bloxroute.broadcast_message import BroadcastMessage
from bxcommon.messages.bloxroute.get_txs_message import GetTxsMessage
from bxcommon.messages.bloxroute.hello_message import HelloMessage
from bxcommon.messages.bloxroute.key_message import KeyMessage
from bxcommon.messages.bloxroute.message import Message
from bxcommon.messages.bloxroute.ping_message import PingMessage
from bxcommon.messages.bloxroute.pong_message import PongMessage
from bxcommon.messages.bloxroute.tx_message import TxMessage
from bxcommon.messages.bloxroute.txs_message import TxsMessage
from bxcommon.utils import crypto
from bxcommon.utils.object_hash import ObjectHash


class _BloxrouteMessageFactory(AbstractMessageFactory):
    _MESSAGE_TYPE_MAPPING = {
        BloxrouteMessageType.HELLO: HelloMessage,
        BloxrouteMessageType.ACK: AckMessage,
        BloxrouteMessageType.PING: PingMessage,
        BloxrouteMessageType.PONG: PongMessage,
        BloxrouteMessageType.BROADCAST: BroadcastMessage,
        BloxrouteMessageType.TRANSACTION: TxMessage,
        BloxrouteMessageType.GET_TRANSACTIONS: GetTxsMessage,
        BloxrouteMessageType.TRANSACTIONS: TxsMessage,
        BloxrouteMessageType.KEY: KeyMessage
    }

    def __init__(self):
        super(_BloxrouteMessageFactory, self).__init__()
        self.message_type_mapping = self._MESSAGE_TYPE_MAPPING
        self.base_message_type = Message

    def get_hashed_message_preview_from_input_buffer(self, input_buffer):
        """
        Peeks the hash and network number from hashed messages.
        Currently, only Broadcast messages are supported here.
        TODO: refactor TxMessage + KeyMessage to have network number before content and write message converters
              https://bloxroute.atlassian.net/browse/BX-581
        :param input_buffer
        :return: is full header, message hash, network number, payload length
        """
        hash_header_length = self.base_message_type.HEADER_LENGTH + crypto.SHA256_HASH_LEN + constants.NETWORK_NUM_LEN
        _is_full_message, _command, payload_length = self.get_message_header_preview_from_input_buffer(input_buffer)
        is_full_header = input_buffer.length >= hash_header_length
        if payload_length is None or not is_full_header:
            return False, None, None, None
        else:
            hash_header = input_buffer.peek_message(hash_header_length)

            offset = self.base_message_type.HEADER_LENGTH
            message_hash = hash_header[offset:offset + crypto.SHA256_HASH_LEN]
            offset += crypto.SHA256_HASH_LEN

            network_num, = struct.unpack_from("<L", hash_header[offset:offset + constants.NETWORK_NUM_LEN])
            return is_full_header, ObjectHash(message_hash), network_num, payload_length


bloxroute_message_factory = _BloxrouteMessageFactory()
