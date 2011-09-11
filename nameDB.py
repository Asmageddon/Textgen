import random, name, os

def fc(filename):
	mission=[]
	mission+=[eval( "{"+open(os.path.join("data","mission", filename),"r").read()+"}" )]

words = eval(open(os.path.join("data", "words")).read())

def FormatText(string):
	lastchar=''
	result=""
	for char in string:
		if char in [',','.','!',';','?',':',' ',chr(10)] and lastchar!=char: result+=char
		lastchar=char
	return result

def GetText(string,mdata=None):
	#print string
	string+=chr(10)
	mode=0
	current=''
	result=''
	first=1
	chance=100.0
	olol=1
	i=''
	for char in string:
		#print char
		if char=="%":
			if first:
				current.capitalize()
				if current!='': first=0
			result+=current
			olol=1
			current=''
			mode=1
		elif char=="@":
			if first:
				current.capitalize()
				if current!='': first=0
			result+=current
			olol=1
			current=''
			mode=2
		elif char in [',','.','!',';','?',':','|',' ',chr(10)]:
			if mode==1:
				if random.randint(0.0,100.0)<=chance:
					if first:result+=GetWord(current).capitalize()
					else: result+=GetWord(current)
				first=0
				mode=0
				current=''
				chance=100
				olol=-1
				if char in ['.',';','!','?']: first=1
			elif mode==2: #(target,person,task,reward,penalty)
				what=[]
				if   current=='target': what=mdata[0]
				elif current=='person': what=mdata[1]
				elif current=='task':   what=mdata[2]
				elif current=='reward': what=mdata[3]
				elif current=='penalty':what=mdata[4]
				if len(i)>0:result+=what[int(i)-1]
				else: result+=random.choice(what)
				mode=0
				i=''
				current=''
				olol=-1
			if char==chr(10):
				if first: current.capitalize()
				result+=current
			elif char!='|':current+=char
		elif ord(char)>=48 and ord(char)<=57:
			if mode==1 and olol>0:
				if chance==100: chance=0
				chance+=olol*(ord(char)-48); olol/=10.0
			elif mode==2: i+=char
		else: current+=char
	return result