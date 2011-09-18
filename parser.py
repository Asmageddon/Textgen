import os, random, string

#Remove this later: (or not)
words = eval(open(os.path.join("data", "words")).read())

class node(object):
	def get(self): return self
	def to_string(self): return ""
	def structure(self, indent): pass
	def optimize(self): pass

class nothing(node):
	def get(self): return self
	def to_string(self):
		return ""
	def structure(self, indent):
		r = ""
		for i in range(indent):
			r+='  '
		print r+"-"

class text(node): #Format: "Word"
	def __init__(self,content=""):
		self.value=content
	def get(self):
		return self
	def to_string(self):
		return self.value
	def structure(self,indent):
		r = ""
		for i in range(indent):
			r+='  '
		print '%s[text]: "%s"' % (r, self.value)

def starts_with(text, chars):
	if len(text)>0:
		return text[0] in chars
	return 0

def randword_builtin(value):
	if value == "anything":
		return '$'+random.choice(words.keys())

class randword(node): #Format: "$word" #This is also anything :3
	def __init__(self, value):
		self.value = value
	def get_mode(self, value):
		if value[0] not in string.uppercase:
			mode = 0
		else:
			if len( value ) > 1:
				if value[1] not in string.uppercase: mode = 1
				else: mode = 2
			else:
				mode = 2
		return mode
	def format(self, result, mode):
		if   mode == mode_lower:
			return text(result)
		elif mode == mode_capital:
			return text(result.capitalize())
		elif mode == mode_upper:
			return text(result.upper())
	def get(self):
		result = "$" + self.value.lower()
		mode = self.get_mode(self.value)
		done = 0
		while not done:
			if len(result) == 0:
				done = 1
			else:
				key = result[1:].lower()
				if   key in randword_reserved:
					result = randword_builtin(key)
				elif result[0] == "$":
					if key in words:
						result = random.choice(words[key])
					else:
						done = 1
				elif result[0] == "!":
					result = parse(key).to_string()
				else:
					done = 1
		return self.format(result, mode)
	def to_string(self):
		return self.get().to_string()
	def structure(self,indent):
		r = ""
		for i in range(indent):
			r+='  '
		print r + '[randword]: "%s"' % self.value

class sequence(node): #Format: "Dunno"
	def __init__(self):
		self.data = [[]]
	def get(self):
		return self
	def get_option(self, index):
		result = sequence()
		result.data = [self.data[index]]
		return result
	def to_string(self, index = None):
		result=""
		if index == None:
			for i in random.choice(self.data):
				result+=i.to_string()
		else:
			for i in self.data[index]:
				result+=i.to_string()
		return result
	def add(self, item):
		if item:
			self.data[-1]+=[item]
	def add_option(self):
		self.data+=[[]]
	def structure(self,indent):
		r = ""
		for i in range(indent):
			r+='  '
		print r+"[sequence]:"
		if len(self.data) == 1:
			for j in range(len(self.data[0])):
				self.data[0][j].structure(indent+1)
		else:
			for i in range(len(self.data)):
				print r + "  option %i:" % i
				for j in range(len(self.data[i])):
					self.data[i][j].structure(indent+2)
	def optimize(self):
		za_string = ""
		for o in range(0, len(self.data)):
			za_string = ""
			new_sequence = []
			for element in self.data[o]:
				element.optimize()
			for element in self.data[o][:]:
				if element.__class__ == type(text()):
					za_string+=element.to_string()
				else:
					if za_string!="":
						new_sequence += [ text(za_string) ]
						za_string = ""
					new_sequence += [element]
			if za_string!="":
				new_sequence += [ text(za_string) ]
				za_string = ""
			self.data[o] = new_sequence[:]

class repeat(node):
	def __init__(self, item, min_times, max_times):
		self.item = item
		self.min = min_times
		self.max = max_times
	def get(self):
		return self
	def to_string(self):
		result = ""
		for i in range(0, random.randint(self.min, self.max)):
			result+=self.item.to_string()
		return result
	def structure(self,indent):
		r = ""
		for i in range(indent):
			r+='  '
		print r+"[repeat]:"
		print r+"  times"
		print r+"    min: %i" %self.min
		print r+"    max: %i" %self.max
		print r+"  value:"
		self.item.structure(indent+2)
	def optimize(self):
		self.item.optimize()

