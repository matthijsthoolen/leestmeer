# -*- coding: utf-8 -*-

from __future__ import print_function
from os import environ
import datetime

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

import jsonpickle

import AVIscoreMod

class Component(ApplicationSession):
	"""
    An application component that publishes an event every five seconds.
    """

	@inlineCallbacks
	def onJoin(self, details):
		print("session attached")

		def analyze(message):
			#print(message)
			#print()
			
			# Parse JSON into an object with attributes corresponding to dict keys.
			#x = json.loads(message, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
			
			x = jsonpickle.decode(message)
		
			print(x['text'][0]['paragraph'])
			
			#print(json.dumps(x))
			
			answer = AVIscoreMod.main(x,'avi','object')
			print(answer.overall[0].aviscore)
			
			encode = jsonpickle.encode(answer)
			
			return encode

		try:
			yield self.register(analyze, 'com.analyze.async')
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