from _socket import gethostbyaddr
from random import randint

from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, TCP, ICMP, traceroute, UDP
from scapy.layers.l2 import ARP, Ether


def synScan(dstip, dstport=80, timeout=5, iface=conf.iface):
    """
    使用syn包对dstip范围和dstport范围的进程进行扫描

    :param dstip:目标主机（集）
    :param dstport:目标端口（集）
    :param timeout:发送完数据包后等待的最长时间
    :param iface:选择网卡
    :return:返回回应数据包及响应集 和 未响应数据包集
    """
    return sr(IP(dst=dstip) / TCP(sport=RandShort(), iface=iface, dport=dstport, flags="S"), threaded=True,
              timeout=timeout,
              filter="tcp")


def ackScan(dstip, dstport=80, timeout=5, iface=conf.iface):
    """
    使用ack包对dstip范围和dstport范围的进程进行扫描

    :param dstip:目标主机（集）
    :param dstport:目标端口（集）
    :param timeout:发送完数据包后等待的最长时间
    :param iface:选择网卡
    :return:返回回应数据包及响应集 和 未响应数据包集
    """
    return sr(IP(dst=dstip) / TCP(sport=RandShort(), dport=dstport, iface=iface, flags="A"), threaded=True,
              timeout=timeout,
              filter="tcp")


def xmasScan(dstip, dstport=666, timeout=5, iface=conf.iface):
    """
    使用xmas包(flag为'FPU'的tcp包)对dstip范围和dstport范围的进程进行扫描

    :param dstip:目标主机（集）
    :param dstport:目标端口（集）
    :param timeout:发送完数据包后等待的最长时间
    :param iface:选择网卡
    :return:返回回应数据包及响应集 和 未响应数据包集
    """
    return sr(IP(dst=dstip) / TCP(dport=dstport, flags="FPU"), iface=iface, threaded=True, timeout=timeout,
              filter="tcp")


def ipScan(dstip, proto, timeout=5, iface=conf.iface):
    """
    使用ip包对dstip范围和proto协议范围进行扫描

    :param dstip:目标主机（集）
    :param proto:目标协议（集）
    :param timeout:发送完数据包后等待的最长时间
    :param iface:选择网卡
    :return:返回回应数据包及响应集 和 未响应数据包集
    """
    return sr(IP(dst=dstip, proto=proto) / "SCAPY", retry=2, iface=iface, threaded=True, timeout=timeout, filter="ip")


def arpPing(dstnet, timeout=2, iface=conf.iface):
    """
    扫描局域网内目标ip网段的网络主机

    :param dstnet:局域网内目标网段
    :param timeout:发送完数据包后等待的最长时间
    :param iface:选择网卡
    :param iface:选择网卡
    :return:返回回应数据包及响应集 和 未响应数据包集
    """
    return srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=dstnet), iface=iface, threaded=True, timeout=timeout,
               filter="arp")


def icmpPing(dstnet, retry=3, count=4, timeout=3, iface=conf.iface):
    """
    模拟ping

    :param count:发送个数
    :param dstnet:目标主机(集)
    :param timeout:发送完数据包后等待的最长时间
    :param iface:选择网卡
    :return:返回回应数据包及响应集 和 未响应数据包集
    """
    if isinstance(iface, str):
        iface = IFACES.dev_from_name(iface)
    return srloop(
        [IP(src=iface.ip, dst=dstnet) / ICMP(id=1, seq=randint(30, 50)) / b'abcdefghijklmnopqrstuvwabcdefghi' for i in
         range(count)],
        threaded=True, iface=iface, timeout=timeout, filter="icmp", retry=retry, count=1)


def tcpTraceroute(dstip, mttl=10, timeout=3, iface=conf.iface):
    """
    使用tcp协议进行traceroute

    :param dstip:目的主机
    :param mttl:最大ttl
    :param timeout:发送完数据包后等待的最长时间
    :param iface:选择网卡
    :return:返回回应数据包及响应集 和 未响应数据包集
    """
    return sr(IP(dst=dstip, ttl=(1, mttl)) / TCP(dport=53, flags="S"), iface=iface, threaded=True, timeout=timeout,
              filter="tcp")


def udpTraceroute(dstip, mttl=10, timeout=3, iface=conf.iface):
    """
    使用udp协议进行traceroute

    :param dstip:目的主机
    :param mttl:最大ttl
    :param timeout:发送完数据包后等待的最长时间
    :param iface:选择网卡
    :return:返回回应数据包及响应集 和 未响应数据包集
    """
    return sr(IP(dst=dstip, ttl=(1, mttl)) / UDP() / DNS(qd=DNSQR(qname="test.com")), iface=iface, threaded=True,
              timeout=timeout,
              filter=None)


def arpScanHost(dstip, iface):
    """
    扫描局域网的主机，返回ip地址和主机名元组的列表

    :param dstip:目的主机(集)
    :param iface:选择的网卡
    :return:返回ip地址和主机名元组的列表
    """
    ans, unans = arpPing(dstnet=dstip, iface="以太网")
    res = []
    tmp = len(ans)
    for (s, r) in ans:
        print(f"还剩{tmp}个地址待解析")
        tmp -= 1
        dip = s["ARP"].pdst
        try:
            res.append((dip, gethostbyaddr(dip)))
        except:
            pass
    return res
