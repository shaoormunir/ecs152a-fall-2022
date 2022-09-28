import dpkt
import sys
def process_capture(pcap_file):
    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if not isinstance(eth.data, dpkt.ip.IP):
                print('Non IP Packet type not supported %s' % eth.data.__class__.__name__)
                continue
            ip = eth.data
            tcp = ip.data
            print(f"Source: {ip.src} Destination: {ip.dst} Protocol: {ip.p}")
            print(f"Source Port: {tcp.sport} Destination Port: {tcp.dport}")

            tcp = ip.data
            if isinstance(tcp.data, dpkt.http.Request):
                http = tcp.data
                print(f"HTTP Request: {http.uri}")
            elif isinstance(tcp.data, dpkt.http.Response):
                http = tcp.data
                print(f"HTTP Response: {http.status_line}")
            else:
                print(f"TCP Data: {tcp.data}")
            

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
            
            # check if the packet is a http packet
            if len(data) <= 0 or tcp.sport != 80:
                continue
                
            # print response body
            http = dpkt.http.Response(tcp.data)
            print(http.body.decode())

if __name__ == '__main__':
  # check if argument is provided
  if len(sys.argv) != 2:
    print("Usage: python3 dpkt-demo.py capture.pcap")
    sys.exit(1)
  else:
    process_capture(sys.argv[1])
