import json 
import itertools
from typing import Generator, Dict, Iterator, Optional

import ipaddress

from src.network import Ping

class HostNotFound(Exception):
    pass

class Computer(object):
    """
    Represents computer instance obj.
    """
    PACKET_DATA_ATTRS = "ip ttl".split()
    
    def __init__(self, *args, **kwargs) -> None:
        self.attrs = {}

        if "packet_data" in kwargs:
            self.packet_data = kwargs["packet_data"]

            for attr in self.PACKET_DATA_ATTRS:
                if hasattr(self.packet_data, attr):
                    self.attrs[attr] = getattr(self.packet_data, attr)

    def serialize(self) -> str:
        return json.dumps(self.attrs)

    def __str__(self) -> str:
        string = "Computer {}:\n{{\n".format(self.attrs.get("ip", "Unknown"))
        for attr in self.attrs:
            string += " {}: {}\n".format(attr, self.attrs[attr])
        string += "}\n"
        return string
        

class Monitor(object):
    '''
    Represents the montior.

    :param network_subnet: the subnet of the network. in the shape of "10.0.0.0/24"
    :type network_subnet: str
    '''
    def __init__(self, network_subnet) -> None:
        self.network_subnet = ipaddress.ip_network(network_subnet)
        self.existing_hosts = {}

    def scan_network(self) -> Generator[Computer, None, None]:
        for host in self.get_hosts():
            yield self.scan_host(host)

    def scan_host(self, host: str) -> Computer:
        result = self.send_ping(host)
        self.existing_hosts[host] = result
        return result

    def get_hosts(self, max_hosts: int=0) -> Iterator[str]:
        gen = (str(host) for host in self.network_subnet.hosts())
        if max_hosts:
            return itertools.islice(gen, max_hosts)
        return gen

    def send_ping(self, ip_address: str) -> Computer:
        ping_obj = Ping(ip_address)
        print("Send ping to {}".format(ip_address))
        ping_data = ping_obj.activate()
        computer_obj = None
        if not ping_data:
            raise HostNotFound(f"host {ip_address} not found")

        print("Got answer from {}".format(ip_address))
        computer_obj = Computer(packet_data=ping_data)
        self.existing_hosts[ip_address] = computer_obj
        return computer_obj

    def serialize(self) -> Dict[Computer, str]:
        return NotImplemented

if __name__ == "__main__":
    monitor = Monitor("10.0.0.0/24")
    monitor.scan_network()
