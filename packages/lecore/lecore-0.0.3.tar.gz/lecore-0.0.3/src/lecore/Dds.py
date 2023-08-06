import numbers
import socket


class Dds:
    """Class for sending data to DDS server and receiving command"""

    def __init__(self, host, port):
        """Get host and port of DDS. Open socket and bind the port
        :param host: Hostname or IP address of dds server, e.g. devel.lecloud.cz
        :param port: Port of dds server, e.g. 20000 from LE, 50106 from outside"""
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.header = None
        self.body = None
        self.command = None
        self.callback = None
        self.decimals = 3
        self.channel = None

    def set_device(self, dev_id, channel, callback=None):
        """Set device parameters for dds reports
        :param dev_id: Device ID either as integer number or string already
        :param channel: Logical communication, zero means no channel indication
        :param callback: Command reception callback. Got command, returns response."""
        # Create header using number or string device ID
        if isinstance(dev_id, numbers.Number):
            self.header = f"{dev_id:x}"
        else:
            self.header = f"{dev_id}"
        if channel != 0:
            self.channel = f"-{channel}:"
        else:
            self.channel = f":"
        self.callback = callback

    def set_coll(self, coll):
        """Pass data collection to send as dictionary
        :param coll: Dictionary of data to send"""
        self.body = "{"
        sep = ""
        # Print all members of dictionary
        for key in coll:
            val = coll[key]
            #
            if isinstance(val, float):
                val = round(val, self.decimals)
            self.body += f"{sep}{str(key)}: {val}"
            sep = ", "
        self.body += "}"

    def send_log(self, log):
        """Send log string message to log file
        :param log: Log message
        :returns True on success
        :returns False on failure"""
        if self.header is None:
            return False
        # Send UDP data to dds
        self.sock.sendto(bytes(self.header + ":" + log, "utf-8"), (self.host, self.port))
        return True

    def send_receive(self, resp_timeout):
        """Send the report and receive command from DDS.
        If command is received, we pass it to app-specific callback that returns response for server
        :param resp_timeout: Timeout of dds server to respond
        :returns True on successful transmission and reception if required
        :returns False on response timeout"""
        # Check that we have data to send
        if self.header is None or self.body is None:
            return False
        # Send UDP data to dds
        self.sock.sendto(bytes(self.header + self.channel + self.body, "utf-8"), (self.host, self.port))
        # Non-zero response timeout means we want to receive command
        if resp_timeout != 0:
            # Set timeout
            self.sock.settimeout(resp_timeout)
            try:
                # Try receive data
                (resp, address) = self.sock.recvfrom(1024)
                # We got response, encode it and split
                command = str(resp, 'utf-8')
                parts = command.split(':')
                # Check it is for us
                if parts[0] in self.header:
                    # Get request ID and pass command to callback function
                    resp_id = int(parts[1]) + (1 << 15)
                    self.command = parts[2]
                    if self.callback is not None:
                        resp_str = self.callback(self.command)
                    else:
                        resp_str = "Accepted"
                    # Prepare response and send it back
                    self.body = f"{resp_id}:{resp_str}"
                    self.sock.sendto(bytes(parts[0] + ":" + parts[1] + self.body, "utf-8"), address)
            # Timeout exception
            except socket.timeout:
                return False
        return True


