from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

class Echo(Protocol):

    def dataReceived(self, data):
        print data
        self.transport.write(data)

class Quote(Protocol):

    def connectionMade(self):
        self.transport.write("An apple a day keeps doctor away\n")
        self.transport.loseConnection()


class CountedEcho(Protocol):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.numProtocols = self.factory.numProtocols + 1
        self.transport.write("Welecome! There are now %d protocols connected"
                             % self.factory.numProtocols)


    def connectionLost(self, reason):
        self.factory.numProtocols = self.factory.numProtocols - 1

    def dataReceived(self, data):
        self.transport.write(data)

class QOTFactory(Factory):
    numProtocols = 0

    def buildProtocol(self, addr):
        return CountedEcho(self)


endpoint = TCP4ServerEndpoint(reactor, 8007)
endpoint.listen(QOTFactory())
reactor.run()

