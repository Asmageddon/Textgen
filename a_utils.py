import random

def commandize(string):
	command=[]
	current=""
	print string
	for char in string:
		if char in ["/n"," ",",","."]:
			if current!="":
				command+=[current]
				current=""
		else: current+=char
	if current !="":command+=[current[0:len(current)-1]]
	return command

def wranddict(dict):
	s=sum(dict.values())
	ss=random.randint(0,s)
	for i in dict:
		ss-=dict[i]
		if ss<=0: return i
def wrand(c):
	s=sum(c)
	ss=random.randint(0,s)
	i=0
	while ss>c[i]:
		ss-=c[i]
		i+=1
	return i
