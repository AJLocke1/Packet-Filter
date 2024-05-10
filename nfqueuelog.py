from netfilterqueue import NetfilterQueue

def print_packet(pkt):
    print(pkt)

# Create a NetfilterQueue object for each NFQUEUE number
nfqueue_outbound = NetfilterQueue()
nfqueue_inbound = NetfilterQueue()

# Bind each NetfilterQueue object to its respective NFQUEUE number
nfqueue_outbound.bind(1, print_packet)
nfqueue_inbound.bind(0, print_packet)

try:
    # Run the NFQUEUEs
    nfqueue_outbound.run()
    nfqueue_inbound.run()
except KeyboardInterrupt:
    pass

# Unbind the NFQUEUEs
nfqueue_outbound.unbind()
nfqueue_inbound.unbind()