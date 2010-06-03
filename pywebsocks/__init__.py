# coding: utf-8
# (c) 2009 Gleicon Moraes
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
import re


class BasicOperations(object):
    """ Basic tx websockets operations handler. Overwrite it with your operations """
    def __init__(self):
        self.writeHandler=None

    def on_read(self, sendLine):
        pass
    
    def on_connect(self):
        pass
    
    def on_close(self, r):
        pass

    def setWriteHandler(self, handler):
        self.writeHandler=handler
   
    def _out(self, str):
        if self.writeHandler == None:
            print 'No handler'
        else:
            self.writeHandler('\x00%s\xff' % str)

    def after_connection(self):
        pass

class WebSocketServer(LineReceiver):
    HDR_ORIGIN = re.compile('Origin\:\s+(.*)')
    HDR_LOCATION = re.compile('GET\s+(.*)\s+HTTP\/1.1', re.I)
    HDR_HOST = re.compile('Host\:\s+(.*)')
    HDR_KEY_1 = re.compile('Sec-WebSocket-Key1:(.*)')
    HDR_KEY_2 = re.compile('Sec-WebSocket-Key2:(.*)')
    def __init__(self):
        
        self.hdr = '''HTTP/1.1 101 Web Socket Protocol Handshake\r
Upgrade: WebSocket\r
Connection: Upgrade\r
Sec-WebSocket-Origin: %s\r
Sec-WebSocket-Location: ws://%s%s
Sec-WebSocket-Protocol: sample\r\n\r\n
Response'''

    def connectionMade(self):
        self.setRawMode()
        self.factory.oper.on_connect()
    
    def lineReceived(self, line):
        self.factory.oper.on_read(line)

    def rawDataReceived(self, line):
        origin, location, host, key1, key2 = self._parseHeaders(line)
        challenge = self._make_challenge_response(key1, key2, '')
        print self.hdr % (origin, host, location)
        print key1
        print key2
        self.sendLine(self.hdr % (origin, host, location))
        self.delimiter='\xff'
        self.setLineMode()
        self.factory.oper.setWriteHandler(self.sendLine)
        self.factory.oper.after_connection()

    def connectionLost(self, reason):
        self.factory.oper.on_close(reason)

    def _parseHeaders(self, buf):
        o=None
        l=None
        h=None
        k1=None
        k2=None
        for a in buf.split('\n\r'):
            print a
            org=self.HDR_ORIGIN.search(a)
            loc=self.HDR_LOCATION.search(a)
            hst=self.HDR_HOST.search(a)
            key1=self.HDR_KEY_1.search(a)
            key2=self.HDR_KEY_2.search(a)
            if org != None:
                o=org.group(1).strip()
            if hst != None:
                h=hst.group(1).strip()
            if loc != None:
                l=loc.group(1).strip()
            if key1 != None:
                k1=key1.group(1).strip()
            if key2 != None:
                k2=key2.group(1).strip()
        return o,l,h,k1,k2

    def _parse_keys(self, key1, key2):
        """ Parse the keys and return numbers and spaces """
        digits = [filter(lambda x: x.isdigit(), k)for k in [key1, key2]]
        digints = [int(d) for d in digits]
        spaces = [filter(lambda x: x == ' ', k)for k in [key1, key2]]
        space_count = [len(s) for s in spaces]
        divide_me = zip(digints, space_count)        
        return [d/s for d,s in divide_me]

    def _make_challenge_response(self, key1, key2, bytes):
        """
        Returns the challenge response
        Arguments:
        - `key1`:
        - `key2`:
        - `bytes`:
        """
        

        
    
class WebSocketFactory(Factory):
    protocol = WebSocketServer

    def __init__(self, oper=BasicOperations):
        self.oper=oper


