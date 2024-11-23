# BatchProcessor

**BatchProcessor** is a lightweight Python library designed to efficiently group records into batches while adhering to customizable size and count constraints. It's ideal for applications where records need to be processed in manageable chunks, such as file uploads, data ingestion pipelines, or batch processing systems.

## Features

- **Flexible Configuration**: Easily set limits for:
  - Maximum record size (in bytes).
  - Maximum batch size (in bytes).
  - Maximum number of records per batch.
- **Automatic Batching**: Dynamically creates batches based on the provided constraints.
- **Resilient Processing**: Skips records that exceed the maximum record size to ensure uninterrupted processing.
- **Simple Interface**: Straightforward API for easy integration with existing workflows.

## Installation

Clone the repository and include the `BatchProcessor` module in your project. Alternatively, you can package the library or publish it on PyPI for distribution.

## Usage

### Basic Example
```python
from batch_processor import BatchProcessor

# Initialize with default constraints
processor = BatchProcessor()

# Sample records
records = [
    "record_1", 
    "record_2", 
    ...
]

# Process into batches
batches = processor.run_process(records)

# Output: List of batches adhering to constraints
print(batches)
```

## Unit tests

- **Diverse test cases**: Test cases are included and can be run with `python -m unittest test_batch_processor.py`
