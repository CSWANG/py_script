#!/bin/env python
#-*- coding:  utf-8 -*-

import socket
import subprocess
import datetime
import os
import sys
import logging

def initLogging(logFilename):
    logging.basicConfig(
                    level    = logging.DEBUG,
                    format   = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt  = '%Y/%m/%d %H:%M:%S',
                    filename = logFilename,
                    filemode = 'a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def chkpath(_chk):
    i = len(_chk) -1
    if _chk[i] in '/':
        pass
    else:
        _chk = _chk + '/'

    return _chk

def check_server(address, port):
    s = socket.socket()
    print "Attempting to connect to %s on port %s" % (address, port)
    try:
        s.connect((address, port))
        print "Connected to %s on port %s" % (address, port)
        return True
    except socket.error, e:
        print "Connection to %s on port %s failed: %s" % (address, port, e)
        return False

def main():
    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("-a", "--address", dest="address", default="localhost", help="ADDRESS for server",
                      metavar="ADDRESS")

    parser.add_option("-p", "--port", dest="port", type="int", default=443, help="PORT for server", metavar="PORT")

    parser.add_option("-l", "--log", dest="log",  default='off', help="LOG all state", metavar="LOG")

    (options, args) = parser.parse_args()
    path = chkpath(os.path.realpath(os.path.dirname(sys.argv[0])))
    now = datetime.datetime.now().strftime("%m%d_%H%M_%S")

    filename = '%s%s_tracefile.log' % (path,now)

    logfile = '%sconnect.log' % (path)

    cmd = 'traceroute -d %s' % options.address

    if options.log == 'all':
        if check_server(options.address, options.port) == True:
            initLogging(logfile)
            logging.info('%s connected port:%s' % (options.address, options.port))
        else:
            initLogging(logfile)
            logging.debug('Responses fail %s port:%s' % (options.address, options.port))
            logfile = open(filename, "w")
            subprocess.call(cmd, shell=True, stdout=logfile)
            logfile.close()
    else:
        if check_server(options.address, options.port) == False:
            initLogging(logfile)
            logging.debug('Responses fail %s port:%s' % (options.address, options.port))
            logfile = open(filename, "w")
            subprocess.call(cmd, shell=True, stdout=logfile)
            logfile.close()


if __name__ == '__main__':
    main()
