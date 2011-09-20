import random
#import nameDB as n
import textgen_parser as parser

s=[]
s+=["I'd drink $amount_liquid $drink!"]
s+=["$name $relation\s $name!"]
s+=["We need $number $container\'s of $explosive, please $action_fetch them for $person_who "]
s+=["I'm $willing_to to pay a lot for $container_liquid of $year $alcohol"]
s+=["Could you $action_fetch me some $item?"]
s+=["$Action_fetch for me a $animal $bodypart from it's $location_nature"]
s+=["We're making $animal $bodypart $food_liquid for tommorow $meal and we still lack ingredients!"]
s+=["How the hell can I eat $dish without my $metal $cutlery!? Get it from the kitchen!"]
s+=["$Name stole my $item! Retrieve it for me!"]
s+=["$Number $metal $shield\'s got stolen from our $w_equipment_storage, please get them back for us"]
s+=["I want $name\s $dessert before $time_of_day!"]
s+=["Steal some $w_equipment from $sport court near $building"]
s+=["$Action_fetch everything valuable you can find in $name\'s $building."]
s+=["I want you to kill $adjective $animal that has been rampaging around the $location_civ"]
s+=["A $adjective $animal drank a $container_liquid of my finest $alcohol, $action_kill that $person_addict!"]
s+=["I need $animal $bone for a $jewelery, I will give you one of my $crystal\'es"]
s+=["I want $w_carnage! $action_kill or $action_kill every single $animal, $animal and $monster you can find!"]
s+=["Know $name, the $person? Don't ask $w_ask\s, and you'll get $w_rich in no time"]
s+=["That $name! He dares to insult me about my fine $item! $action_evil him"]
s+=["$Name, that $adj_mad $w_creator of $adjective $item must be killed."]
s+=["$Name, the $person must be killed for $gq sins!"]
s+=["$Company will make you $w_rich if you $action_kill $name, that $person_bad"]
s+=["Request $name to make some $item for $time_of_week $time_of_day"]
s+=["Tell the $company that I need that $adjective item before $time_for"]
s+=["Could you $interaction $name for me?"]
s+=["Hey, play some $sport_type $sport with me!"]
s+=["I want a $metal $weapon_ranged"]
s+=["TELL ME! What is better? $cutlery or $cutlery!?"]
s+=["You meet a $adj_mystery $person dressed in $color $adj_cloth $cloth: $action yourself, $gqb says"]
s+=["A wild $animal appears! $name uses $pokeattack, it's $pokeffective"]
s+=["You find $wounded $person lying on ground.: 'H...help me, $name wanted to $action_evil me!"]
s+=["You find some $person\s fighting with $person\s, you take a $metal $weapon and walk away"]
s+=["You notice a scared $person in a dark alley. She cowers in fear, but gives you a $item_precious of $attribute $enchant_value"]
s+=["On $time_of_week there was a $weapon fighting contest!"]
s+=["$Group_of_people $relation $name, the $person!"]
s+=["Oh no! $company is in possesion of $element! We must stop them before they $action_evil us!"]
s+=["There is a $person infected with $disease in our $location!!!"]
s+=["There is no $person like our $name!"]
s+=["$trollword.Don't go to /[:l:]/..."]
s+=["$trollword $trollword $trollword $trollword $trollword"]
s+=["I $relation people with $color skin!"]
s+=["$random_number_of_dots$sentence_end"]
s+=["You $modalverb $action_daily $food!"]
s+=["$time_of_day is the time of $monster\s!"]
s+=["The $adj_good $name was $action_kill\ed by a $adj_evil $monster"]
s+=["A $person ordered everybody to train $martial_art"]
s+=["$digit_n0$digit$digit tons of $material_solid were used to build a $adj_size $fortification!"]
s+=["It has been proved that $anything+$anything=$anything"]
s+=["By utilizing $adj_arcane techniques you can combine $anything with $anything to create the $adj_power $cutlery!"]
s+=["Have faith in $god and you will be $salvation!"]
s+=["Thou shalt witness my $superpower and tremble in fear, $adj_evil $demon"]
s+=["In the name of $element_magic, $outfit $creature shall $action_evil you and deliver $adj_death death you deserve!"]
s+=["$monster $relative\s will $action $person_who as they did in $year with $anything"]
s+=["spam time! $anything $anything $anything $anything"]
s+=["You need to ask $name the $humanoid for help if you want to take down $name, $adj_evil $monster"]
s+=["There are $w_old tales that mention a $weapon that can $sentence_powerful"]

def sentence():
	return parser.parse(random.choice(s)).to_string()

def text(string):
	print string, string.__class__
	return parser.parse(string).to_string()

if __name__=="__main__":
	for i in s:
		r= parser.parse(i).to_string()
		print r
		if "$" in r: raw_input()
	print "!!! Be wary that it is highly likely not all problems will be spotted with this simple test"