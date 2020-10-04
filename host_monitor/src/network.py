from typing import Optional

from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1
from scapy.route import conf as scapy_conf

PING_TIMEOUT = 5

class PingData(object):
    """
    docstring
    """
    TARGET_LAYERS = ["ICMP", "IP"]
    TRANSLATOR = {"ip": "src"}

    def __init__(self, ping_reply_packet) -> None:
        self.ping_reply_packet = ping_reply_packet

    def __getattr__(self, item):
        if item in self.TRANSLATOR:
            item = self.TRANSLATOR[item]

        for layer in self.TARGET_LAYERS:
            if hasattr(self.ping_reply_packet[layer], item):
                return getattr(self.ping_reply_packet[layer], item)
        
        raise AttributeError(item)

class Ping(object):
    """
    Sends ping to given address
    """
    ECHO_REPLY = 0

    def __init__(self, ip_address) -> None:
        self.dst_ip = ip_address

    def activate(self) -> Optional[PingData]:
        interface, src_ip, _ = scapy_conf.route.route(self.dst_ip)

        return self.send_ping(self.dst_ip, src_ip, interface)

    def send_ping(self, dst_ip, src_ip, interface) -> Optional[PingData]:
        ping_request = IP(src=src_ip, dst=dst_ip) / ICMP(type="echo-request")
        ping_reply = sr1(ping_request, iface=interface, timeout=PING_TIMEOUT, verbose=0)

        if not ping_reply:
            return None

        if ping_reply["ICMP"].type == self.ECHO_REPLY:
            return PingData(ping_reply)

if __name__ == "__main__":

    p = Ping("10.0.0.138")
    
    p.activate()