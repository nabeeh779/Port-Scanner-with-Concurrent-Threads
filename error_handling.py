import ipaddress


def check_ip(ip):
    try:
        # This will check both IPv4 and IPv6 addresses
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def check_ports(start, end):
    # Check ports range
    max_Port = 65535
    min_Port = 1
    if start < min_Port or end > max_Port or start > end:
        return False
    return True


def is_valid_thread_count(num_threads):
    # Check threads number is vaild
    min_threads = 1
    max_threads = 1000
    if isinstance(num_threads, int) and min_threads <= num_threads <= max_threads:
        return True
    return False

