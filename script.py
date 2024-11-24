from batch_processor import BatchProcessor, MAX_RECORD_SIZE

def run_example(description: str, records: list):
    """
    Helper function to process records with BatchProcessor and print results.


    Args:
            description (str): Description of the test case.
            records (list): List of input records.
    """
    processor = BatchProcessor()
    print(f"Test: {description}")
    print(f"Number of input records: {len(records)}")
    batches = processor.run_process(records)
    print(f"Number of output batches: {len(batches)}")
    for i, batch in enumerate(batches, 1):
        print(f"  Batch {i}: {len(batch)} records, {sum(len(r.encode('utf-8')) for r in batch)} bytes")
    print("-" * 50)

if __name__ == "__main__":
    # Example 1: Empty input
    run_example("Empty input", [])

    # Example 2: Single small record
    run_example("Single small record", ["small_record"])

    # Example 3: Record exceeding max size
    run_example(
        "Record exceeding max size", 
        ["x" * (MAX_RECORD_SIZE + 1)]
    )

    # Example 4: Multiple small records fitting into one batch
    run_example(
        "Multiple small records (one batch)", 
        ["small"] * 10
    )

    # Example 5: Large batch with multiple records (exceeding max size)
    run_example(
        "Large batch with multiple records",
        ["x" * (MAX_RECORD_SIZE // 2)] * 12
    )

    # Example 6: Exceeding maximum number of records per batch
    run_example(
        "Exceeding maximum number of records per batch",
        ["x"] * 600
    )

    # Example 7: Mixed sizes, skipping invalid records
    run_example(
        "Mixed sizes, skipping invalid records",
        [
            "x" * (MAX_RECORD_SIZE - 10),
            "x" * (MAX_RECORD_SIZE + 1),  # Invalid, skipped
            "y" * (MAX_RECORD_SIZE - 20),
            "z" * 100
        ]
    )

    # Example 8: Large input set exceeding batch size and count
    run_example(
        "Large input set exceeding batch size and count",
        ["x" * 100] * 6000  # Each record is 100 bytes
    )

    # Example 9: Unicode characters and varying sizes
    run_example(
        "Unicode characters and varying sizes",
        [
            "hello",                     # 5 bytes
            "你好",                       # 6 bytes
            "🙂",                        # 4 bytes
            "🌍🌎🌏" * 100_000,            # Exceeds MAX_RECORD_SIZE, skipped
            "short"                      # 5 bytes
        ]
    )
