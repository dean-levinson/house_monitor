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
        self.existing_hosts = {}

    def scan_network(self):
        for host in self.network_subnet.hosts():
            self.send_ping(str(host))
    
    def send_ping(self, ip_address):        
        ping_obj = Ping(ip_address)
        print("Send ping to {}".format(ip_address))
        ping_data = ping_obj.activate()
        if ping_data:
            print("Got answer from {}".format(ip_address))
            self.existing_hosts[ip_address] = Computer(packet_data=ping_data)
            print(self.existing_hosts[ip_address])

    def serialize(self):
        pass


class Computer(object):
    """
    Represents computer instance obj.
    """
    PACKET_DATA_ATTRS = "ip ttl".split()

    def __init__(self, *args, **kwargs):
        self.attrs = {}

        if "packet_data" in kwargs:
            self.packet_data = kwargs["packet_data"]

            for attr in self.PACKET_DATA_ATTRS:
                if hasattr(self.packet_data, attr):
                    self.attrs[attr] = getattr(self.packet_data, attr)

    def serialize(self):
        return json.dumps(self.attrs)

    def __str__(self):
        string = "Computer {}:\n{{\n".format(self.attrs.get("ip", "Unknown"))
        for attr in self.attrs:
            string += " {}: {}\n".format(attr, self.attrs[attr])
        string += "}\n"
        return string
        

if __name__ == "__main__":
    monitor = Monitor("10.0.0.0/24")
    monitor.scan_network()