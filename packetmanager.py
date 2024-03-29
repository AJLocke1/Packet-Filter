#Only works on Linux Systems
import scapy
from netfilterqueue import NetfilterQueue

class PacketManager():
    def initiatePacketCapture(self):
        self.nfqueue = NetfilterQueue()
        self.nfqueue.bind(1, self.processPacket)
        try:
            self.nfqueue.run()
        except KeyboardInterrupt:
            print("Firewall Inturupted")

    def get_packet_infomation(packet):
        """
        Infomation is stored in the order of mandatory fields followed by optional
        
        Source Mac Adddress
        Destination Mac Address
        Type 

        IP Version,
        Source IP,
        Destination IP, 
        IP Protocol, 
        IP header Lenght,
        IP total length
        IP Time To Live,

        Source port, 
        Destination Port
        """
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
    
        