# Port Scanner

## Overview

This Python port scanner allows you to scan a range of ports on a specified IP address concurrently. It utilizes threading and thread pooling to perform the scans efficiently. The results are logged and printed to the console.

## Features

- Scan a range of ports on a target IP address.
- Supports concurrent scanning using threading and thread pools.
- Logs results to a file (`port_scanner.log`).
- Provides progress updates during scanning.

## Requirements

- Python 3.6 or later
- `pytest` for testing

# Code Structure

## `main.py`

- **`scan_ports(ip, ports)`**: Scans a list of ports.
- **`scan_ports_help(ip, ports)`**: Helper function for scanning ports.
- **`scan_port(ip, port)`**: Scans a single port and logs results.
- **`scan_ports_concurrently(ip, start_port, end_port, num_threads)`**: Scans ports concurrently using threads.
- **`chunked(iterable, size)`**: Helper function to yield chunks of a specified size from an iterable.
- **`pool_scan_ports_concurrently(ip, start_port, end_port, num_threads)`**: Scans ports concurrently using a thread pool.
- **`main()`**: Entry point for command-line arguments parsing and scanning execution.

## Testing

The code has been tested using `pytest`.
## `test_main.py`

Contains tests for the port scanning functions using `pytest`.

- **`test_scan_port(mocker)`**: Tests for the `scan_port` function, including scenarios for open ports, closed ports, and exceptions.
- **`test_concurrent_port_scans(func, mocker)`**: Tests concurrent scanning functions (`scan_ports_concurrently` and `pool_scan_ports_concurrently`) to ensure all ports are scanned and open ports are identified correctly.
- **`test_concurrent_port_scans_exception_handling(mocker)`**: Tests handling of exceptions during concurrent scanning.
