class BtcMessageType(object):
    VERSION = "version"
    VERACK = "verack"
    PING = "ping"
    PONG = "pong"
    GET_ADDRESS = "getaddr"
    ADDRESS = "addr"
    INVENTORY = "inv"
    GET_DATA = "getdata"
    NOT_FOUND = "notfound"
    GET_HEADERS = "getheaders"
    GET_BLOCKS = "getblocks"
    TRANSACTIONS = "tx"
    BLOCK = "block"
    HEADERS = "headers"
    REJECT = "reject"
    SEND_HEADERS = "sendheaders"