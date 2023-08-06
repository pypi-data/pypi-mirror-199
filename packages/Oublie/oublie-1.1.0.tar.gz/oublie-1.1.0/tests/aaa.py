# Script: pyping.py
# Author: s0lst1c3
# Description: It's ping. In Python. With Scapy. Yep.

from scapy.all import *
from argparse import ArgumentParser

from scapy.layers.inet import IP, ICMP


def set_configs():
    parser = ArgumentParser()

    parser.add_argument('-c',
                        dest='count',
                        required=False,
                        type=int,
                        default=1,
                        metavar='N',
                        help='Send N packets to destination.')

    parser.add_argument(dest='dst',
                        type=str,
                        metavar='<destination address>',
                        help='The IP address to send packets to.')

    args = parser.parse_args()

    return {'count': args.count, 'dst': args.dst}


def main():
    configs = set_configs()

    srloop(IP(dst=configs['dst']) / ICMP(), count=configs['count'])


if __name__ == '__main__':
    main()
