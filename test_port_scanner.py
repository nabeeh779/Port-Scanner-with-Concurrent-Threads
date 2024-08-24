import pytest
from unittest.mock import Mock, patch
from main import scan_port, scan_ports_concurrently, pool_scan_ports_concurrently
import socket


def test_scan_port(mocker):
    # Test for an open port
    mock_socket = mocker.patch(
        "socket.socket"
    )  # Mocker.patch change socket.socket object with a mock
    mock_socket.return_value.__enter__.return_value.connect_ex.return_value = (
        0  # Connect_ex method of the mock
    )
    # socket is set to return 0, which indicates that the port is open.

    with patch("builtins.print") as mock_print:
        scan_port("127.0.0.1", 80)
        mock_print.assert_any_call("Port 80 is open on 127.0.0.1")

    # Test for a closed port
    mock_socket.return_value.__enter__.return_value.connect_ex.return_value = (
        1  # connect_ex method to return 1,
    )
    # indicating that the port is closed.

    with patch("builtins.print") as mock_print:
        scan_port("127.0.0.1", 81)
        mock_print.assert_any_call("Checking Port:81 on 127.0.0.1\n")
        assert not any(
            "Port 81 is open on 127.0.0.1" in call[0][0]
            for call in mock_print.call_args_list
        )

    # Test for an exception , connect_ex method raise an exception.
    mock_socket.return_value.__enter__.return_value.connect_ex.side_effect = Exception(
        "Test exception"
    )

    with patch("logging.error") as mock_log:
        scan_port("127.0.0.1", 82)
        mock_log.assert_called_with(
            "Error scanning port 82 on 127.0.0.1: Test exception"
        )


# Run multiple times, once for each function
@pytest.mark.parametrize(
    "func", [scan_ports_concurrently, pool_scan_ports_concurrently]
)
def test_concurrent_port_scans(func, mocker):
    mock_scan_port = mocker.patch("main.scan_port")

    # Simulate some open and closed ports
    def side_effect(ip, port):
        if port in [80, 443]:
            return 0  # Open port
        return 1  # Closed port

    mock_scan_port.side_effect = side_effect  # Sets the side_effect of the mocked
    # scan_port.

    func("127.0.0.1", 79, 444, 4)  # Scan ports 79-444 with 4 threads

    # Check that all ports were scanned
    assert mock_scan_port.call_count == 444 - 79 + 1

    # Check that open ports were correctly identified
    open_ports = [
        call[0][1] for call in mock_scan_port.call_args_list if call[0][1] in [80, 443]
    ]
    assert set(open_ports) == {80, 443}


def test_concurrent_port_scans_exception_handling(mocker):
    mock_scan_port = mocker.patch("main.scan_port")
    mock_scan_port.side_effect = Exception("Test exception")

    with patch("logging.error") as mock_log:
        pool_scan_ports_concurrently("127.0.0.1", 1, 100, 4)
        assert mock_log.call_count == 100  # All ports should log an error
