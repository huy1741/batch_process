from typing import List

# Requirement constants
MAX_RECORD_SIZE = 1 * 1024 * 1024  # 1 MB in bytes
MAX_BATCH_SIZE = 5 * 1024 * 1024  # 5 MB in bytes
MAX_RECORDS_PER_BATCH = 500

class BatchProcessor:
    """
    A library for batch processing that divides records into batches based on size and count limits.
    """

    def __init__(self, max_record_size=MAX_RECORD_SIZE, max_batch_size=MAX_BATCH_SIZE, max_records_per_batch=MAX_RECORDS_PER_BATCH):
        """
        Initializes a BatchProcessor instance with the provided size and count limits.

        Args:
            max_record_size (int): The maximum allowed size (in bytes) for a single record. Defaults to 1 MB.
            max_batch_size (int): The maximum allowed size (in bytes) for a single batch. Defaults to 5 MB.
            max_records_per_batch (int): The maximum number of records allowed in a single batch. Defaults to 500.
        """
        self.max_record_size = max_record_size
        self.max_batch_size = max_batch_size
        self.max_records_per_batch = max_records_per_batch

    def run_process(self, records: List[str]) -> List[List[str]]:
        """
        Processes a list of records into batches based on the configured limits.

        Args:
            records (List[str]): A list of record inputs as strings.

        Returns:
            List[List[str]]: A list of batches, where each batch is a list of records.
                             Each batch adheres to the size and count constraints.
        
        Notes:
            - Records exceeding the maximum record size (`max_record_size`) are skipped.
            - A new batch is created if adding a record would exceed `max_batch_size` or `max_records_per_batch`.
        """
        final_batch = []
        current_batch = []
        current_batch_size = 0

        for record in records:
            record_size = len(record.encode('utf-8'))

            if record_size > self.max_record_size:
                continue

            if (current_batch_size + record_size > self.max_batch_size or
                len(current_batch) + 1 > self.max_records_per_batch):
                final_batch.append(current_batch)
                current_batch = []
                current_batch_size = 0

            current_batch.append(record)
            current_batch_size += record_size

        if current_batch:
            final_batch.append(current_batch)

        return final_batch
