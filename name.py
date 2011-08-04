import random, nameDB
import a_utils as utils

vowel=[['a','e','o','u','i'],
['y','ou',"ae",'y','oo']]
consonant=[['b','d','w','l','t','h','sh','g','k','p','m','n'],
['ch','c','z','r','j'],
['x','q','v','v']]
city_suffix=['ville','borg']
vowel_chance=[85,15]
consonant_chance=[70,20,10]
end_chance=[-30,15]
city_end_chance=[-40,30]
def generate(m):
	endchance=0
	if   m=="name": endchance=end_chance[0]
	elif m=="city": endchance=city_end_chance[0]
	else:           endchance=end_chance[0]
	mode=1
	name=''
	while random.randint(0,100)>endchance:
		if mode==1:
			name+=random.choice(consonant[utils.wrand(consonant_chance)])
			mode=0
		elif mode==0:
			name+=random.choice(vowel[utils.wrand(vowel_chance)])
			mode=1
		if   m=="name":endchance+=end_chance[1]
		elif m=="city": endchance+=city_end_chance[1]
	if m=="city": name+=random.choice(city_suffix)
	return name.capitalize()
