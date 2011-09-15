import os, random, string

#Remove this later: (or not)
words = eval(open(os.path.join("data", "words")).read())

class node(object): pass

class nothing(node):
	def get(self): return self
	def to_string(self):
		return ""
	def structure(self):
		return ["-"]

class text(node): #Format: "Word"
	def __init__(self,content=""):
		self.value=content
	def get(self):
		return self
	def to_string(self):
		return self.value
	def structure(self):
		return 'text: "%s"' % self.value

def starts_with(text, chars):
	if len(text)>0:
		return text[0] in chars
	return 0
mode_lower   = 0
mode_capital = 1
mode_upper   = 2

class func(node): pass

def randword_builtin(value):
	if value == "anything":
		return '$'+random.choice(words.keys())
randword_reserved = ["anything"]
class randword(func): #Format: "$word" #This is also anything :3
	def __init__(self, value):
		self.value = value
	def get_mode(self, value):
		if value[0] not in string.uppercase:
			mode = 0
		else:
			if len( value ) > 1:
				if value[1] not in string.uppercase: mode = 1
				else: mode = 2
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
				key = result[1:]
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
	def structure(self):
		if   self.mode == mode_lower: mode_str = "lowercase"
		elif self.mode == mode_capital: mode_str = "Capital"
		elif self.mode == mode_upper: mode_str = "UPPERCASE"
		return ['randword: "%s", mode: %s' % (self.value, mode_str)]

class sequence(node): #Format: "Dunno"
	def __init__(self):
		self.data = [[]]
	def get(self):
		return self
	def to_string(self):
		result=""
		for i in random.choice(self.data):
			result+=i.to_string()
		return result
	def add(self, item):
		if item:
			self.data[-1]+=[item]
	def add_option(self):
		self.data+=[[]]

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

class chance(node):
	def __init__(self, object, chance):
		self.object = object
		self.chance = chance
	def get(self):
		if random.random() < self.chance: return self.object
		else: return nothing()
	def to_string(self):
		return self.get().to_string()

class char_range(node):
	def __init__(self, char1, char2):
		self.char1 = char1
		self.char2 = char2
	def get(self):
		a1=int(self.char1)
		a2=int(self.char2)
		return text(chr(random.randint(a1,a2)))
	def to_string(self):
		return self.get().to_string()

set_vowels     = 1
set_consonants = 2
set_digits     = 4
set_letters    = 8
set_uppercase  = 4096

class char_set(node):
	def __init__(self, set_name):
		self.set_type = 0
		set_name_lowercase = set_name.lower()
		if   set_name_lowercase in ['v','vowel']:     self.set_type = set_vowels
		elif set_name_lowercase in ['c','consonant']: self.set_type = set_consonants
		elif set_name_lowercase in ['0','digit']:     self.set_type = set_digits
		elif set_name_lowercase in ['l','letter']:    self.set_type = set_letters
		if set_name[0] in string.uppercase:           self.set_type|= set_uppercase
	def get(self):
		chars = []
		if   self.set_type & set_vowels:     chars = "auoei"
		elif self.set_type & set_consonants: chars = "qwrtypsdfghjklzxcvbnm"
		elif self.set_type & set_letters:    chars = "auoeiqwrtypsdfghjklzxcvbnm"
		elif self.set_type & set_digits:     chars = "0123456789"
		if self.set_type & set_uppercase: chars = chars.upper()
		return text(random.choice(chars))
	def to_string(self):
		return self.get().to_string()
token_characters = '$[]()-|:{}%\\' #Actually '\' isn't a token, but it's special so I can let it in here
word_separation = ' ,.;:"\'/!-+=<>?'
t_text       = 0 # !!TEXT!! ??? PROFIT!
t_dollar     = 1 # $
t_scope_open = 2 # [
t_scope_close= 3 # ]
t_func_start = 4 # (
t_func_end   = 5 # )
t_range      = 6 # -
t_or         = 7 # |
t_colon      = 8 # :
t_curly_open = 9 # {
t_curly_close= 10# }
t_percent    = 11# %
t_number     = 12# 0-9

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
				result += [t_func_start]
			elif char == ')':
				result += [t_func_end]
			elif char == '-':
				result += [t_range]
			elif char == '|':
				result += [t_or]
			elif char == ':':
				result += [t_colon]
			elif char == '{':
				result += [t_curly_open]
			elif char == '}':
				result += [t_curly_close]
			elif char == '%':
				result += [t_percent]
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
		self.result=sequence()
		self.tokens = tokenize(string)
		return self.WTHshouldInameIt()
	def WTHshouldInameIt(self):
		result = sequence()
		while len(self.tokens) > 0:
			if self.accept(t_text):
				result.add ( self.text() )
			else:
				result.add ( self.chance() )
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
	def text_token(self):
		if   self.accept(t_curly_open):  char = '{'
		elif self.accept(t_curly_close): char = '}'
		elif self.accept(t_func_start):  char = '('
		elif self.accept(t_func_end):    char = ')'
		elif self.accept(t_or):          char = '|'
		elif self.accept(t_percent):     char = '%'
		elif self.accept(t_range):       char = '-'
		elif self.accept(t_scope_close): char = ']'
	def chance(self):
		result = None
		if self.eat(t_dollar):
			if self.accept(t_text):
				result = self.randword()
			else:
				result = self.func_call()
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
	def randword(self):
		if self.accept(t_text):
			result = self.tokens[0]
			self.eat()
			return randword(result)
	def repeat(self):
		#return nothing()
		content = self.container()
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
	def container(self):
		if not self.eat(t_scope_open): self.eat(); return nothing()
		result = nothing()
		if self.accept(t_colon):
			result = self.set()
		else:
			result = self.sequence()
		self.eat(t_scope_close)
		return result
	def set(self):
		self.eat(t_colon)
		if self.accept(t_text):
			result = char_set(self.tokens[0])
			self.eat(t_text)
		self.eat(t_colon)
		return result


def parse(text):
	p = parser()
	return p.parse(text)

#for i in range(0,10):
#	print parse("Hey, do you know that Swift Geek[:v:] is a $adj_bad[[, $adj_bad]{0-2} and $adj_bad]%33 $weapon of $element_magic?").to_string()

pass
 #OUTDATED
 #character = ???????
 #digit_no0 = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
 #digit = "0" | digit_no0
 #text = { character }

 #sequence = { text | chance }
 #repeat = container, [ "{", num2, [ ",", num2 ] "}" ]
 #container = "[", [ set | sequence ], {'|', [set | sequence]} , "]"

 ###function = "$", num, ":", container
 ###function_call = "$", "(", num, ")"

 #set = ( ":letter:" | ":digit:" | ":LETTER:" | ":vowel:" | ":VOWEL:" | ":consonant:" | ":CONSONANT:" )

 #randword = "$", text
 #choice = sequence, [{ "|", sequence }]
 #range = character, "-", character
 #chance = [repeat | randword], ("%", num)

 #num = digit_no0, { digit }
 #num2 = { digit }

 #RESERVED NAMES:
   # $anything - anything
   # $master   - the person running the script
   # $slave    - the person master is talking to