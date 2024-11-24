import unittest
from batch_processor import BatchProcessor, MAX_RECORD_SIZE, MAX_BATCH_SIZE, MAX_RECORDS_PER_BATCH

class TestBatchProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = BatchProcessor()

    def test_empty_input(self):
        """Test handling of empty input."""
        self.assertEqual(self.processor.run_process([]), [])

    def test_single_small_record(self):
        """Test a single record that is well within size limits."""
        records = ["small_record"]
        self.assertEqual(self.processor.run_process(records), [records])

    def test_record_exceeding_max_size(self):
        """Test skipping a record that exceeds the maximum allowed size."""
        large_record = "x" * (MAX_RECORD_SIZE + 1)
        self.assertEqual(self.processor.run_process([large_record]), [])

    def test_batch_exceeding_max_size(self):
        """Test splitting into multiple batches when batch size exceeds the limit."""
        small_record = "x" * (MAX_RECORD_SIZE // 2)
        records = [small_record] * 12  # Total size exceeds 5 MB
        batches = self.processor.run_process(records)
        self.assertEqual(len(batches), 2)  # Two batches should be created
        for batch in batches:
            self.assertLessEqual(sum(len(r.encode('utf-8')) for r in batch), MAX_BATCH_SIZE)

    def test_batch_exceeding_max_count(self):
        """Test splitting into multiple batches when record count exceeds the limit."""
        small_record = "x"
        records = [small_record] * 600  # Exceeds max count of 500
        batches = self.processor.run_process(records)
        self.assertEqual(len(batches), 2)  # Should create two batches
        self.assertEqual(len(batches[0]), MAX_RECORDS_PER_BATCH)  # First batch max count
        self.assertEqual(len(batches[1]), 600 - MAX_RECORDS_PER_BATCH)  # Remaining records

    def test_mixed_sizes(self):
        """Test processing records of varying sizes and skipping invalid ones."""
        records = [
            "x" * (MAX_RECORD_SIZE - 1),  # Valid
            "x" * (MAX_RECORD_SIZE + 1),  # Invalid
            "y" * (MAX_RECORD_SIZE - 2),  # Valid
        ]
        batches = self.processor.run_process(records)
        self.assertEqual(len(batches), 1)  # Only one batch
        self.assertEqual(len(batches[0]), 2)  # Two valid records

    def test_large_input_set(self):
        """Test handling a very large number of records."""
        small_record = "x" * 100  # Each record is 100 bytes
        records = [small_record] * 10_000  # Total input exceeds batch limits
        batches = self.processor.run_process(records)
        self.assertGreater(len(batches), 0)
        for batch in batches:
            self.assertLessEqual(len(batch), MAX_RECORDS_PER_BATCH)  # Batch size limit
            self.assertLessEqual(
                sum(len(r.encode('utf-8')) for r in batch), MAX_BATCH_SIZE
            )  # Batch byte size limit

    def test_unicode_characters(self):
        """Test handling of Unicode characters and varying byte sizes."""
        records = [
            "hello",  # 5 bytes
            "你好",  # 6 bytes
            "🙂",  # 4 bytes
            "🌍🌎🌏" * 100_000,  # Exceeds MAX_RECORD_SIZE, invalid
            "short",  # 5 bytes
        ]
        batches = self.processor.run_process(records)
        self.assertEqual(len(batches), 1)  # Only one valid batch
        self.assertEqual(len(batches[0]), 4)  # Four valid records

    def test_boundary_conditions(self):
        """Test records exactly at size limits and at batch limits."""
        records = [
            "x" * MAX_RECORD_SIZE,  # Exactly MAX_RECORD_SIZE
            "y" * (MAX_RECORD_SIZE - 1),  # Slightly below limit
            "z" * MAX_RECORD_SIZE,  # Exactly MAX_RECORD_SIZE
            "w" * (MAX_RECORD_SIZE - 10),  # Slightly below limit
        ]
        batches = self.processor.run_process(records)
        self.assertEqual(len(batches), 1)  # Should fit in one batch
        self.assertEqual(len(batches[0]), 4)  # All records valid

    def test_multiple_edge_cases(self):
        """Test a mixture of valid and invalid records."""
        records = [
            "x" * (MAX_RECORD_SIZE + 10),  # Invalid
            "y" * (MAX_RECORD_SIZE // 2),  # Valid
            "z" * (MAX_RECORD_SIZE // 2),  # Valid
            "a" * (MAX_BATCH_SIZE + 1),  # Invalid batch-size record
            "b" * (MAX_RECORD_SIZE - 1),  # Valid
        ]
        batches = self.processor.run_process(records)
        self.assertEqual(len(batches), 1)  # Only one batch
        self.assertEqual(len(batches[0]), 3)  # Three valid records

if __name__ == "__main__":
    unittest.main()
