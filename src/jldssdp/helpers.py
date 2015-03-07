'''
    Created on Mar 7, 2015
    @author: jldupont
'''
import netifaces as ni

def get_eth0_ipv4():
    """
    Extracts the IPv4 address associated with eth0 interface
    """
    
    eth0 = ni.ifaddresses('eth0')[ni.AF_INET][0]
    return eth0['addr']
