#Only works on Linux Systems
import subprocess
import scapy
import threading
from netfilterqueue import NetfilterQueue

class Packet_Manager():
    """
    Filters Packets based on it filtering lists. The lists are broken down as much as possible to limit the amount of time spent looking
    through lists on each packet and to limit the amount of data that needs to be refreshed when a packet updates.
    """
    def __init__(self, App):
        self.app = App
        #packets coming into the network from the internet
        self.inbound_interface = "eth1"
        #packets going to the internet from the network
        self.outbound_interface = "eth0"


        self.incoming_ip_whitelists = []
        self.incoming_mac_whitelists = []
        self.incoming_port_whitelists = []
        self.incoming_protocol_whitelists = []
        self.incoming_application_whitelists = []

        self.outgoing_ip_whitelists = []
        self.outgoing_mac_whitelists = []
        self.outgoing_port_whitelists = []
        self.outgoing_protocol_whitelists = []
        self.outgoing_application_whitelists = []

        self.incoming_ip_blacklists = []
        self.incoming_mac_blacklists = []
        self.incoming_port_blacklists = []
        self.incoming_protocol_blacklists = []
        self.incoming_application_blacklists = []

        self.outgoing_ip_blacklists = []
        self.outgoing_mac_blacklists = []
        self.outgoing_port_blacklists = []
        self.outgoing_protocol_blacklists = []
        self.outgoing_application_blacklists = []

        self.incoming_exceptions = []
        self.outgoing_exceptions = []

        self.filter_settings = {}

        self.load_filter()
        self.initiate_packet_capture()

    def initiate_packet_capture(self):
        try:
            #Enable packet forwarding
            subprocess.run(["sudo", "sysctl", "net.ipv4.ip_forward=1"], check=True)
            #Add iptables rule to forward packets to NFQUEUE
            subprocess.run(["sudo", "iptables", "-A", "FORWARD", "-i", self.outbound_interface, "-j", "NFQUEUE", "--queue-num", "0"], check=True)
            subprocess.run(["sudo", "iptables", "-A", "FORWARD", "-i", self.inbound_interface, "-j", "NFQUEUE", "--queue-num", "1"], check=True)
           
            #Bind NetfilterQueue
            self.outbound_thread = threading.Thread(target=self.bind_nfqueue, args=(0, "outgoing"))
            self.inbound_thread = threading.Thread(target=self.bind_nfqueue, args=(1, "incoming"))

        except KeyboardInterrupt:
            print("Firewall Interrupted")
        except subprocess.CalledProcessError as e:
            print("Error occurred:", e)
    
    def bind_nfqueue(self, queue_number, direction):
        nfqueue = NetfilterQueue()
        nfqueue.bind(queue_number, lambda packet: self.process_packet(packet, direction))
        nfqueue.run()

    
    def end_packet_capture(self):
        subprocess.run(["sudo", "sysctl", "net.ipv4.ip_forward=0"])
        subprocess.run(["sudo", "iptables", "-D", "FORWARD", "-j", "NFQUEUE", "--queue-num", "1"])

    def load_filter(self):
        self.incoming_ip_whitelists = self.refresh_whitelist("IP Address", "Whitelist", "Incoming")
        self.incoming_mac_whitelists = self.refresh_whitelist("MAC Address", "Whitelist", "Incoming")
        self.incoming_port_whitelists = self.refresh_whitelist("Port", "Whitelist", "Incoming")
        self.incoming_protocol_whitelists = self.refresh_whitelist("Protocol", "Whitelist", "Incoming")
        self.incoming_application_whitelists = self.refresh_whitelist("Application", "Whitelist", "Incoming")

        self.outgoing_ip_whitelists = self.refresh_whitelist("IP Address", "Whitelist", "Outgoing")
        self.outgoing_mac_whitelists = self.refresh_whitelist("MAC Address", "Whitelist", "Outgoing")
        self.outgoing_port_whitelists = self.refresh_whitelist("Port", "Whitelist", "Outgoing")
        self.outgoing_protocol_whitelists = self.refresh_whitelist("Protocol", "Whitelist", "Outgoing")
        self.outgoing_application_whitelists = self.refresh_whitelist("Application", "Whitelist", "Outgoing")

        self.incoming_ip_blacklists = self.refresh_whitelist("IP Address", "Blacklist", "Incoming")
        self.incoming_mac_blacklists = self.refresh_whitelist("MAC Address", "Blacklist", "Incoming")
        self.incoming_port_blacklists = self.refresh_whitelist("Port", "Blacklist", "Incoming")
        self.incoming_protocol_blacklists = self.refresh_whitelist("Protocol", "Blacklist", "Incoming")
        self.incoming_application_blacklists = self.refresh_whitelist("Application", "Blacklist", "Incoming")

        self.outgoing_ip_blacklists = self.refresh_whitelist("IP Address", "Blacklist", "Outgoing")
        self.outgoing_mac_blacklists = self.refresh_whitelist("MAC Address", "Blacklist", "Outgoing")
        self.outgoing_port_blacklists = self.refresh_whitelist("Port", "Blacklist", "Outgoing")
        self.outgoing_protocol_blacklists = self.refresh_whitelist("Protocol", "Blacklist", "Outgoing")
        self.outgoing_application_blacklists = self.refresh_whitelist("Application", "Blacklist", "Outgoing")

        self.incoming_ip_accept_exceptions = self.refresh_exceptions("IP Address", "Whitelist", "Incoming")
        self.incoming_mac_accept_exceptions = self.refresh_exceptions("MAC Address", "Whitelist", "Incoming")
        self.incoming_port_accept_exceptions = self.refresh_exceptions("Port", "Whitelist", "Incoming")
        self.incoming_protocol_accept_exceptions = self.refresh_exceptions("Protocol", "Whitelist", "Incoming")
        self.incoming_application_accept_exceptions = self.refresh_exceptions("Application", "Whitelist", "Incoming")

        self.outgoing_ip_accept_exceptions= self.refresh_exceptions("IP Address", "Whitelist", "Outgoing")
        self.outgoing_mac_accept_exceptions = self.refresh_exceptions("MAC Address", "Whitelist", "Outgoing")
        self.outgoing_port_accept_exceptions = self.refresh_exceptions("Port", "Whitelist", "Outgoing")
        self.outgoing_protocol_accept_exceptions = self.refresh_exceptions("Protocol", "Whitelist", "Outgoing")
        self.outgoing_application_accept_exceptions = self.refresh_exceptions("Application", "Whitelist", "Outgoing")

        self.incoming_ip_deny_exceptions = self.refresh_exceptions("IP Address", "Blacklist", "Incoming")
        self.incoming_mac_deny_exceptions = self.refresh_exceptions("MAC Address", "Blacklist", "Incoming")
        self.incoming_port_deny_exceptions = self.refresh_exceptions("Port", "Blacklist", "Incoming")
        self.incoming_protocol_deny_exceptions = self.refresh_exceptions("Protocol", "Blacklist", "Incoming")
        self.incoming_application_deny_exceptions = self.refresh_exceptions("Application", "Blacklist", "Incoming")

        self.outgoing_ip_deny_exceptions= self.refresh_exceptions("IP Address", "Blacklist", "Outgoing")
        self.outgoing_mac_deny_exceptions = self.refresh_exceptions("MAC Address", "Blacklist", "Outgoing")
        self.outgoing_port_deny_exceptions = self.refresh_exceptions("Port", "Blacklist", "Outgoing")
        self.outgoing_protocol_deny_exceptions = self.refresh_exceptions("Protocol", "Blacklist", "Outgoing")
        self.outgoing_application_deny_exceptions= self.refresh_exceptions("Application", "Blacklist", "Outgoing")

        self.filter_settings = self.refresh_settings()

    def refresh_whitelist(self, type, whitelist_type, direction):
        return self.app.data_manager.fetch_whitelist(type, whitelist_type, direction)

      
    def refresh_exceptions(self, type, whitelist_type, direction):
        return self.app.data_manager.fetch_exceptions(type, whitelist_type, direction)

    def refresh_settings(self):
        return self.app.settings
    
    def process_packet(self, packet, direction):
        types = ["ip", "mac", "port", "protocol", "application"]
        packet_info = self.get_packet_info(packet)

        #Check if blacklisted or whitelisted in exceptions
        for type in types:
            deny_exception = getattr(self, direction + "_" + type + "_deny_exceptions")
            for exception in deny_exception:
                if packet_info[type] == exception[0]:
                    if packet_info[exception[1]] == packet_info[exception[2]]:
                        if self.filter_settings["enable logs"]:
                            self.app.data_manager.append_to_or_create_log("Deny Exception:" + exception[0] + exception[1] + exception[2])
                        return "drop"
                    
            accept_exception = getattr(self, direction + "_" + type + "_accept_exceptions")
            for exception in accept_exception:
                if packet_info[type] == exception[0]:
                    if packet_info[exception[1]] == packet_info[exception[2]]:
                        return "accept"

        #Check if blacklisted in whitelists 
        for type in types:
            if packet_info[type] in getattr(self, direction + "_" + type + "_blacklists"):
                if self.filter_settings["enable logs"]:
                    self.app.data_manager.append_to_or_create_log("Blacklist:" + packet_info[type])
                return "drop"
            else:
                if self.filter_settings[type + " whitelist strictness"] == "Strict":
                    if packet_info[type] in getattr(self, direction + "_" + type + "_whitelists"):
                        return "accept"
                    else:
                        if self.filter_settings["enable logs"]:
                            self.app.data_manager.append_to_or_create_log("Whitelist Strictness:" + type)
                        return "drop"
                else:
                    return "accept"

    def get_packet_info(packet):
        packet_info = {"ip": "", "mac": "", "port": "", "protocol": "", "application": "" }
        #Get IP Address
        if scapy.IP in packet:
            packet_info["ip"] = packet[scapy.IP].src
        #Get Mac Address
        if scapy.Ether in packet:
            packet_info["mac"] = packet[scapy.Ether].src
        #Get transport Layer Protocol
        packet_info["protocol"] = packet.layer4_protocol.name
        #Get Port
        if packet_info["protocol"]:
            try:
                packet_info["port"] = packet[packet_info["protocol"]].sport
            except AttributeError:
                pass
        #Geuss Application
        packet_info["application"] = packet[scapy.Raw].guess_payload_class().__name__
        #Retrun information
        return packet_info



    
        
