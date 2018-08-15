import unittest
from bxcommon.utils.object_hash import ObjectHash
from bxcommon.constants import SHA256_HASH_LEN


class ObjectHashTests(unittest.TestCase):

    def setUp(self):
        self.int_hash_31a = ObjectHash(bytearray([i for i in range(SHA256_HASH_LEN)]))
        self.int_hash_31b = ObjectHash(memoryview(bytearray([i for i in range(SHA256_HASH_LEN)])))
        self.int_hash_32 = ObjectHash(bytearray([i for i in range(1, SHA256_HASH_LEN + 1)]))
        self.int_hash_all_0 = ObjectHash(bytearray([0] * SHA256_HASH_LEN))

    def test_init(self):
        with self.assertRaises(AssertionError):
            ObjectHash(bytearray([i for i in range(SHA256_HASH_LEN - 1)]))
        with self.assertRaises(AssertionError):
            ObjectHash(bytearray())

        expected = self.int_hash_31a.binary
        actual = bytearray([i for i in range(SHA256_HASH_LEN)])
        self.assertEqual(expected, actual)
        actual = ObjectHash(memoryview(actual))
        self.assertEqual(actual.binary, expected)
        self.assertIsNotNone(hash(self.int_hash_all_0))

    def test_hash(self):
        self.assertEqual(hash(self.int_hash_31a), hash(self.int_hash_31b))
        self.assertNotEqual(hash(self.int_hash_31a), hash(self.int_hash_32))
        to_31 = bytearray([i for i in range(SHA256_HASH_LEN)])
        mutable_to_31 = ObjectHash(to_31)
        initial_hash = hash(mutable_to_31)
        to_31[6] = 12
        mutated_hash = hash(mutable_to_31)
        self.assertEqual(initial_hash, mutated_hash)

    def test_cmp(self):
        self.assertTrue(self.int_hash_31a == self.int_hash_31b)
        self.assertTrue(self.int_hash_32 > self.int_hash_31a)
        self.assertTrue(self.int_hash_all_0 < self.int_hash_31b)

    def test_get_item(self):
        self.assertEqual(self.int_hash_31a[5], 5)
        self.assertEqual(self.int_hash_31b[25], 25)
        self.assertEqual(self.int_hash_32[10], 11)
        self.assertEqual(self.int_hash_all_0[20], 0)

        int_list = [0] * SHA256_HASH_LEN
        expected = 3
        expected_index = 1
        int_list[expected_index] = expected
        int_hash = ObjectHash(bytearray(int_list))
        self.assertEqual(int_hash[expected_index], expected)

    def test_repr(self):
        self.assertEqual(repr(self.int_hash_31a), repr(self.int_hash_31b))
        self.assertNotEqual(repr(self.int_hash_31a), repr(self.int_hash_32))
        self.assertNotEqual(repr(self.int_hash_31b), repr(self.int_hash_all_0))

        expected = bytearray([i for i in range(SHA256_HASH_LEN )])
        actual = ObjectHash(bytearray(expected))
        self.assertEqual(repr(actual), repr(expected))







