"""
    Created on 2012-01-20
    @author: jldupont
"""

from twisted.internet import epollreactor
epollreactor.install()

from protocol import SSDP

from twisted.internet import reactor
from twisted.internet.task import LoopingCall


def loop(proto):
    """
    The main loop
    """
    proto.sendNotify()
    


def run(usn=None, nt=None, loc=None, noloop=False, delay=30, eth0 = None):

    ##
    ## Substitute the eth0 IPv4 address
    ##
    loc = loc % {"eth0": eth0}

    proto = SSDP(usn=usn, nt=nt, location=loc, max_age=3600, disable_receive = True)

    ##
    ## Assigns a transport to the protocol instance
    ##    
    reactor.listenMulticast(SSDP.PORT, proto, listenMultiple=True)
    
    lc = LoopingCall(lambda:loop(proto))
    lc.start(delay, now=True)
    
    ##
    ## Because the LoopingCall is at least executed once,
    ##  we can safely exit here
    ##
    if not noloop:
        reactor.run()
