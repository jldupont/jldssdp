'''
Created on Mar 7, 2015

@author: jldupont
'''
import json
import logging

from twisted.internet.protocol import DatagramProtocol


class SSDP(DatagramProtocol, object):
    """
    The SSDP protocol
    """
    ADDRESS = "239.255.255.250"
    PORT = 1900
    
    INTERESTING_TOKENS = ['location', 'server', 'nt', 'usn']
    
    NOTIFY_PACKET="""NOTIFY * HTTP/1.1\r
    Host: 239.255.255.250:1900\r
    Cache-Control: max-age=%(max_age)d\r
    Location: %(location)s\r
    Server: jldssdp UPnP/1.0\r
    NTS: ssdp:alive\r
    NT: %(nt)s\r
    USN: %(usn)s\r\n\r\n
    """
    
    def __init__(self, usn=None, nt=None, location=None, max_age=None, disable_receive=False):
        super(SSDP, self).__init__()
        
        self.usn = usn
        self.nt  = nt
        self.loc = location
        self.max_age = max_age
        
        self.disable_receive = disable_receive
    
    def startProtocol(self):
        """
        Called after protocol has started listening.
        """        
        # We don't want this to go very far
        self.transport.setTTL(1)
        
        # Join a specific multicast group:
        self.transport.joinGroup( self.ADDRESS )
        
    def sendNotify(self):
        """
        Sends a NOTIFY SSDP UDP packet
        """
        d = { "max_age": self.max_age, "nt": self.nt, "usn": self.usn, "location":self.loc }
        pkt = self.NOTIFY_PACKET % d
        self.transport.write(pkt, (self.ADDRESS, self.PORT))
        
            
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
        
        if self.disable_receive:
            return
        
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
                r[start_token] = tokens[1].strip()
                
        return r

