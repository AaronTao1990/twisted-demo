from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

class SimpleMessage(Protocol):

    def sendMessage(self, msg):
        self.tranport.write("MESSAGE : %s\n", msg)

def gotProtocol(p):
    p.sendMessage("Hello")
    reactor.callLater(1, p.sendMessage, "this is another message")
    reactor.callLater(2, p.tranport.loseConnection)

point = TCP4ClientEndpoint(reactor, "localhost", 8007)
d = connectProtocol(point, SimpleMessage())
d.addCallback(gotProtocol)

reactor.run()
