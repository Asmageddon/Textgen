import sys
import threading
import socket

import re
from random import randint, choice
from time import sleep

import textgen_parser as parser
from lolwut import sentence

comment_rate = 0.01
reply_rate = 1.0

def dmsg(text, person = None):
	if person == None:
		print "[STATUS] %s" % text
	else:
		print "[%s] %s" % (person, text)

def wrand(dictionary):
	s = sum(dictionary.values())
	i = randint(0, s)
	n=-1
	while i > dictionary.values()[n]:
		i -= dictionary.values()[n]
		n -=1
	return dictionary.keys()[n]

def split_data(data):
	result = [ "" ]
	mode = 0
	for char in data:
		if mode >= 3:
			result[-1] += char
		else:
			if char == " ":
				mode += 1
				result += [""]
			else:
				result[-1] += char
	return result

def split_words(text):
	result = [""]
	for char in text:
		if char in word_chars:
			result[-1] += char
		else:
			result += ""
	return result

def get_nick(full_id):
	on = 0
	nick = ""
	for char in full_id:
		if   char == ':': on=1
		elif char == '!': on = 0; break
		else:
			nick += char
	return nick.lower()

word_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_@"

class ManagerClass:
	def __init__(self, server, port=6667):
		self.storage = None
		self.server = server
		self.port = port
		self.threads = []
		self.family = 0
		self.salt = randint(0,99999999)
	def spawn(self, channel="#anime", name=None, bot_type="worker"):
		if name == None:
			name = parser.parse("$C$v$Anything").to_string().replace(" ", "-")
		if len(name) > 16: name = name[:16]
		dmsg( "Spawning %s into %s" % (name, channel) )
		if bot_type == "worker":
			bot = WorkerClass(self.server, self.port, channel, name)
		else:
			bot = None
		self.threads += [ bot ]
		self.family += 1
		self.threads[-1].parent = self
		self.threads[-1].storage = self.storage
		self.threads[-1].start()
	def terminate(self):
		print "Terminating"
		for t in self.threads:
			try:
				t.terminate()
			except:
				pass

class BotClass(threading.Thread):
	def __init__(self, server, port, channel, name):
		threading.Thread.__init__(self)
		self.parent = None
		self.server = server
		self.port = port
		self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.channel = channel
		self.name = name

	def run(self):
		dmsg('Attempting to connect...' , self.name)
		try:
			self.sock.connect( (self.server, self.port) )
			dmsg('Connected to %s!' % (self.server) , self.name )
			self.connected = True
		except:
			dmsg('Failed to connect: %s' % (sys.exc_info()) , self.name)
			self.connected = False
		if self.connected:
			self.sock.send('NICK %s\r\n' % self.name)
			self.sock.send('USER Bot%s AnAnonBot AnAnonBot :Derp IRC\r\n' %self.name)
			self.sock.send('JOIN %s\r\n' % self.channel)
			self.sock.send('PRIVMSG %s :Hello.\r\n' % self.channel)
		act = 0
		while self.connected:
			data = self.sock.recv(4096)
			act = 0

			if data == '':
				self.connected = False
			else:
				dmsg("(received)%s\\r\\n" % data[:-2], self.name)
				sdata = split_data(data)
				if   sdata[0] == "PING":
					self.ping(data)
				elif sdata[1] == "PRIVMSG":
					if sdata[0][1:1+len(self.name)] == self.name:
						self.sending(sdata[0], sdata[2], sdata[3][1:-2])
					else:
						self.receive(sdata[0], sdata[2], sdata[3][1:-2])
					if self.name.lower() in sdata[3].lower():
						self.mention(sdata[0], sdata[2], sdata[3][1:-2])
				elif sdata[1] == "NICK":
					self.on_nick_change(get_nick(sdata[0]), sdata[2][1:-2])
				elif sdata[1] == "PART":
					self.on_part(get_nick(sdata[0]), sdata[2][:-2])
				elif sdata[1] == "JOIN":
					self.on_join(get_nick(sdata[0]), sdata[2][1:-2])

		dmsg('Exiting.' , self.name)
		if self.parent != None:
			self.parent.family -= 1
		self.sock.close()
	def ping(self, data):
		self.sock.send("PONG :%s" % self.name)
		dmsg("Sent PONG to %s" % self.channel , self.name)
	def sending(self, sender, channel, message): pass
	def receive(self, sender, channel, message): pass
	def mention(self, sender, channel, message): pass
	def send(self, message, channel = None):
		dmsg("Sending: \"%s\" to %s" % (message, channel), self.name)
		if channel == None:
			channel = self.channel
		elif channel[0] != "#":
			channel = "#" + channel
		self.sock.send('PRIVMSG %s :%s\r\n' % (channel, message))
	def terminate(self): self.connected = False
	def on_part(self, person, channel): pass
	def on_join(self, person, channel): pass
	def on_nick_change(self, prev, new): pass

