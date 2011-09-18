import random
import dbus, gobject
import time
from dbus.mainloop.glib import DBusGMainLoop

import lolwut

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
	return result.replace("&lt;", '<').replace("&gt;", '>')

class Data:
	def __init__(self):
		self.characters = {}
		self.words = {}

class MyPurpleInterface:
	def __init__(self):
		self.spam = 0
		self.data = {}
		self.counter = 0
	def received(self, account, receiver, message, conv, flags):
		message = unformat(message)
		print "[%s] -> [%s]: %s" % (account, receiver, message)
		conversation = purple.PurpleConvIm(conv)
		if message[-1]!=" ":
			print "1"
			if len(message)>1 and message[0]=="!":
				print "2"
				purple.PurpleConvImSend(conversation,lolwut.text(message[1:]))
			else:
				self.spam+=self.counter
				self.sent(account,receiver, " ")
	def sending(self, account, receiver, message):
		message = unformat(message)
		print "[%s] -> [%s]: %s" % (account, receiver, message)
		pieces = message.split(' ')
		conv = purple.PurpleFindConversationWithAccount(4, receiver, account)
		conversation = purple.PurpleConvIm(conv)
		if len(message)>1 and message[0]=="!":
			purple.PurpleConvImSend(conversation,lolwut.text(message[1:]))
		elif len(pieces)==3:
			if pieces[0]=="set":
				exec("self.%s = %s" % (pieces[1], pieces[2]) )
		elif len(pieces)==2:
			if pieces[0]=="go":
				try:
					n = int(pieces[1])
					self.spam+=n
					self.sent(account,receiver, " ")
				except:
					pass
	def sent(self, account, receiver, message):
		conv = purple.PurpleFindConversationWithAccount(4, receiver, account)
		conversation = purple.PurpleConvIm(conv)
		if message[-1]==" " and self.spam > 0:
			self.spam-=1
			purple.PurpleConvImSend(conversation, lolwut.sentence()+" ")

p = MyPurpleInterface()

bus.add_signal_receiver(p.received,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="ReceivedImMsg")

bus.add_signal_receiver(p.sending,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="SendingImMsg")

bus.add_signal_receiver(p.sent,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="SentImMsg")

loop = gobject.MainLoop()
loop.run()

#prpl-jabber
#prpl-gg
#prpl-icq
#prpl-irc
#prpl-msn
#prpl-aim