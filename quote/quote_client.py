from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor

class QuoteProtocol(Protocol):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.transport.write(self.factory.quote)

    def dataReceived(self, data):
        print "Received data : %s" % (data,)
        self.transport.loseConnection()

class QuoteFactory(ClientFactory):

    def __init__(self, quote):
        self.quote = quote

    def buildProtocol(self, addr):
        return QuoteProtocol(self)

    def clientConnectionFailed(self, connector, reason):
        maybeStopConnector()

    def clientConnectionLost(self, connector, reason):
        maybeStopConnector()

def maybeStopConnector():
    global quote_counter
    quote_counter -= 1
    if not quote_counter:
        reactor.stop()

quotes = [
    'Carpe diem',
    'You snooze and lose',
    'The early bird gets the worm'
]

quote_counter = len(quotes)

for quote in quotes:
    reactor.connectTCP('localhost', 8000, QuoteFactory(quote))

reactor.run()
