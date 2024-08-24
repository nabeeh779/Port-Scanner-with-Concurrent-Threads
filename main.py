import socket
import sys
import threading
import argparse  # Python module used for parsing command-line arguments
import logging
from concurrent.futures import ThreadPoolExecutor
import itertools
from error_handling import *

# Setting up logging
logging.basicConfig(
    filename="port_scanner.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
# Global lock for thread-safe printing or logging
lock = threading.Lock()


def scan_ports(ip, ports):
    """
    Function to scan a list of ports.
    Used by each thread.
    """
    total_ports = len(ports)  # Getting ports len
    for index, port in enumerate(
        ports
    ):  # enumerate function - loop over ports and have an automatic counter.
        scan_port(ip, port)  # Run scan port function
        with (
            lock
        ):  # Ensures that the code block is executed by only one thread at a time
            progress = (
                (index + 1) / total_ports * 100
            )  # Percentage of ports scanned based on the current index
            print(f"Progress: {progress:.2f}%\n")  # Print for the user


def scan_port(ip, port):
    """
    This Function do the port scan.
    Input: Destination IP , destination port.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Timeout each connection attempt.
            # Attempt to connect to the port , (connect_ex) provides an error code instead of raising exceptions.
            result = sock.connect_ex((ip, port))
            print(f"Checking Port:{port} on {ip}\n")
            with lock:
                if result == 0:  # Port is open
                    print(f"Port {port} is open on {ip}")
                    logging.info(f"Port {port} is open on {ip}")
                else:
                    logging.info(f"Port {port} is closed on {ip}")
    except Exception as e:
        with lock:
            logging.error(f"Error scanning port {port} on {ip}: {e}")


def scan_ports_concurrently(ip, start_port, end_port, num_threads):
    """
    This function divides the port scanning task among multiple threads
    """
    port_range = range(
        start_port, end_port + 1
    )  # Port range from start port to end_port+1
    thread_list = []  # Thread list to store threads
    for i in range(num_threads):
        ports_to_scan = port_range[i::num_threads]  # Divide port range
        thread = threading.Thread(
            target=scan_ports, args=(ip, ports_to_scan)
        )  # Create thread
        thread_list.append(thread)  # Adding thread to thread list
        thread.start()  # Start thread

    # Wait for all threads to complete
    for thread in thread_list:
        thread.join()


def chunked(iterable, size):
    """
    Yield successive n-sized chunks from iterable.
    """
    iterator = iter(
        iterable
    )  # Convert the input iterable into an iterator to enable sequential access
    for first in iterator:
        yield list(itertools.chain([first], itertools.islice(iterator, size - 1)))


def pool_scan_ports_concurrently(ip, start_port, end_port, num_threads):
    """
    This function divides the port scanning task among multiple threads, it differs from the previous one
    because it uses Thread Pool to manage threads more efficiently and avoid creating too many threads.
    """
    port_range = range(start_port, end_port + 1)
    with ThreadPoolExecutor(
        max_workers=num_threads
    ) as executor:  # Creates a pool of threads
        # Divide the port range into chunks and submit tasks to the executor
        futures = [
            executor.submit(scan_ports, ip, ports)
            for ports in chunked(port_range, num_threads)
        ]
        # Wait for all tasks to complete
        for future in futures:
            future.result()  # Handle exceptions if any


def main():
    # Parse commandLine arguments
    parser = argparse.ArgumentParser(description="Port Scanner with Concurrent Threads")
    parser.add_argument("ip", help="Target IP address to scan")
    parser.add_argument(
        "--start-port", type=int, default=1, help="Starting port number (default: 1)"
    )
    parser.add_argument(
        "--end-port", type=int, default=1024, help="Ending port number (default: 1024)"
    )
    parser.add_argument(
        "--threads", type=int, default=10, help="Number of threads to use (default: 10)"
    )
    args = parser.parse_args()

    if not check_ip(args.ip):
        print(f"Error: Invalid IP address '{args.ip}'.")
        sys.exit(1)
    if not check_ports(args.start_port, args.end_port):
        print(
            f"Error: Invalid port range {args.start_port} - {args.end_port}. Ports must be between 1 and 65535 and "
            f"start port must be less than or equal to end port. "
        )
        sys.exit(1)
    if not is_valid_thread_count(args.threads):
        print(
            f"Error: Invalid number of threads {args.threads}. Number of threads must be between 1 and 1000."
        )
        sys.exit(1)

    # scan_ports_concurrently(args.ip, args.start_port, args.end_port, args.threads)
    pool_scan_ports_concurrently(args.ip, args.start_port, args.end_port, args.threads)


if __name__ == "__main__":
    main()
