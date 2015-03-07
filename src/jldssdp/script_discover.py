"""
    Created on 2012-01-20
    @author: jldupont
"""

from twisted.internet import epollreactor
epollreactor.install()

from protocol import SSDP

from twisted.internet import reactor


def run(*p, **k):
    
    reactor.listenMulticast(SSDP.PORT 
                            ,SSDP()
                            ,listenMultiple=True)
    reactor.run()
