import json 
import ipaddress
import scapy.all as scapy

from .network import Ping


class Monitor(object):
    '''
    Represents the all montior.

    :param network_subnet: the subnet of the network. in the shape of "10.0.0.0/24"
    :type network_subnet: str
    '''
    def __init__(self, network_subnet):
        self.network_subnet = ipaddress.ip_network(network_subnet)

    def scan_network(self):
        for host in self.network_subnet.hosts():
            self.send_ping(str(host))
    
    def send_ping(self, ip_address):        
        ping_obj = Ping(ip_address)
        if ping_obj.activate():
            print("Got answer from {}".format(ip_address))

    def serialize(self):
        pass


class Computer(object):
    """
    Represents computer instance obj.
    """
    def __init__(self, ip, mac, ttl):
        self.ip = ip
        self.ttl = ttl

    def serialize(self):
        return json.dumps({
            "ip": self.ip,
            "ttl": self.ttl
        })

if __name__ == "__main__":
    monitor = Monitor("10.0.0.0/24")
    monitor.scan_network()