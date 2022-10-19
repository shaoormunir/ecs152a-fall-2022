import dpkt

# create a reader
f = open('testfile.pcap', 'rb')
pcap = dpkt.pcap.Reader(f)

# iterate over the pcap
for ts, buf in pcap:
    
    # gives you the link layer content
    eth = dpkt.ethernet.Ethernet(buf)
    
    if not isinstance(eth.data, dpkt.ip.IP):
        continue
    
    # gives you the network layer content
    ip = eth.data
    
    if isinstance(ip.data, dpkt.tcp.TCP):
        print('TCP')
    elif isinstance(ip.data, dpkt.udp.UDP):
        print('UDP')
    else:
        print('Other')