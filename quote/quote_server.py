from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

class QuoteProtocol(Protocol):

    def dataReceived(self, data):
        print '%d connections connected for now' % (self.factory.numConnections, )
        print '> received : %s> response : %s' % (data, self.getQuote())
        self.transport.write(self.getQuote())
        self.updateQuote(data)

    def connectionMade(self):
        self.factory.numConnections += 1

    def connectionLost(self, reason):
        self.factory.numConnections -= 1

    def getQuote(self):
        return self.factory.quote

    def updateQuote(self, quote):
        self.factory.quote = quote


class QuoteFactory(Factory):
    numConnections = 0
    protocol = QuoteProtocol

    def __init__(self, quote=None):
        self.quote = quote or "An apple a day keeps doctor away"

reactor.listenTCP(8000, QuoteFactory())
reactor.run()
