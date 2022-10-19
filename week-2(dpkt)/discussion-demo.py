import dpkt

# create a reader
f = open('capture.pcap', 'rb')
pcap = dpkt.pcap.Reader(f)

# iterate over the pcap
for ts, buf in pcap:
    
    # gives you the link layer content
    eth = dpkt.ethernet.Ethernet(buf)
    
    if not isinstance(eth.data, dpkt.ip.IP):
        continue
    
    # gives you the network layer content
    ip = eth.data
    
    if not isinstance(ip.data, dpkt.tcp.TCP):
        continue
    
    # gives you the transport layer content
    tcp = ip.data
    
    # gives you the application layer content
    data = tcp.data
    
    # # check if the packet is a http packet
    # if len(data) <= 0 or tcp.sport != 80:
    #     continue

    if len(data) <= 0 or tcp.dport != 80:
        continue
        
    # print response body
    try:
      http = dpkt.http.Request(tcp.data)
      print(http)
    except Exception as e:
      print(e)
      continue