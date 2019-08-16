import argparse
import unittest
from unittest import mock
from argparse import Namespace

from bxcommon import node_runner, constants
from bxcommon.connections.node_type import NodeType
from bxcommon.models.blockchain_network_model import BlockchainNetworkModel
from bxcommon.utils import logger, log_level, log_format, config
from bxcommon.models.node_model import NodeModel


class NodeMock(object):
    NODE_TYPE = NodeType.GATEWAY

    def __init__(self, opts: Namespace):
        self.opts: Namespace = opts


class EventLoopMock(object):

    def __init__(self):
        self.run_count = 0

    def run(self, *args, **kwargs):
        self.run_count += 1


class TestNodeRunner(unittest.TestCase):

    def setUp(self):
        self.blockchain_network = BlockchainNetworkModel(
                    protocol="Bitcoin",
                    network="Mainnet",
                    network_num=1,
                    block_interval=600,
                    final_tx_confirmations_count=6
        )
        opts = {
            "log_path": "",
            "to_stdout": True,
            "external_port": 0,
            "node_id": "Test-Node-1",
            "blockchain_network": self.blockchain_network.network,
            "network_num": self.blockchain_network.network_num,
            "blockchain_protocol": self.blockchain_network.protocol,
            "blockchain_networks": [self.blockchain_network],
            "log_level": log_level.LogLevel.INFO,
            "log_format": log_format.LogFormat.PLAIN,
            "log_flush_immediately": True,
            "use_extensions": True,
            "thread_pool_parallelism_degree": config.get_thread_pool_parallelism_degree(
                str(constants.DEFAULT_THREAD_POOL_PARALLELISM_DEGREE)
            )
        }
        self.opts = Namespace()
        self.opts.__dict__ = opts
        logger._log = mock.MagicMock()
        self.event_loop_mock = EventLoopMock()

    @mock.patch("bxcommon.utils.logger.fatal")
    @mock.patch("bxcommon.utils.cli.get_argument_parser")
    @mock.patch("bxcommon.utils.cli.parse_arguments")
    @mock.patch("bxcommon.services.sdn_http_service.fetch_blockchain_networks")
    @mock.patch("bxcommon.network.network_event_loop_factory.create_event_loop")
    @mock.patch("bxcommon.services.sdn_http_service.register_node")
    @mock.patch("bxcommon.utils.config.log_pid")
    @mock.patch("bxcommon.utils.config.init_logging")
    def test_run_node(
            self,
            init_logging_mock,
            log_pid_mock,
            register_node_mock,
            create_event_loop_mock,
            fetch_blockchain_networks_mock,
            get_argument_parser_mock,
            parse_arguments_mock,
            fatal_mock
    ):
        init_logging_mock.return_value = None
        log_pid_mock.return_value = None
        create_event_loop_mock.return_value = self.event_loop_mock
        register_node_mock.return_value = NodeModel()
        fetch_blockchain_networks_mock.return_value = [self.blockchain_network]
        get_argument_parser_mock.return_value = argparse.ArgumentParser()
        parse_arguments_mock.return_value = self.opts
        fatal_mock.return_value = None
        node_runner.run_node("",  self.opts, NodeMock)
        self.assertEqual(self.event_loop_mock.run_count, 1)
