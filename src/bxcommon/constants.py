from bxcommon.utils import cli

MAX_CONN_BY_IP = 30  # Maximum number of connections that an IP address can have

CONNECTION_TIMEOUT = 3  # Number of seconds that we wait to retry a connection.
MAX_CONNECT_RETRIES = 3
RETRY_BLOCKCHAIN_CONNECT_FOREVER = True

# Number of bad messages I'm willing to receive in a row before declaring the input stream
# corrupt beyond repair.
MAX_BAD_MESSAGES = 3

# Number of tries to connect to a peer on startup
NET_ADDR_INIT_CONNECT_TRIES = 3
NET_ADDR_INIT_CONNECT_RETRY_INTERVAL_SECONDS = 2

# The size of the recv buffer that we fill each time.
RECV_BUFSIZE = 8192

CONNECTION_RETRY_SECONDS = 5  # Seconds to wait before retrying connection.

SINK_TIMEOUT_SECONDS = 60  # Seconds timeout for the sink

# Number of messages that can be cut through at a time
MAX_CUT_THROUGH_SEND_QUEUE = 5000

# Number of messages that can be kept in the history at a time.
# Two identical messages that are broadcast more than MAX_MESSAGE_HISTORY messages apart
# will both be cut through broadcast.
MAX_MESSAGE_HISTORY = 5000

# True if we want to avoid doing the database puts
FAKE_DB = False

# True if we want to take heap profiles
PROFILING = False

# negative if we are never going to crash
# Otherwise, it's the number of seconds until this bloxroute node
# will crash.
CRASH_INTERVAL = -1

LOG_FOR_WEB = True

ENABLE_LOGGING = True

# If the peer is more this many blocks behind me, then we close the connection.
# This is useful to change for testing so that we can test tranfer rates for large numbers of blocks.
HEIGHT_DIFFERENCE = 100

FLUSH_LOG = True

LISTEN_ON_IP_ADDRESS = '0.0.0.0'

# The length of everything in the header minus the checksum
HDR_COMMON_OFF = 16

# Length of a sha256 hash
SHA256_HASH_LEN = 32

# Size of integer in bytes
UL_INT_SIZE_IN_BYTES = 4  # If changing here, also change in bxapi/constants.py

# Expiration time for block broadcast message if services info is missing
MISSING_BLOCK_EXPIRE_TIME = 60

btc_magic_numbers = {
    'main': 0xD9B4BEF9,
    'testnet': 0xDAB5BFFA,
    'testnet3': 0x0709110B,
    'regtest': 0xDAB5BFFA,
    'namecoin': 0xFEB4BEF9
}

# The length of everything in the header minus the checksum
BTC_HEADER_MINUS_CHECKSUM = 20
BTC_HDR_COMMON_OFF = 24
BTC_BLOCK_HDR_SIZE = 81
# Length of a sha256 hash
BTC_SHA_HASH_LEN = 32

# The services that we provide
# 1: can ask for full blocks.
# 0x20: Node that is compatible with the hard fork.
BTC_CASH_SERVICE_BIT = 0x20  # Bitcoin cash service bit
BTC_NODE_SERVICES = 1
BTC_CASH_SERVICES = 33

BTC_OBJTYPE_TX = 1
BTC_OBJTYPE_BLOCK = 2
BTC_OBJTYPE_FILTERED_BLOCK = 3

CUT_THROUGH_TIMEOUT = 60  # Maximum time (in seconds) that we wait for the remote to send us this block
MGR_DELETE_DELAY = 100  # Time (in seconds) we wait until we delete this manager from our node.

MIN_PYLINT_SCORE = 9.5

RELAY_PING_INTERVAL_SEC = 60

# The unsigned integer transaction SID representing null.
NULL_TX_SID = 0  # If changing, also change in bxapi/constants.py

# Unsigned int used for no idx in hello messages from gateways.
NULL_IDX = 0  # If changing, also change in bxapi/constants.

PLATFORM_LINUX = "linux"
PLATFORM_MAC = "darwin"

DEFAULT_SLEEP_TIMEOUT = 0.1  # Schedule an event to be executed fast on alarm queue.

MAX_KQUEUE_EVENTS_COUNT = 1000

BX_API_ROOT_URL = cli.get_args().sdn_url
BX_API_ROUTES = {
    "nodes": BX_API_ROOT_URL + "/nodes",
    "node": BX_API_ROOT_URL + "/nodes/{0}",
    "node_peers": BX_API_ROOT_URL + "/nodes/{0}/peers",
    "node_event": BX_API_ROOT_URL + "/nodes/{0}/events"
}