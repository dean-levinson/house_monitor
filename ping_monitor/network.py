from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1
from scapy.route import conf as scapy_conf

class Ping(object):
    """
    Sends ping to given address
    """
    ECHO_REPLY = 0

    def __init__(self, ip_address):
        self.dst_ip = ip_address

    def activate(self):
        interface, src_ip, _ = scapy_conf.route.route(self.dst_ip)

        return self.send_ping(self.dst_ip, src_ip, interface)


    def send_ping(self, dst_ip, src_ip, interface):
        ping_request = IP(src=src_ip, dst=dst_ip) / ICMP(type="echo-request")
        ping_reply = sr1(ping_request, iface=interface, timeout=5, verbose=0)

        return ping_reply["ICMP"].type == self.ECHO_REPLY


if __name__ == "__main__":

    p = Ping("10.0.0.138")
    
    p.activate()