class modifier(node):
	def __init__(self):
		self.parameters = []
		self.value = nothing()
		self.name = "blank modifier"
	def modify(self, string):
		return string
	def get(self):
		return self.value
	def to_string(self):
		return self.modify(self.get().to_string())
	def structure(self, indent):
		r = ""
		for i in range(indent):
			r+='  '
		print r+"[modifier]"
		print r+"  type: %s" % self.name
		for i in range(len(self.parameters)):
			print "%s  parameter %s: %s" % (r, i, self.parameters[i])
		print r+"  Value:"
		self.value.structure(indent+2)
	def optimize(self):
		self.value.optimize()
	def split_words(self, value):
		result = []
		current = ""
		for char in value:
			if (char in string.lowercase) or (char in string.uppercase):
				current+=char
			else:
				result+=[current]+[char]
				current = ""
		return result
	def get_parameter(self, index, integer = 0):
		if len(self.parameters) > index:
			result = self.parameters[index]
			if integer:
				try:
					result = int(result)
				except:
					result = 0
			return result
		else:
			if integer: return 0
			else: return ""
class modifier_factory(modifier):
	def __init__(self, string, value):
		self.value = value #Should always be a sequence() object

		t = type(node())
		pieces = string.split(' ')
		mod_type = pieces[0].lower()

		if len(pieces) > 1: self.parameters = pieces[1:]
		else:               self.parameters = []

		self.name = mod_type
		if   mod_type == "jumble":    t = type(modifier_jumble())
		elif mod_type == "flip":      t = type(modifier_flip())
		elif mod_type == "reverse":   t = type(modifier_reverse())
		elif mod_type == "acronym":   t = type(modifier_acronym())
		elif mod_type == "randcase":  t = type(modifier_randcase())
		elif mod_type == "upper":     t = type(modifier_uppercase())
		elif mod_type == "lower":     t = type(modifier_lowercase())
		elif mod_type == "mix":       t = type(modifier_mix())
		elif mod_type == "alternate": t = type(modifier_alternate())
		elif mod_type == "word":      t = type(modifier_word())
		elif mod_type == "allbut":    t = type(modifier_allbut())
		elif mod_type == "replace":   t = type(modifier_replace())
		self.__class__ = t

class modifier_jumble(modifier):
	def modify(self, value):
		result = ""
		current = ""
		for char in value+" ":
			if (char in string.lowercase) or (char in string.uppercase):
				current+=char
			else:
				if len(current)<4:
					result+= current
					current = ""
				else:
					start = current[0   ]
					end   = current[  -1]
					middle= current[1:-1]
					current = ""
					new_middle = ""
					while len(middle) > 0:
						index = random.randint(0,len(middle)-1)
						new_middle+= middle[index]
						middle = middle[:index]+middle[index+1:]
					result+=start + new_middle + end
				result+=char
		return result
class modifier_flip(modifier):
	def modify(self, value):
		result = ""
		for i in range(1,len(value)+1):
			result+=value[-i]
		return result
class modifier_reverse(modifier):
	def modify(self, value):
		current = ""
		result = self.split_words(value)#[]
		result_reversed = ""
		#for char in value:
			#if (char in string.lowercase) or (char in string.uppercase):
				#current+=char
			#else:
				#result+=[current]+[char]
				#current = ""
		for i in range(1,len(result)+1):
			result_reversed+=result[-i]
		return result_reversed
class modifier_acronym(modifier):
	def modify(self, value):
		result = ""
		for piece in self.split_words(value):
			if (piece[0] in string.lowercase) or (piece[0] in string.uppercase):
				result+=piece[0]
		return result
class modifier_randcase(modifier):
	def modify(self, value):
		result = ""
		for char in value:
			if random.randint(0,1): result+= char.upper()
			else: result+= char.lower()
		return result
class modifier_uppercase(modifier):
	def modify(self, value):
		return value.upper()
class modifier_lowercase(modifier):
	def modify(self, value):
		return value.lower()
class modifier_mix(modifier):
	def modify(self, value):
		pieces = self.split_words(value)
		pieces1=[]
		pieces2=[]
		for i in range(0,len(pieces)):
			if i%2: pieces1+=[pieces[i]]
			else:   pieces2+=[pieces[i]]
		new_pieces = []
		while len(pieces2) > 0:
			index = random.randint(0,len(pieces2)-1)
			new_pieces+=[pieces2[index]]
			del pieces2[index]
		result = ""
		for i in range(0,len(new_pieces)):
			result+=new_pieces[i]+pieces1[i]
		if len(pieces1) > len(new_pieces):
			result += pieces1[-1]
		return result
