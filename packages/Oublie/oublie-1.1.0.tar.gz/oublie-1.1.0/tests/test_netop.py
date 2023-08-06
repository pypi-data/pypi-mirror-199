from _socket import gethostbyaddr

from src.Oublie.netop import *

ans, unans = None, None

# ans,unans=synSCAN("172.16.14.87",80)

# ans, unans = sr(IP(dst="127.0.0.1")/ICMP(), timeout=3)
# ans.summary(lambda s,r: r.sprintf("%IP.src% is alive") )

# ans, unans = xmasScan("172.16.76.91")

# ans, unans = sr(IP(dst="127.0.0.1",proto=80)/"SCAPY",retry=2)

# ans.summary(lambda s,r:(s.summary(),r.summary()))

# ans, unans = ackScan("172.16.76.91",(80,90))

# ans, unans = arpPing("172.16.76.0/24", iface="以太网")

ans, unans = icmpPing("172.16.76.1", timeout=5, iface='以太网')

# ans, unans = tcpTraceroute("172.16.14.1", 3, )

# ans, unans = icmpPing("172.16.76.1", 10, iface='以太网')

# ans, unans = udpTraceroute("172.16.76.1", 3, 3)

# res = arpScanHost("172.16.76.0/27", "以太网")
# print(res)

# for i in ans:
#     i.show()

ans.summary()
print("----")
if unans != None:
    unans.summary()

# if ans:
#     print(ans.summary)
# else:
#     print("没有响应")

# print(conf.route.route("172.16.14.1"))
# ifa = IFACES.dev_from_name('以太网')
# print(ifa.name, ifa.index, ifa.network_name, ifa.description)
