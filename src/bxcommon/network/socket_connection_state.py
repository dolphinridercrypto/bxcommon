class SocketConnectionState(object):
    CONNECTING = 0b000000000
    INITIALIZED = 0b000000001
    MARK_FOR_CLOSE = 0b000000010