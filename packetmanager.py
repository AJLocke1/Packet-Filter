#Only works on Linux Systems
import multiprocessing.process
import subprocess
import scapy.all as sc
import threading
import multiprocessing
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

        self.load_filter()

        self.num_processes = 4  # Adjust this value based on the number of CPU cores
        self.packet_queue = multiprocessing.Queue()
        self.initiate_packet_capture()

    def initiate_packet_capture(self):
        try:
            #Enable packet forwarding
            subprocess.run(["sudo", "sysctl", "net.ipv4.ip_forward=1"], check=True)
            #Add iptables rule to forward packets to NFQUEUE
            subprocess.run(["sudo", "iptables", "-A", "FORWARD", "-o", "br0", "-m", "physdev", "--physdev-out", self.outbound_interface, "-j", "NFQUEUE", "--queue-num", "1"], check=True)
            subprocess.run(["sudo", "iptables", "-A", "FORWARD", "-o", "br0", "-m", "physdev", "--physdev-out", self.inbound_interface, "-j", "NFQUEUE", "--queue-num", "0"], check=True)

            process = multiprocessing.Process(target=self.bind_nfqueue, args=(0, "outgoing"))
            process_2 = multiprocessing.Process(target=self.bind_nfqueue, args=(1, "incoming"))
            process.daemon = True
            process_2.daemon = True
            process.start()
            process_2.start()

        except KeyboardInterrupt:
            print("Firewall Interrupted")
        except subprocess.CalledProcessError as e:
            print("Error occurred:", e)
    
    def bind_nfqueue(self, queue_number, direction):
        nfqueue = NetfilterQueue()
        nfqueue.bind(queue_number, lambda packet: self.process_packet(queue_number, packet, direction))
        nfqueue.run()
    
    def end_packet_capture(self):
        subprocess.run(["sudo", "sysctl", "net.ipv4.ip_forward=0"])
        subprocess.run(["sudo", "iptables", "-D", "FORWARD", "-o", "br0", "-m", "physdev", "--physdev-out", self.outbound_interface, "-j", "NFQUEUE", "--queue-num", "1"])
        subprocess.run(["sudo", "iptables", "-D", "FORWARD", "-o", "br0", "-m", "physdev", "--physdev-out", self.inbound_interface, "-j", "NFQUEUE", "--queue-num", "0"])

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
        return self.app.data_manager.fetch_whitelists(type, whitelist_type, direction)

    def refresh_exceptions(self, type, whitelist_type, direction):
        return self.app.data_manager.fetch_exceptions(type, whitelist_type, direction)

    def refresh_settings(self):
        return self.app.settings
    

    def process_packet(self, queue_num, packet, direction):
        scapy_packet = sc.IP(packet.get_payload())
        #used to access the classes filter lists
        types = ["ip", "mac", "port", "protocol", "application"]
        #get only the neccessary packet info for filtering
        packet_info = self.get_packet_info(scapy_packet)
        #Check for killswitch or filter disabling
        if self.filter_settings["enable filtering"] == "False":
            return "accept"
        if self.filter_settings["enable killswitch"] == "True":
            if self.filter_settings["enable logs"] == "True":
                self.app.data_manager.append_to_or_create_log("Killswitch")
            return "drop"

        #Check if blacklisted or whitelisted in exceptions
        drop = 0
        accept = 0
        for type in types:
            deny_exceptions = getattr(self, direction + "_" + type + "_deny_exceptions")
            for exception in deny_exceptions:
                if packet_info[type] == exception[0]:
                    if packet_info[exception[1]] == exception[2]:
                        drop +=1
                      
            accept_exceptions = getattr(self, direction + "_" + type + "_accept_exceptions")
            for exception in accept_exceptions:
                if packet_info[type] == exception[0]:
                    if packet_info[exception[1]] == exception[2]:
                        accept += 1

        if drop == 0 and accept == 0:
            pass
        else:
            if drop > accept:
                if self.filter_settings["enable logs"] == "True":
                    self.app.data_manager.append_to_or_create_log("Deny Exception: " + exception[0] + exception[1] + exception[2])
                return "drop"
            else:
                return "allow"


        #Check if blacklisted in whitelists 
        for type in types:
            if packet_info[type] in getattr(self, direction + "_" + type + "_blacklists"):
                if self.filter_settings["enable logs"] == "True":
                    self.app.data_manager.append_to_or_create_log("Blacklist: " + packet_info[type])
                return "drop"
            else:
                if self.filter_settings[type + " whitelist strictness"] == "Strict":
                    if packet_info[type] in getattr(self, direction + "_" + type + "_whitelists"):
                        pass
                    else:
                        if self.filter_settings["enable logs"] == "True":
                            self.app.data_manager.append_to_or_create_log("Whitelist Strictness: " + type)
                        return "drop"
                else:
                    pass
        return "accept"

    def get_packet_info(self, packet):
        packet_info = {"ip": "", "mac": "", "port": "", "protocol": "", "application": "" }
        #Get IP Address
        if sc.IP in packet:
            packet_info["ip"] = packet[sc.IP].src
        #Get Mac Address
        if sc.Ether in packet:
            packet_info["mac"] = packet[sc.Ether].src
        #Get transport Layer Protocol
        protocol_numbers = {6: "TCP", 17: "UDP", 1: "ICMP", 132: "SCTP", 33: "DCCP", 47: "GRE", 46: "RSVP", 115: "L2TP", 2: "IGMP", 137: "MPLS", 17: "QUIC", 103: "RTP", 254: "SRTP", 35: "LISP", 20: "WireGuard"}
        packet_info["protocol"] = protocol_numbers[packet[sc.IP].proto]
        #Get Port
        if packet_info["protocol"]:
            try:
                if packet_info["protocol"] == "QUIC":
                    try:
                        packet_info["port"] = str(packet[packet_info["protocol"]].sport)
                    except Exception:
                        packet_info["port"] = str(packet["UDP"].sport)
                        packet_info["protocol"] = "UDP"
                packet_info["port"] = str(packet[packet_info["protocol"]].sport)
            except Exception:
                pass
        #Geuss Application
        if packet.payload is None:
            packet_info["application"] == "Unkown"
        else:
            packet_info["application"] = packet.payload.guess_payload_class(packet.payload).__name__
        #Retrun information
        return packet_info
    
    def test_filter_logic(self, num_tests):
        test_results = []
        for test in range(num_tests):
            packet = self.generate_packet()
            test_result = self.process_packet(packet)
            packet_info = self.get_packet_info(packet)
            test_results.append(test_result, packet_info)
        return test_results
 
    def generate_packet(self):
        src_ip = sc.RandIP()
        dst_ip = sc.RandIP()
        ip_packet = sc.IP(src=src_ip, dst=dst_ip)

        src_mac = sc.RandMAC()
        dst_mac = sc.RandMAC()
        ether_packet = sc.Ether(src=src_mac, dst=dst_mac)

        protocol = ["UDP", "TCP", "ICMP"]
        src_port = sc.RandNum(1, 1024)
        dst_port = sc.RandNum(1024, 65535)
        match protocol:
            case "UDP":
                transport_layer = sc.UPD(src=src_port, dst=dst_port)
            case "ICMP":
                transport_layer = sc.TCP(src=src_port, dst=dst_port)
            case "TCP":
                transport_layer = sc.ICMP(src=src_port, dst=dst_port)
        

        packet = ether_packet / ip_packet / transport_layer

        return packet
    
        
