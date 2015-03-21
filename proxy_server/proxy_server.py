from twisted.internet.defer import Deferred, maybeDeferred, succeed
from twisted.internet.protocol import ClientFactory, ServerFactory, Protocol
import optparse

class ProxyServerProtocol(Protocol):

    def connectionMade(self):
        d = self.factory.service.get_poem()
        d.addCallback(self.transport.write)
        d.addBoth(lambda r: self.transport.loseConnection())

class ProxyServerFactory(ServerFactory):
    protocol = ProxyServerProtocol

    def __init__(self, service):
        self.service = service

class ProxyService(object):
    poem = None

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_poem(self):
        if self.poem:
            print 'cache hitted'
            return succeed(self.poem)

        factory = ProxyClientFactory()
        factory.deferred.addCallback(self.set_poem)
        from twisted.internet import reactor
        reactor.connectTCP(self.host, self.port, factory)
        return factory.deferred

    def set_poem(self, poem):
        self.poem = poem
        return self.poem

class ProxyCientProtocol(Protocol):
    poem = ''

    def dataReceived(self, data):
        self.poem += data

    def connectionLost(self, reason):
        self.factory.poem_finished(self.poem)

class ProxyClientFactory(ClientFactory):
    protocol = ProxyCientProtocol

    def __init__(self):
        print 'new proxy client factory'
        self.deferred = Deferred()

    def clientConnectionFaild(self, reason):
        if self.deferred:
            d, self.deferred = self.deferred, None
            d.errback(reason)

    def poem_finished(self, poem):
        if self.deferred:
            d, self.deferred = self.deferred, None
            d.callback(poem)

def main(options):
    service = ProxyService(options.caddr, options.cport)
    server_factory = ProxyServerFactory(service)
    from twisted.internet import reactor
    reactor.listenTCP(options.sport, server_factory, interface=options.saddr)
    reactor.run()

if __name__ == '__main__':
    parser = optparse.OptionParser('')
    parser.add_option('--caddr', help=help, default='localhost')
    parser.add_option('--cport', help=help, type=int)
    parser.add_option('--saddr', help=help, default='localhost')
    parser.add_option('--sport', help=help, type=int)

    options, args = parser.parse_args()
    main(options)

