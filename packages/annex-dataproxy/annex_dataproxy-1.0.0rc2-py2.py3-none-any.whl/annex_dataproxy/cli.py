from annexremote import Master
from .remote import DataProxyRemote

def main():
    master = Master()
    remote = DataProxyRemote(master)
    master.LinkRemote(remote)
    master.Listen()
