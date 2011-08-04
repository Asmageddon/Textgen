import random
#out=''
#lchar=''
#for char in open('ins').read():
#	if char!="'":
#		if char in [' ','	',',','.','!','"',"'",'?',':',';','-']:
#			if lchar not in [' ','	',',','.','!','"',"'",'?',':',';','-']: out+=chr(10)
#		else: out+=char
#	lchar=char

x=''
for i in range(0,500):
	for i in range(0,random.randint(6,10)):
		if random.randint(0,3)>0: x+=chr(random.choice(range(97,122)))
		else: x+=random.choice(['a','o','u','i','e'])
	x+=chr(10)
open('rg1','w').write(x)
