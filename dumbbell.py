# CMU 18731 HW3
# Code referenced from: git@bitbucket.org:huangty/cs144_bufferbloat.git
# Edited by: Soo-Jin Moon, Deepti Sunder Prakash

#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

import sys
import os
import code

# Parse arguments

parser = ArgumentParser(description="Shrew tests")
parser.add_argument('--bw-host', '-B',
                    dest="bw_host",
                    type=float,
                    action="store",
                    help="Bandwidth of host links",
                    required=True)
parser.add_argument('--bw-net', '-b',
                    dest="bw_net",
                    type=float,
                    action="store",
                    help="Bandwidth of network link",
                    required=True)
parser.add_argument('--delay',
                    dest="delay",
                    type=float,
                    help="Delay in milliseconds of host links",
                    default='10ms')
parser.add_argument('--n',
                    dest="n",
                    type=int,
                    action="store",
                    help="Number of nodes in one side of the dumbbell.",
                    required=True)

parser.add_argument('--maxq',
                    dest="maxq",
                    action="store",
                    help="Max buffer size of network interface in packets",
                    default=1000)

# Expt parameters
args = parser.parse_args()

class DumbbellTopo(Topo):
    "Dumbbell topology for Shrew experiment"
    def build(self, n=6, bw_net=100, delay='20ms', bw_host=10, maxq=None):
    #TODO: Add your code to create topology
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        hl = []
        hr = []
        for i in range(n / 2 - 1):
            hl.append(self.addHost('hl%s' % (i + 1)))
            hr.append(self.addHost('hr%s' % (i + 1)))
            self.addLink(node1=s1, node2=hl[-1], bw=bw_host, delay=delay, max_queue_size=maxq)
            self.addLink(node1=s2, node2=hr[-1], bw=bw_host, delay=delay, max_queue_size=maxq)

        a1 = self.addHost('a1')
        a2 = self.addHost('a2')

        self.addLink(node1=s1, node2=a1, bw=bw_host, delay=delay, max_queue_size=maxq)
        self.addLink(node1=s2, node2=a2, bw=bw_host, delay=delay, max_queue_size=maxq)

        self.addLink(node1=s1, node2=s2, bw=bw_net, delay=delay, max_queue_size=maxq)


def bbnet():
    "Create network and run shrew  experiment"
    print "starting mininet ...."
    topo = DumbbellTopo(n=args.n, bw_net=args.bw_net,
                    delay='%sms' % (args.delay),
                    bw_host=args.bw_host, maxq=int(args.maxq))

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink,
                  autoPinCpus=True)
    net.start()
    dumpNodeConnections(net.hosts)

    #TODO: Add your code to test reachability of hosts
    net.pingAll()

    #TODO: Add your code to start long lived TCP flows
    for i in range(args.n / 2 - 1):
        net.hosts[2 + i].cmd('iperf -s -p ' + str(5001 + i) + ' -t 600 &')
        net.hosts[2 + (args.n / 2  - 1) + i].cmd('iperf -c 10.0.0.' + str(i + 3) + ' -p ' + str(5001 + i) + ' -t 600 &')
        # For part 2:
        break

    # code.interact(local=locals())

    CLI(net)
    net.stop()

if __name__ == '__main__':
    bbnet()
