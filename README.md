# Data Doser
This script creates a sequence of test files and delivers or doses them into an S3 bucket at random times over a period of time.

## Usage
To make the data doser:

```python doser.py --chunks 5 --duration 100 --numfiles=20```

## Prerequisites
A working s3 bucket configured that you can write to.