class WorkerClass(BotClass):
	def __init__(self, server, port, channel, name):
		BotClass.__init__(self, server, port, channel, name)
		self.privileges = {
			"asmageddon": (3, {} ),
		}
		self.remind = {
			"Asmageddon":[("Asmageddon", "")]
		}
		self.ignore = []
		self.follow = []
	def receive(self, sender, channel, message):
		spaces = 0
		current = 0
		p = re.compile("~")
		split_message = re.split(p, message)
		if len(split_message) >= 2:
			suffix = message[-1]
			rest = message[:-1]
			self.command(sender, channel, rest, suffix)
	def mention(self, sender, channel, message):
		if "bot" in sender.lower(): return None
		p = re.compile("^%s[\-,:]\s*" % self.name)
		if p.match(message):
			self.command(sender, channel, p.sub("", message), "")
		else:
			self.command(sender, channel, message, "")
	def allow(self, command, person):
		allow = 0
		for i in range(0, len(orders_allowed)):
			if command in orders_allowed[i]:
				if person in self.privileges:
					if command in self.privileges[person][1]:
						allow = self.privileges[person][1][command]
					elif self.privileges[person][0] >= i:
						allow = 1
				else: allow = 0
				break
			else:
				allow = -1
		return allow
	def command(self, sender, channel, order, suffix):
		if len(order) <= 2: return
		if sender in self.ignore: return
		print dmsg("%s, %s" % (order, suffix), self.name)
		commander = get_nick(sender)

		p = command_parser(order, commander)

		print p.get()
		allow = self.allow(p.get(), commander)
		if   allow ==  0: self.send("Nope"); return
		elif allow == -1: self.send("%s: Unrecognized command" % commander); return

		if  p.accept("say", 1):
			self.send(parser.parse(p.get_rest()).to_string())
		elif p.accept("remind", 1):
			username = p.get()
			p.accept("", 1)
			p.accept("about", 1)
			p.accept("to", 1)
			text = p.get_rest()
			if username not in self.remind: self.remind[username] = []
			self.remind[username] += [ (commander, text) ]
			self.send("Ok, will remind %s: '%s'" % (username, text))
		elif p.accept("ignore", 1):
			#ignore = "ignore", username, { delimiter , username }
			users = []
			users += [p.get()]
			p.accept("", 1)
			while p.accept("and", 1):
				users += [p.get()]
				p.accept("", 1)
			if len(users) <= 0: return
			userlist_readable = users[0]
			del users[0]
			for user in users:
				userlist_readable += ", %s" % user
			for user in users:
				if user not in self.ignore: self.ignore += [user]
			self.send("Understood, will now ignore %s" % userlist_readable)
		elif p.accept("follow", 1):
			#follow = "follow", username, { delimiter , username }
			users = [ p.get() ]
			while p.accept("and", 1):
				users += [p.get()]
				p.accept("", 1)
			if len(users) <= 0: return
			userlist_readable = users[0]
			del users[0]
			for user in users:
				if user not in self.follow: self.follow += [user]
			for user in users:
				userlist_readable += ", %s" % user
			self.send("Understood, will now follow %s" % userlist_readable)
		elif p.accept("leave", 1):
			self.leave(channel)
		elif p.accept("spawn", 1):
			if p.accept(""):
				self.parent.spawn(channel, p.get())
			else:
				self.parent.spawn(channel)
		elif p.accept("silence", 1):
			if   p.accept("no"):
				self.silence = 0
			elif p.accept("yes"):
				self.silence = 1
			else:
				self.silence = 1
		elif p.accept("log", 1):
			self.send("Unimplemented")
	def leave(self, channel):
		self.connected = 0
	def on_join(self, person, channel):
		if person.lower() in self.remind:
			for memo in self.remind[person]:
				message = "%s: Message from %s: '%s'" % (person, memo[0], memo[1])
				self.send(message, channel)
			del self.remind[person]

