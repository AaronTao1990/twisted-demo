from twisted.internet.protocol import Protocol, ServerFactory

class SimpleProtocol(Protocol):

    def connectionMade(self):
        print 'new connection'
        self.transport.write(self.factory.quote)
        self.transport.loseConnection()

class SimpleServerFactory(ServerFactory):

    protocol = SimpleProtocol

    def __init__(self, quote):
        self.quote = quote

def main():
    from twisted.internet import reactor
    quote = 'an apple a day keeps doctor away\n'
    factory = SimpleServerFactory(quote)
    reactor.listenTCP(8000, factory, interface='localhost')
    reactor.run()

if __name__ == '__main__':
    main()
