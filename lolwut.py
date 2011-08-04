import random
import nameDB as n
s=[]
s+=["I'd drink %amount-liquid %drink|!"]
s+=["%name %relation|s %name|!"]
s+=["We need %number %container|s of %explosive, please get them for us"]
s+=["I'm willing to pay a lot for %cont-liquid of %year|' %alcohol"]
s+=["Could you %action-fetch me some %item?"]
s+=["%action-fetch for me a %animal %bodypart from it's %loc-nature"]
s+=["We're making %animal %bodypart %food-liquid for tommorow %meal and we still lack ingredients!"]
s+=["How the hell can I eat %dish without my %metal %cutlery!? Get it from the kitchen!"]
s+=["%name stole my %item! Retrieve it for me!"]
s+=["%number %metal %shield|s got stolen from our armory, please get them back for us"]
s+=["I want %name|'s %dessert before %time-of-day!"]
s+=["Steal some equipment from %sport court near %building"]
s+=["Steal everything valuable you can find in %name|'s %building."]
s+=["I want you to kill %adjective %animal that has been rampaging around the %loc-civ"]
s+=["A %adjective %animal drunk a bottle of my finest %alcohol, kill that %person-addict!"]
s+=["I need %animal %bone for a %jewelery, I will give you one of my %crystal|es"]
s+=["I WANT BLOOD! %action-kill or %action-kill every single %animal, %animal and %animal you can find!"]
s+=["Know %name, the %person? Don't ask questions, and you'll get rich in no time"]
s+=["That %name! He dares to insult me about my fine %item! %action-evil him"]
s+=["%name, that mad creator of %adjective %item must be killed."]
s+=["%name, the %person must be killed for %gq sins!"]
s+=["%company will make you rich if you %action-kill %name, that %person-bad"]
s+=["Request %name to make some %item for %time-of-week %time-of-day"]
s+=["Tell the %company that I need that %adjective item before %time-for"]
s+=["Could you %interaction %name for me?"]
s+=["Hey, play some %sport with me!"]
s+=["I want a %metal %weapon-ranged"]
s+=["TELL ME! What is better? %cutlery or %cutlery!?"]
s+=["You meet a %a-mystery %person dressed in %8color %15a-cloth %cloth: '%action yourself, %gqb says'"]
s+=["A wild %animal appears! %name uses %pokeattack, it's %pokeffective"]
s+=["You find %9wounded %person lying on ground.: 'H...help me, %name wanted to %action-evil me!'"]
s+=["You find some %person|s fighting with %person|s, you take a %metal %weapon and walk away"]
s+=["You notice a scared %person in a dark alley. She cowers in fear, but gives you a %item-precious of %attribute %3enchant-value"]
s+=["On %time-of-week there was a %weapon fighting contest!"]
s+=["%group-of-people %relation %name, the %person|!"]
s+=["Oh no! %company is in possesion of %element|! We must stop them before they %action-evil us!"]
s+=["There is a %person-any infected with %disease in our %location|!!!"]
s+=["There is no %person-any like our %name|!"]
s+=["%trollword|.Don't go to /%letter|/..."]
s+=["%trollword %trollword %trollword %7trollword %9trollword"]
s+=["I hate people with %color skin!"]
s+=["%random-number-of-dots|%sentence-end"]
s+=["You %modalverb %consume|!"]
s+=["%time-of-day is the time of %monster|s!"]
s+=["The %a-good %name was %action-kill|ed by a %a-evil %monster"]
s+=["A %person ordered everybody to train %martial-art"]
s+=["%digit-n0|%digit|%digit tons of %mat-solid were used to build a %a-size %fortification|!"]
s+=["It has been proved that %anything|+%anything|=%anything"]
s+=["By utilizing %a-arcane techniques you can combine %anything with %anything to create the %a-power %cutlery|!"]
s+=["Have faith in %god and you will be %salvation|!"]
s+=["Thou shalt witness my %superpower and tremble in fear, %a-evil %demon"]
s+=["In the name of %element-magic, %outfit fairy shall %action-evil you and deliver %a-death death you deserve!"]
def sentence():
	return n.GetText(random.choice(s))

if __name__=="__main__":
	for i in range(0,3):
		a=""
		for i in range(0,10):
			a+=sentence()
		if len(a)>250:
			if random.randint(0,1): a=a[:249]
			else: a=a[-249:]
		print a
		print ""