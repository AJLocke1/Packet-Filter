#Only works on Linux Systems
import subprocess
import scapy
from netfilterqueue import NetfilterQueue

class Packet_Manager():
    def __init__(self, App):
        self.app = App

        self.blacklisted_ip_addresses = []
        self.blacklisted_port_numbers = []
        self.blacklisted_protocols = []
        self.blacklisted_applications = []
        self.blacklisted_mac_addresses = []

        self.whitelisted_ip_addresses = []
        self.whitelisted_mac_addresses = []
        self.whitelisted_port_numbers = []
        self.whitelisted_protocols = []
        self.whitelisted_applications = []

        self.exceptions = []

        self.filter_settings = {}

        self.load_filter()
        self.initiate_packet_capture()

    def initiate_packet_capture(self):
        try:
            # Enable packet forwarding
            subprocess.run(["sudo", "sysctl", "net.ipv4.ip_forward=1"], check=True)
            # Add iptables rule to forward packets to NFQUEUE
            subprocess.run(["sudo", "iptables", "-A", "FORWARD", "-j", "NFQUEUE", "--queue-num", "1"], check=True)
            # Bind NetfilterQueue
            self.nfqueue = NetfilterQueue()
            self.nfqueue.bind(1, self.process_packet)
            self.nfqueue.run()
        except KeyboardInterrupt:
            print("Firewall Interrupted")
        except subprocess.CalledProcessError as e:
            print("Error occurred:", e)
    
    def end_packet_capture(self):
        subprocess.run(["sudo", "sysctl", "net.ipv4.ip_forward=0"])
        subprocess.run(["sudo", "iptables", "-D", "FORWARD", "-j", "NFQUEUE", "--queue-num", "1"])

    def load_filter(self):
        self.blacklisted_ip_addresses = self.refresh_whitelist("IP Address", "Whitelist")
        self.blacklisted_port_numbers = self.refresh_whitelist("Port", "Whitelist")
        self.blacklisted_protocols  = self.refresh_whitelist("Protocol", "Whitelist")
        self.blacklisted_applications = self.refresh_whitelist("Application", "Whitelist")
        self.blacklisted_mac_addresses = self.refresh_whitelist("MAC Address", "Whitelist")

        self.whitelisted_ip_addresses = self.refresh_whitelist("IP Address", "Blacklist") 
        self.whitelisted_mac_addresses = self.refresh_whitelist("MAC Address", "Blacklist")
        self.whitelisted_port_numbers = self.refresh_whitelist("Port", "Blacklist")
        self.whitelisted_protocols = self.refresh_whitelist("Protocol", "Blacklist")
        self.whitelisted_applications = self.refresh_whitelist("Application", "Blacklist")

        self.exceptions = self.refresh_exceptions()


    def refresh_whitelist(self, type, whitelist_type):
        return self.app.data_manager.fetch_whitelist(type, whitelist_type)

    def refresh_exceptions(self):
        return self.app.data_manager.fetch_exceptions()

    def refresh_settings(self):
        return self.app.data_manager.read_settings()
    
    def process_packet(self, packet):
        if self.is_blocked_by_whitelists(packet) is False:
            packet.accept()
        if self.is_blocked_by_machine_learning(packet) is False:
            packet.accept()
        if self.is_blocked_by_exceptions(packet) is False:
            packet.accept()


    
        
