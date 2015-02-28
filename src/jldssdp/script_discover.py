"""
    Created on 2012-01-20
    @author: jldupont
"""
import logging
import socket


from twisted.internet import epollreactor
epollreactor.install()

from twisted.internet.protocol import DatagramProtocol

from twisted.internet import reactor


class SSDP(DatagramProtocol):
    """
    The SSDP protocol
    """
    ADDRESS = "239.255.255.250"
    PORT = 1900
    
    def startProtocol(self):
        """
        Called after protocol has started listening.
        """
        # We don't want this to go very far
        self.transport.setTTL(1)
        
        # Join a specific multicast group:
        self.transport.joinGroup( self.ADDRESS )
        
            
    def datagramReceived(self, data, (host, port)):
        
        logging.info("Data:\n %s" % data)



def run(interface):
    """
    """

    reactor.listenMulticast(SSDP.PORT 
                            ,SSDP()
                            ,listenMultiple=True)
       
    reactor.run()