class command_parser(object):
	def __init__(self, order, commander):
		self.order = order

		x = order.lower().strip()
		pattern = re.compile("[.,\-!?\ ]+")
		x = pattern.sub(" ", x)
		for command in aliases:
			pattern2 = "("
			for alias in aliases[command][:-1]:
				pattern2 += alias
			pattern2 += aliases[command][-1].replace(" ", "\\ ")+")"
			x = re.compile(pattern2).sub(command , x)

		x.replace("me", commander)
		self.sorder = x.split(" ")

		self.current_part = 0
	def get(self):
		result = ""
		if len(self.sorder) <= self.current_part : return ""
		else:
			return self.sorder[self.current_part]
	def get_rest(self):
		i = 0
		lchars = 0
		char_num = 0
		for char in self.order:
			char_num += 1
			if char in ".,-!? ":
				if lchars == 0:
					lchars = 1
					i += 1
			else: lchars = 0
			if i >= self.current_part: break
		return self.order[char_num:]
	def accept(self, string = "", consume = 0):
		result = 0
		if string == "":
			if self.get() != "": result = 1
			else: result = 0
		elif self.get() == string: result = 1
		else: result = 0
		if result & consume: self.current_part += 1
		return result

aliases = {
	"say":["say", "speak" , "talk", "spam", "chatter", "converse"],
	"remind":["tell", "relay", "notify", "remind", "relay to"],
	"ignore":["forget", "ignore", "pay no attention to"],
	"follow":["follow", "spy", "stalk", "go after"],
	"leave":["leave", "die", "go away", "leave us"],
	"spawn":["spawn", "create", "raise"],
	"silence":["silence", "stfu", "quiet"],
	"log":["record", "log"],

	"yes":[ "on", "yes", "true", "enable", "enabled", "negative", "1" ],
	"no":[ "off", "no", "false", "disable", "disabled", "positive", "0" ],
	"all":[ "\*", "all", "everything", "everyone"],
	"but":["but", "except", "aside from", "but not"],
	"and":["and", ",", "as well as"]
}

orders_allowed =[ #Sorted by level
	[ "say" , "remind" ], #Level 0 - anyone
	[ "silence" ], #Level 1 - some privileges required
	[ "leave" , "spawn" , "ignore", "log"], #level 2 - advanced privileges required
	[ "follow" ] #level 3 - MASTER POWAH
]

#text
#nick
#delimiter = ( "," | " " | "and" )
#say = "say", ["to", nick], text
#remind = "remind", [username, ["about" | "to"]], text, ["in", time]
#ignore = "ignore", username, { delimiter , username }
#follow = "follow", username, { delimiter , username }
#leave = "leave", [ "here" | channel ]
#spawn = "spawn", [name], ["in", channel]
#silence = "silence", [on | off]
#log = "log", ( ["all", "but", username, { delimiter , username }] | [username, { delimiter , username }]), ["into", logfile]

if __name__ == "__main__":
	dmsg("Starting up")
	man = ManagerClass("irc.freenode.org", 6667)
	man.spawn("#anime")
	##man.spawn("#asmabottest")
	#man.spawn("#anime", "Cherry")
	#man.spawn("#anime", "Lime")
	#man.spawn("#anime", "Bloodberry")
	raw_input()
	man.terminate()