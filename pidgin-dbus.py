import random
import dbus, gobject
import time
from dbus.mainloop.glib import DBusGMainLoop

import textgen_parser as parser

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()

obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")

def unformat(string):
	ignore = 0
	result = ""
	for char in string:
		if   char == "<" :
			ignore = 1
		elif char == ">":
			ignore = 0
		elif not ignore:
			result+=char
	result = result.replace("&lt;", '<')
	result = result.replace("&gt;", '>')
	result = result.replace("&quot;", '"')
	result = result.replace("&apos;", "'")
	return result

class Data:
	def __init__(self):
		self.characters = {}
		self.words = {}

class MyPurpleInterface:
	def __init__(self):
		self.data = {}
		self.counter = ""
	def received(self, account, receiver, message, conv, flags):
		message = unformat(message)
		print "[%s] -> [%s]: %s" % (account, receiver, message)

		conversation = purple.PurpleConvIm(conv)
		if len(message)>1:
			if message[0]=="!":
				reply = parser.get_text(message[1:])
				purple.PurpleConvImSend(conversation, reply)
			elif self.counter != "" and message[-1]!=" ":
				variables = {}
				reply = parser.get_text(self.counter, message, variables)+" "
				purple.PurpleConvImSend(conversation, reply)
	def sending(self, account, receiver, message):
		message = unformat(message)
		print "[%s] -> [%s]: %s" % (account, receiver, message)

		conv = purple.PurpleFindConversationWithAccount(4, receiver, account)
		conversation = purple.PurpleConvIm(conv)

		if len(message)>1:
			if message[0]=="!":
				variables = {}
				reply = parser.get_text(message[1:], "", variables)
				purple.PurpleConvImSend(conversation, reply)
			elif len(message) >= 8:
				if message[:8] == "counter:":
					print "[INFO]counter set to: \"%s\""  % message[8:]
					self.counter = message[8:]

p = MyPurpleInterface()

bus.add_signal_receiver(p.received,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="ReceivedImMsg")

bus.add_signal_receiver(p.sending,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="SendingImMsg")

loop = gobject.MainLoop()
loop.run()

#prpl-jabber
#prpl-gg
#prpl-icq
#prpl-irc
#prpl-msn
#prpl-aim