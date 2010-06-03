#!/usr/bin/env python

import unittest
from pywebsocks import WebSocketServer

class MyTest(unittest.TestCase):

    def testParseKeys(self):
        "Make sure we can parse the keys"
        ws = WebSocketServer()
        parsed = ws._parse_keys('18x 6]8vM;54 *(5:  {   U1]8  z [  8',
                                '1_ tx7X d  <  nw  334J702) 7]o}` 0')
        self.assertEquals(parsed, [155712099, 173347027])

    


if __name__ == '__main__':
    unittest.main()
