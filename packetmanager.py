#Only works on Linux Systems
import subprocess
import scapy
from netfilterqueue import NetfilterQueue

class Packet_Manager():
    def __init__(self, App):
        self.blacklisted_ip_addresses = []
        self.blacklisted_port_numbers = []
        self.blacklisted_protocols = []
        self.blacklisted_Applications = []

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
        return False
    
    def is_blocked_by_rules(self, packet_data):
        return False
    
    def is_blocked_by_machine_learning(self, packet_data):
        return False
    
    def get_packet_infomation(self, packet):
        packet_info = []
        #Get Layer 2 Infomation
        if packet.haslayer("Ether"):
            ethernet_layer = packet["Ether"]
            packet_info.append(ethernet_layer.src)
            packet_info.append(ethernet_layer.dst)
            packet_info.append(ethernet_layer.type)

            if ["Dot1Q"] in ethernet_layer:
                vlan_info = ethernet_layer["Dot1Q"]
                packet_info.append(vlan_info.vlan)
                packet_info.append(vlan_info.prio)
                packet_info.append(vlan_info.dei)

        #Get Layer 3 Infomation
        if packet.haslayer('IP'):
            ip_layer = packet['IP']
            packet_info.append(ip_layer.version)
            packet_info.append(ip_layer.src)
            packet_info.append(ip_layer.dst)
            packet_info.append(ip_layer.proto)
            packet_info.append(ip_layer.ihl)
            packet_info.append(ip_layer.len)
            packet_info.append(ip_layer.ttl)
            packet_info.append(ip_layer.tos)  # Differentiated Services Code Point (DSCP)
            packet_info.append(ip_layer.id)
            packet_info.append(ip_layer.flags)
            packet_info.append(ip_layer.frag)

            #Get layer 4 infomation
            if ip_layer.proto == 6:  # TCP protocol
                tcp_layer = packet['TCP']
                packet_info.append(tcp_layer.sport)
                packet_info.append(tcp_layer.dport)
                packet_info.append(tcp_layer.seq)
                packet_info.append(tcp_layer.ack)
                packet_info.append(tcp_layer.dataofs)
                packet_info.append(tcp_layer.flags)
                packet_info.append(tcp_layer.window)
                packet_info.append(tcp_layer.chksum)
                packet_info.append(tcp_layer.urgptr)

            elif ip_layer.proto == 17:  # UDP protocol
                udp_layer = packet['UDP']
                packet_info.append(udp_layer.sport)
                packet_info.append(udp_layer.dport)
                packet_info.append(udp_layer.len)
                packet_info.append(udp_layer.chksum)

            elif ip_layer.proto == 1:  # ICMP protocol
                icmp_layer = packet['ICMP']
                packet_info.append(icmp_layer.type)
                packet_info.append(icmp_layer.code)
                packet_info.append(icmp_layer.chksum)
                packet_info.append(icmp_layer.id)
                packet_info.append(icmp_layer.seq)
                
        return packet_info

    def test_mock_packet(self, protocol, s_ip, d_ip, s_port, d_port):
        if protocol == "TCP":
            mock_packet = scapy.IP(src=s_ip, dst=d_ip) / scapy.TCP(sport=s_port, dport=d_port)
        elif protocol == "UDP":
            mock_packet = scapy.IP(src=s_ip, dst=d_ip) / scapy.UDP(sport=s_port, dport=d_port)
        elif protocol == "ICMP":
            mock_packet = scapy.IP(src=s_ip, dst=d_ip) / scapy.ICMP(sport=s_port, dport=d_port)
        
        self.nfqueue.queue.put(str(mock_packet))

    def load_whitelists(self):
        App.da

    
        