import os
from IPy import IP
import pprint
import prettytable
from concurrent.futures import ThreadPoolExecutor
import time
import getopt
import sys
import argparse
import sys

class PingTool:

    PING_CMD_SET = {
        'win32': 'ping {ip} -n {repeat} -w 200',
        'darwin': 'ping {ip} -c {repeat} -w 200',
        'linux': 'ping {ip} -c {repeat} -w 1'
    }
    PING_CMD = PING_CMD_SET[sys.platform]
    UNREACHABLE_STRING_SET = {
        'win32': '100% loss',
        'darwin': '100.0% packet loss',
        'linux': '100% packet loss'
    }
    UNREACHABLE_STRING = UNREACHABLE_STRING_SET[sys.platform]
    repeat = 1

    __field_names = ['IP', 'isReachable']
    __USAGE = """
PingTool is used to ping all host ip in a specified netwok, and can display a report

Usage: python ping.py [-n] [-r count] [-n net]

Options:
    -h,--help       Print usage
    -c              Count of ping requests to be sent
    -n              Network to test
    -s              return a subset of ip list. True is for reachable ip, false is for unreachable 
"""

    def __init__(self, netStr, repeat=1, state=True):
        ##self.parser_cli()
        #self.print_args()
        self.netStr = netStr
        self.repeat = repeat
        self.state = state
        self.pingCmd = self.PING_CMD.format(repeat=self.repeat, ip='{ip}')
        self.IPs = IP(self.netStr)[1:-1]
        self.__executor = ThreadPoolExecutor(256)
        self.__pt = prettytable.PrettyTable()
        self.__pt.field_names = self.__field_names

    #def parser_cli(self):
    #    if len(sys.argv) < 2:
    #        print(self.__USAGE)
    #        sys.exit(0)
    #    opts, args = getopt.getopt(sys.argv[1:],"n:c:s:h",["help"])
    #    for opt, arg in opts:
    #        if opt in ['-n']:
    #            self.netStr = arg
    #        elif "-c" == opt:
    #            self.repeat = arg
    #            self.pingCmd = self.PING_CMD.format(repeat=arg, ip='{ip}')
    #        elif "-s" == opt:
    #            if arg == 'true':
    #                self.state = True
    #            elif arg == 'false':
    #                self.state = False
    #            else:
    #                print(self.__USAGE)
    #                sys.exit(0)
    #        elif opt in ["--help", "-h"]:
    #            print(self.__USAGE)
    #            sys.exit(0)

    #def print_args(self):
    #    tmp = ''
    #    tmp += 'count: %s\t'%self.repeat
    #    tmp += 'network: %s\t'%self.netStr
    #    tmp += 'state: %s'%self.state
    #    print(tmp)
            
    #def getIPs(self):
    #    print(self.IPs.len())
    #    for ip in self.IPs:
    #        print(ip)

    def report(self, state='all'):
        print('Probe for {netStr}, total reachable: {reachableCount}'.format(netStr=self.netStr, reachableCount=len(self.result)))
        for r in self.result:
            self.__pt.add_row(r)
        print(self.__pt)

    def filter(self):
        if self.state:
            self.result = [r for r in self.result if r[-1]]
        return self

    def get_cached(self, netStr):
        return None

    def reachableIPs(self):
        cached = self.get_cached(self.netStr)
        if cached:
            return cached
        
        self.probe()
        return [str(r[0]) for r in self.result if r[-1]]

    def probe(self):
        self.result = []
        tmp_futures = []
        isFinish = False
        for ip in self.IPs:
            tmp_futures.append(self.__executor.submit(os.popen, self.pingCmd.format(ip=ip, repeat=self.repeat)))
        while (not isFinish):
            for f in tmp_futures:
                if not f.done():
                    break
            else:
                isFinish = True
            time.sleep(1)
        for idx, ip in enumerate(self.IPs):
            self.result.append(
                (
                    ip, 
                    False if self.UNREACHABLE_STRING in tmp_futures[idx].result().read() else True
                )
            )
        return self

if __name__ == "__main__":
    pt = PingTool('10.20.97.0/24')
    pt.probe().filter().report()
    pt = PingTool('192.25.97.0/24')
    pt.probe().filter().report()