import dpkt
import sys
def process_capture(pcap_file):
    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            # gives you the link layer content
            eth = dpkt.ethernet.Ethernet(buf)
            if not isinstance(eth.data, dpkt.ip.IP):
                print('Non IP Packet type not supported %s' % eth.data.__class__.__name__)
                continue

            # gives you the network layer content
            ip = eth.data
            # gives you the transport layer content
            tcp = ip.data
            print(f"Source: {ip.src} Destination: {ip.dst} Protocol: {ip.p}")
            print(f"Source Port: {tcp.sport} Destination Port: {tcp.dport}")

            # gives you the transport layer content
            tcp = ip.data
            if isinstance(tcp.data, dpkt.http.Request):
                # gives you the application layer content
                http = tcp.data
                print(f"HTTP Request: {http.uri}")
            elif isinstance(tcp.data, dpkt.http.Response):
                # gives you the application layer content
                http = tcp.data
                print(f"HTTP Response: {http.status_line}")
            else:
                print(f"TCP Data: {tcp.data}")

if __name__ == '__main__':
  # check if argument is provided
  if len(sys.argv) != 2:
    print("Usage: python3 dpkt-demo.py capture.pcap")
    sys.exit(1)
  else:
    process_capture(sys.argv[1])