class modifier_alternate(modifier):
	def to_string(self):
		if   self.value.__class__ != type(sequence()): return self.value.to_string()
		elif len(self.value.data) < 2: return self.value.to_string()

		if not hasattr(self, "direction"):
			self.direction = self.get_parameter(0,1)
		if not hasattr(self, "position"):
			self.position = self.get_parameter(1,1)

		if self.position > len(self.value.data)-1:
			self.position = 0
		if self.position < 0:
			self.position = len(self.value.data)-1

		result = self.value.to_string(self.position)
		if self.direction:
			self.position -= 1
		else:
			self.position += 1
		return result
class modifier_word(modifier):
	def modify(self, value):
		result = ""
		index = []
		pieces = self.split_words(value)
		for param in self.parameters:
			try:
				c = int(param)-1
				index += [c]
			except: pass
		for i in index:
			if i > len(pieces)//2 or i < 0: continue
			else:
				result += pieces[i*2] + pieces[i*2+1]
		return result
class modifier_allbut(modifier):
	def modify(self, value):
		result = ""
		index = []
		pieces = self.split_words(value)
		for param in self.parameters:
			try:
				c = int(param)-1
				index += [c]
			except: pass
		for i in range(0, len(pieces)//2):
			if i in index: continue
			result += pieces[i*2] + pieces[i*2+1]
		return result
class modifier_replace(modifier):
	def modify(self, value):
		result = str(value)
		for i in range(0, len(self.parameters)//2):
			result = result.replace(self.get_parameter(i*2),self.get_parameter(i*2+1))
		return result

class chance(node):
	def __init__(self, object, chance):
		self.object = object
		self.chance = chance
	def get(self):
		if random.random() < self.chance: return self.object
		else: return nothing()
	def to_string(self):
		return self.get().to_string()
	def structure(self,indent):
		r = ""
		for i in range(indent):
			r+='  '
		print r+"[chance]:"
		print r+"  chance: %f" % self.chance
		print r+"  value:"
		self.object.structure(indent+2)
	def optimize(self):
		self.object.optimize()

def tokenize(string):
	result = []
	current=""
	l_string = 0
	prev_char = ''
	a=0
	for char in string:
		if char in token_characters and prev_char!='\\':
			l_string = 0
			if   char == '$':
				result += [t_dollar]
			elif char == '[':
				result += [t_scope_open]
			elif char == ']':
				result += [t_scope_close]
			elif char == '(':
				result += [t_func_open]
			elif char == ')':
				result += [t_func_close]
			elif char == '-':
				result += [t_range]
			elif char == '|':
				result += [t_or]
			elif char == '{':
				result += [t_curly_open]
			elif char == '}':
				result += [t_curly_close]
			elif char == '%':
				result += [t_percent]
			elif char == '<':
				result += [t_mod_open]
			elif char == '>':
				result += [t_mod_close]
		else:
			if prev_char=='\\':
				if   char == 'n': char = '\n'
				elif char == 't': char = '\t'
			if l_string:
				if len(result[-1])>0:
					if result[-1][-1] not in word_separation:
						if char in word_separation: result+=[char]
						else: result[-1]+=char
					else:
						result[-1]+=char
				else:
					result[-1]+=char
			else: result+=[char]
			l_string = 1
		prev_char = char
	return result

class parser:
	def __init__(self):
		self.tokens=[]
		self.last_token=None
		self.result=None
	def accept(self, token):
		if len(self.tokens)==0: return 0
		if   token==t_text:
			if self.tokens[0].__class__ in [type(""),type(u"")]:
				return 1
		elif self.tokens[0] == token:
			return 1
		return 0
	def eat(self, token=None):
		if len(self.tokens)==0: return 0
		if token==None:
			del self.tokens[0]
			return 0
		result = self.accept(token)
		if result:
			del self.tokens[0]
		return result
	def parse(self, string):
		self.tokens = tokenize(string)
		self.result = self.root()
		self.result.optimize()
		return self.result

	def root(self):
		result = sequence()
		while len(self.tokens) > 0:
			if self.accept(t_text):
				result.add ( self.text() )
			elif self.accept(t_dollar) or self.accept(t_scope_open):
				result.add ( self.chance() )
			else:
				result.add ( self.text_token() )
		return result
	def sequence(self):
		result = sequence()
		while len(self.tokens) > 0 and not self.accept(t_scope_close):
			if self.accept(t_text):
				result.add ( self.text() )
			elif self.eat(t_or):
				result.add_option()
			elif self.accept(t_dollar) or self.accept(t_scope_open):
				result.add ( self.chance() )
			else:
				result.add ( self.text_token() )
		return result

	def text(self):
		if self.accept(t_text): # text
			result = text(self.tokens[0])
			self.eat()
			return result
	def randword(self):
		if self.accept(t_text):
			result = self.tokens[0]
			self.eat()
			return randword(result)
	def text_token(self):
		if   self.accept(t_curly_open):  char = '{'
		elif self.accept(t_curly_close): char = '}'
		elif self.accept(t_func_open):   char = '('
		elif self.accept(t_func_close):  char = ')'
		elif self.accept(t_or):          char = '|'
		elif self.accept(t_percent):     char = '%'
		elif self.accept(t_range):       char = '-'
		elif self.accept(t_scope_close): char = ']'
		elif self.accept(t_mod_open):    char = '<'
		elif self.accept(t_mod_close):   char = '>'
		self.eat()
		return text(char)

	def chance(self):
		result = None
		if self.eat(t_dollar):
			if self.accept(t_text):
				result = self.randword()
			else:
				result = self.repeat()
		else:
			result = self.repeat()
		if self.eat(t_percent):
			if self.accept(t_text):
				try:
					chance_value = float(self.tokens[0])/(10.0 ** len(self.tokens[0]))
					self.eat()
					return chance(result, chance_value)
				except: pass
		return result
	def repeat(self):
		#return nothing()
		content = self.modify()
		min_times = 0
		max_times = 0
		if self.eat(t_curly_open):
			if self.accept(t_text):
				try:
					min_times = max_times = int(self.tokens[0])
				except:
					min_times = 1
					max_times = 1
				self.eat()
				if self.eat(t_range):
					if self.accept(t_text):
						try:
							max_times = int(self.tokens[0])
						except:
							min_times = 0
						self.eat()
			self.eat(t_curly_close)
			return repeat(content, min_times, max_times)
		return content
	def modify(self):
		result = self.container()
		pieces = []
		if self.eat(t_mod_open):
			contents = ""
			while not self.accept(t_mod_close):
				if self.accept(t_text):
					contents+=self.tokens[0]
					self.eat(t_text)
				else:
					break
			self.eat(t_mod_close)
			pieces = contents.split(',')
			if len(pieces) == 1:
				return modifier_factory( pieces[0], result )
			else:
				pass #TODO
		else:
			return result
	def container(self):
		if not self.eat(t_scope_open): self.eat(); return nothing()
		result = nothing()
		result = self.sequence()
		self.eat(t_scope_close)
		return result

def parse(text):
	p = parser()
	return p.parse(text)


#----------------#
#Constants follow#
#----------------#
mode_lower   = 0
mode_capital = 1
mode_upper   = 2

randword_reserved = ["anything"]

mod_jumble    = 2**1 #Something Good -> Smheonitg Good
mod_flip      = 2**2 #Something Good -> dooG gnihtemoS
mod_reverse   = 2**3 #Something Good -> Good Something
mod_acronym   = 2**4 #Something Good -> SG
mod_randcase  = 2**5 #Something Good -> sOMeTHIng goOd
mod_uppercase = 2**6 #Something Good -> SOMETHING GOOD
mod_lowercase = 2**7 #Something Good -> something good
mod_mix       = 2**8 #Something Good -> Good Something / Something Good
pmod_alternate= 2**9 #Something Good -> Something, Good, Something, Good, ...
pmod_word     = 2**10#Something Good -> Something      / Good
pmod_allbut   = 2**11#Something Good -> Good           / Something
pmod_replace  = 2**12#Something Good -> S0mething G00d
pmod_remove   = 2**13#Something Good -> Smething Gd

set_vowels     = 1
set_consonants = 2
set_digits     = 4
set_letters    = 8
set_uppercase  = 4096

token_characters = '$[]()-|:{}%<>\\' #Actually '\' isn't a token, but it's special so I can let it in here
word_separation = ' ,.;:"\'/!-+=?'
t_text       = 0 # !!TEXT!! ??? PROFIT!
t_dollar     = 1 # $
t_scope_open = 2 # [
t_scope_close= 3 # ]
t_func_open  = 4 # (
t_func_close = 5 # )
t_range      = 6 # -
t_or         = 7 # |
t_curly_open = 9 # {
t_curly_close= 10# }
t_percent    = 11# %
t_number     = 12# 0-9
t_mod_open   = 13# <
t_mod_close  = 14# >

if __name__=="__main__":
	for i in ["jumble","flip","reverse","acronym","randcase","upper","lower","mix","alternate","word","allbut","replace"]:
		a = parse("[\n[Will it seriously and fully honestly turn out ok?|Mill it seriously and fully honestly turn out ok]<"+i+" 1 3>]{2}")
		#a.structure(0)
		print "%s (%s)" % (a.to_string(),i)