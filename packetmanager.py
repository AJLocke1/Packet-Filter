#Only works on Linux Systems
import subprocess
import scapy
from netfilterqueue import NetfilterQueue

class Packet_Manager():
    def __init__(self, App):
        self.blacklisted_ip_addresses = []
        self.blacklisted_port_numbers = []
        self.blacklisted_protocols = []
        self.blacklisted_applications = []
        self.blacklisted_mac_addresses = []

        self.load_whitelists(App)

        print(self.blacklisted_applications)

    def initiatePacketCapture(self):
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
        finally:
            # Cleanup: Disable packet forwarding and remove iptables rule
            subprocess.run(["sudo", "sysctl", "net.ipv4.ip_forward=0"])
            subprocess.run(["sudo", "iptables", "-D", "FORWARD", "-j", "NFQUEUE", "--queue-num", "1"])

    def process_packet(self, packet):
        packet_data = self.get_packet_infomation(packet)
        if self.is_blocked_by_whitelists(packet_data) is False:
            packet.accept()
        if self.is_blocked_by_machine_learning is False:
            packet.accept()
        if self.is_blocked_by_rules is False:
            packet.accept()

    def is_blocked_by_whitelists(self, packet_data):
        if packet_data["ip_scr"] in self.blacklisted_ip_addresses:
            return True
        if packet_data["tcp_sport"] or packet_data["udp_sport"] in self.blacklisted_ports:
            return True
        if packet_data["l4_protocol"] in self.blacklisted_protocols:
            return True
        if packet_data["l7_protocol"] in self.blacklisted_applications:
            return True
        if packet_data["eth_src"] in self.blacklisted_mac_addresses:
            return True
        return False

    
    def is_blocked_by_rules(self, packet_data):
        return False
    
    def is_blocked_by_machine_learning(self, packet_data):
        return False
    
    def get_packet_infomation(self, packet):
        packet_info = {}
        # Get Layer 2 Information
        if packet.haslayer("Ether"):
            ethernet_layer = packet["Ether"]
            packet_info['eth_src'] = ethernet_layer.src
            packet_info['eth_dst'] = ethernet_layer.dst
            packet_info['eth_type'] = ethernet_layer.type

            if "Dot1Q" in ethernet_layer:
                vlan_info = ethernet_layer["Dot1Q"]
                packet_info['vlan'] = vlan_info.vlan
                packet_info['vlan_prio'] = vlan_info.prio
                packet_info['vlan_dei'] = vlan_info.dei

        # Get Layer 3 Information
        if packet.haslayer('IP'):
            ip_layer = packet['IP']
            packet_info['ip_version'] = ip_layer.version
            packet_info['ip_src'] = ip_layer.src
            packet_info['ip_dst'] = ip_layer.dst
            packet_info['ip_proto'] = ip_layer.proto
            packet_info['ip_ihl'] = ip_layer.ihl
            packet_info['ip_len'] = ip_layer.len
            packet_info['ip_ttl'] = ip_layer.ttl
            packet_info['ip_tos'] = ip_layer.tos  # Differentiated Services Code Point (DSCP)
            packet_info['ip_id'] = ip_layer.id
            packet_info['ip_flags'] = ip_layer.flags
            packet_info['ip_frag'] = ip_layer.frag

            packet_info['l4_protocol'] = ip_layer.proto

            # Get Layer 4 Information
            if ip_layer.proto == 6:  # TCP protocol
                tcp_layer = packet['TCP']
                packet_info['tcp_sport'] = tcp_layer.sport
                packet_info['tcp_dport'] = tcp_layer.dport
                packet_info['tcp_seq'] = tcp_layer.seq
                packet_info['tcp_ack'] = tcp_layer.ack
                packet_info['tcp_dataofs'] = tcp_layer.dataofs
                packet_info['tcp_flags'] = tcp_layer.flags
                packet_info['tcp_window'] = tcp_layer.window
                packet_info['tcp_chksum'] = tcp_layer.chksum
                packet_info['tcp_urgptr'] = tcp_layer.urgptr

            elif ip_layer.proto == 17:  # UDP protocol
                udp_layer = packet['UDP']
                packet_info['udp_sport'] = udp_layer.sport
                packet_info['udp_dport'] = udp_layer.dport
                packet_info['udp_len'] = udp_layer.len
                packet_info['udp_chksum'] = udp_layer.chksum

            elif ip_layer.proto == 1:  # ICMP protocol
                icmp_layer = packet['ICMP']
                packet_info['icmp_type'] = icmp_layer.type
                packet_info['icmp_code'] = icmp_layer.code
                packet_info['icmp_chksum'] = icmp_layer.chksum
                packet_info['icmp_id'] = icmp_layer.id
                packet_info['icmp_seq'] = icmp_layer.seq

        packet_info['l7_protocol'] = packet.payload.guess_payload_class()
        
        return packet_info

    def test_mock_packet(self, protocol, s_ip, d_ip, s_port, d_port):
        if protocol == "TCP":
            mock_packet = scapy.IP(src=s_ip, dst=d_ip) / scapy.TCP(sport=s_port, dport=d_port)
        elif protocol == "UDP":
            mock_packet = scapy.IP(src=s_ip, dst=d_ip) / scapy.UDP(sport=s_port, dport=d_port)
        elif protocol == "ICMP":
            mock_packet = scapy.IP(src=s_ip, dst=d_ip) / scapy.ICMP(sport=s_port, dport=d_port)
        
        self.nfqueue.queue.put(str(mock_packet))

    def load_whitelists(self, App):
        self.blacklisted_ip_addresses = App.data_manager.fetch_whitelists("Address")
        self.blacklisted_port_numbers = App.data_manager.fetch_whitelists("Port")
        self.blacklisted_protocols = App.data_manager.fetch_whitelists("Protocol")
        self.blacklisted_applications = App.data_manager.fetch_whitelists("Application")
        self.blacklisted_mac_addresses = App.data_manager.fetch_whitlists("MAC Address")
        
    
        