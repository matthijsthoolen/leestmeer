from __future__ import print_function
from os import environ
import datetime

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    An application component that publishes an event every five seconds.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        def utcnow():
            now = datetime.datetime.utcnow()
            return now.strftime("%Y-%m-%dT%H:%M:%SZ")

        try:
            yield self.register(utcnow, 'com.analyze.async')
        except Exception as e:
            print("failed to register procedure: {}".format(e))
        else:
            print("procedure registered")


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("readability", "ws://localhost:8080/ws"),
        u"analyze",
        debug_wamp=False,  # optional; log many WAMP details
        debug=False,  # optional; log even more details
    )
    runner.run(Component)