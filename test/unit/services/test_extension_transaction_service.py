from bxcommon.services.extension_transaction_service import ExtensionTransactionService
from bxcommon.services.transaction_service import TransactionService
from bxcommon.test_utils import helpers
from bxcommon.test_utils.abstract_transaction_service_test_case import AbstractTransactionServiceTestCase
from bxcommon.utils import crypto, convert
from bxcommon.utils.object_hash import Sha256Hash


class ExtensionTransactionServiceTest(AbstractTransactionServiceTestCase):

    def setUp(self):
        helpers.set_extensions_parallelism()
        super(ExtensionTransactionServiceTest, self).setUp()

    def test_get_missing_transactions(self):
        self._test_get_missing_transactions()

    def test_sid_assignment_basic(self):
        self._test_sid_assignment_basic()

    def test_sid_assignment_multiple_sids(self):
        self._test_sid_assignment_multiple_sids()

    def test_sid_expiration(self):
        self._test_sid_expiration()

    def test_sid_expiration_multiple_sids(self):
        self._test_sid_expiration_multiple_sids()

    def test_track_short_ids_seen_in_block(self):
        self._test_track_short_ids_seen_in_block()

    def test_track_short_ids_seen_in_block_multiple_per_tx(self):
        self._test_track_short_ids_seen_in_block_multiple_per_tx()

    def test_transactions_contents_memory_limit(self):
        self._test_transactions_contents_memory_limit()

    def test_expire_old_assignments(self):
        self._test_expire_old_assignments()

    def test_memory_stats(self):
        self._test_memory_stats()

    def test_iter_timestamped_transaction_hashes_from_oldest(self):
        self._test_iter_transaction_hashes_from_oldest()

    def test_removed_transactions_history_by_hash(self):
        self._test_removed_transactions_history_by_hash()

    def test_removed_transactions_history_by_sid(self):
        self._test_removed_transactions_history_by_sid()

    def test_removed_transactions_length_limit(self):
        self._test_removed_transactions_length_limit()

    def test_add_tx_without_sid(self):
        self._test_add_tx_without_sid()

    def add_tx_without_sid_expire(self):
        self._test_add_tx_without_sid_expire()

    def test_add_sid_without_content(self):
        self._test_add_sid_without_content()

    def test_assign_short_id(self):
        transaction_hash = Sha256Hash(helpers.generate_bytearray(crypto.SHA256_HASH_LEN))
        short_id1 = 100

        self.assertFalse(self.transaction_service.has_short_id(short_id1))
        self.assertFalse(self.transaction_service.has_transaction_contents(transaction_hash))

        self.transaction_service.assign_short_id(transaction_hash, short_id1)

        self.assertTrue(self.transaction_service.has_short_id(short_id1))
        self.assertFalse(self.transaction_service.has_transaction_contents(transaction_hash))

        short_id2 = 200
        self.transaction_service.assign_short_id(transaction_hash, short_id2)
        self.assertTrue(self.transaction_service.has_short_id(short_id2))

        short_ids = self.transaction_service.get_short_ids(transaction_hash)
        self.assertEqual(2, len(short_ids))
        self.assertTrue(short_id1 in short_ids)
        self.assertTrue(short_id2 in short_ids)

    def test_set_contents(self):
        transaction_hash = Sha256Hash(helpers.generate_bytearray(crypto.SHA256_HASH_LEN))
        tx_contents = memoryview(helpers.generate_bytearray(500))

        self.assertFalse(self.transaction_service.has_transaction_contents(transaction_hash))

        self.transaction_service.set_transaction_contents(transaction_hash, tx_contents)

        self.assertTrue(self.transaction_service.has_transaction_contents(transaction_hash))

        saved_contents = self.transaction_service.get_transaction_by_hash(transaction_hash)
        self.assertEqual(convert.bytes_to_hex(tx_contents), convert.bytes_to_hex(saved_contents.tobytes()))
        self.assertEqual(len(tx_contents), self.transaction_service._total_tx_contents_size)

        new_content = memoryview(helpers.generate_bytearray(750))
        self.transaction_service.set_transaction_contents(transaction_hash, new_content)
        saved_contents = self.transaction_service.get_transaction_by_hash(transaction_hash)
        self.assertEqual(convert.bytes_to_hex(tx_contents), convert.bytes_to_hex(saved_contents.tobytes()))
        self.assertEqual(len(new_content), self.transaction_service._total_tx_contents_size)

    def test_process_gateway_transaction_from_bdn(self):
        self._test_process_gateway_transaction_from_bdn()

    def test_get_transactions(self):
        self._test_get_transactions()

    def _get_transaction_service(self) -> TransactionService:
        return ExtensionTransactionService(self.mock_node, 0)
