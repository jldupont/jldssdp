"""
    Created on 2012-01-20
    @author: jldupont
"""
import logging
import json


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
    
    INTERESTING_TOKENS = ['location', 'server', 'nt', 'usn']
    
    
    def startProtocol(self):
        """
        Called after protocol has started listening.
        """        
        # We don't want this to go very far
        self.transport.setTTL(1)
        
        # Join a specific multicast group:
        self.transport.joinGroup( self.ADDRESS )
        
            
    def datagramReceived(self, data, (host, port)):
        """
        Example:
        
        NOTIFY * HTTP/1.1
        Host: 239.255.255.250:1900
        Cache-Control: max-age=60
        Location: http://192.168.1.1:1780/InternetGatewayDevice.xml
        NTS: ssdp:alive
        Server: POSIX, UPnP/1.0 linux/5.10.56.51
        NT: urn:schemas-upnp-org:device:LANDevice:1
        USN: uuid:DF6DC556-C32F-8E72-45EB-B7CDDA382DB9::urn:schemas-upnp-org:device:LANDevice:1
        """
        try:

            lines = data.split("\n")
            lines = map(lambda line:line.strip(), lines)
            lines = filter(lambda line:len(line)>0, lines)
    
            if not self.is_notify(lines):
                return
            
            entry = self.keep_interesting_tokens(lines)
            
            print json.dumps( entry )

        except:
            logging.error("Data: %s" % repr(data))
        

    def is_notify(self, lines):
        
        first_line = lines[0]
        first_line_token = first_line.split(" ")
        first_token = first_line_token[0].lower()
        
        return first_token == "notify"


    def keep_interesting_tokens(self, lines):
        
        r = {}
        
        for line in lines:
            tokens = line.split(":", 1)
            start_token = tokens[0].lower()
            
            if start_token in self.INTERESTING_TOKENS:
                r[start_token] = tokens[1]
                
        return r



def run(*p, **k):
    
    reactor.listenMulticast(SSDP.PORT 
                            ,SSDP()
                            ,listenMultiple=True)
    reactor.run()
