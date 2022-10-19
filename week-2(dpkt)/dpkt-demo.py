import dpkt
import sys
def process_capture(pcap_file):
    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        # iterate over each pacet in the capture
        for ts, buf in pcap:
            print('-------------------------')
            # gives you the link layer content
            eth = dpkt.ethernet.Ethernet(buf)

            # make sure the packet is an IP packet
            if not isinstance(eth.data, dpkt.ip.IP):
                # print('Non IP Packet type not supported %s' % eth.data.__class__.__name__)
                continue

            # gives you the network layer content
            ip = eth.data


            # gives you the transport layer content
            tcp = ip.data

            # make sure the packet is a TCP packet
            if not isinstance(tcp, dpkt.tcp.TCP):
                # print('Non TCP Packet type not supported %s' % tcp.__class__.__name__)
                continue
            else:
              

                # check if the packet is an HTTP packet
                if tcp.dport == 80 and len(tcp.data) > 0:
                    print('HTTP Request')
                      # print out the source and destination IP addresses
                    print('Source Port: %s' % tcp.sport)
                    print('Destination Port: %s' % tcp.dport)
                    if len(tcp.data) > 0:
                        try:
                            http = dpkt.http.Request(tcp.data)
                            print(http)
                        except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                          continue
                elif tcp.sport == 80 and len(tcp.data) >= 0:
                    print('HTTP Response')
                      # print out the source and destination IP addresses
                    print('Source Port: %s' % tcp.sport)
                    print('Destination Port: %s' % tcp.dport)
                    if len(tcp.data) > 0:
                        try:
                            http = dpkt.http.Response(tcp.data)
                            print(http.body.decode())
                        except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                            continue
                else:
                    # non HTTP packet
                    continue
              

if __name__ == '__main__':
  # check if argument is provided
  if len(sys.argv) != 2:
    print("Usage: python3 dpkt-demo.py capture.pcap")
    sys.exit(1)
  else:
    process_capture(sys.argv[1])
