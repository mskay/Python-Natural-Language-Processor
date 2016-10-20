#!/usr/bin/env python
# ------------------------------------------------------ #
# Python Natural Language Processer:
# - Given inputs, this program stores information in its
# - knowledge base, making conclusions based on different
# - kinds of information. It can then recall facts about
# - different things infered from the input and knowledge
# - base.
# ------------------------------------------------------ #
import re

class Word:
    def __init__(self, singular, plural, equivalent_to_singular, not_equivalent_to_singular, equivalent_to_plural, not_equivalent_to_plural):
        self.singular = singular
        self.plural = plural
        self.equivalent_to_singular = equivalent_to_singular
        self.not_equivalent_to_singular = not_equivalent_to_singular
        self.equivalent_to_plural = equivalent_to_plural
        self.not_equivalent_to_plural = not_equivalent_to_plural


'''
Helper Functions
'''

def ask_plural_or_singular(x, y, first, second, tense, is_not):
	# Used to track where we are in the sentences when asking about 'x'
	counter = 0
	end_of_equivalent_plural = False
	end_of_equivalent_singular = False
	end_of_not_equivalent_plural = False
	end_of_not_equivalent_singular = False
	#print "known words", known_words

	if ((x.singular in known_words) or (x.plural in known_words)) and ((y.singular in known_words) or (y.plural in known_words)):
		print "Ok."
	elif ((x.singular in known_words) or (x.plural in known_words)) and ((y.singular not in known_words) or (y.plural not in known_words)):
		response = raw_input("What is the {} form of {}?\n".format(tense,second)).lower()
		# Means word has no plural or singular
		if response != "na":
			if tense == "plural":
				y.plural = response
			else:
				y.singular = response
	elif ((x.singular not in known_words) or (x.plural not in known_words)) and ((y.singular in known_words) or (y.plural in known_words)):
		response = raw_input("What is the {} form of {}?\n".format(tense,first)).lower()
		# Means word has no plural or singular
		if response != "na":
			if tense == "plural":
				x.plural = response
			else:
				x.singular = response

	else:
		# Means word has no plural or singular
		response = raw_input("What is the {} form of {}?\n".format(tense,first)).lower()
		response2 = raw_input("What is the {} form of {}?\n".format(tense,second)).lower()
		if response != "na":
			if tense == "plural":
				x.plural = response
			else:
				x.singular = response

		if response2 != "na":
			if tense == "plural":
				y.plural = response2
			else:
				y.singular = response2

			


	if 	x.plural not in known_words and x.plural != "":
		known_words.append(x.plural)
	if y.plural not in known_words and y.plural != "":
		known_words.append(y.plural)

	if x.singular not in known_words and x.singular != "":
		known_words.append(x.singular)
	if y.singular not in known_words and y.singular != "":
		known_words.append(y.singular)

	if tense == "plural":
		if is_not == True:
			if y.plural not in KB[KB.index(x)].not_equivalent_to_plural and y.plural != "":
				KB[KB.index(x)].not_equivalent_to_plural.append(y.plural)
		elif is_not == False:
			if y.plural not in KB[KB.index(x)].equivalent_to_plural and y.plural != "":
				KB[KB.index(x)].equivalent_to_plural.append(y.plural)

	elif tense == "singular":
		if is_not == True:
			if y.singular not in KB[KB.index(x)].not_equivalent_to_singular and y.singular != "":
				KB[KB.index(x)].not_equivalent_to_singular.append(y.singular)
		elif is_not == False:
			if y.singular not in KB[KB.index(x)].equivalent_to_singular and y.singular != "":
				KB[KB.index(x)].equivalent_to_singular.append(y.singular)

	
KB = []
known_words = []
previous = False
counter = 0
end_of_equivalent_plural = False
end_of_equivalent_singular = False
end_of_not_equivalent_plural = False
end_of_not_equivalent_singular = False
while True:
	x_in_KB = False
	y_in_KB = False
	is_not = False

	response = raw_input("")
	singularMatch = re.match( r'(A|An)?\s?(\w+) is ((?:not ))?((a|an)\s)?(\w+)\.', response)
	pluralMatch = re.match( r'(\w+) are ((?:not ))?(\w+)\.', response)
	questionIsMatch = re.match( r'Is (a |an )?(\w+) (a |an )?(\w+)\?', response)
	questionAreMatch = re.match( r'Are (\w+) (\w+)\?', response)
	question2Match = re.match( r'What do you know about (\w+)\?', response)

	# Test regular expressions here

	if singularMatch:

		# For the Anything else validity
		previous = False


		x = Word(singularMatch.group(2).lower(), "", [], [], [], [])
		y = Word(singularMatch.group(6).lower(), "", [], [], [], [])
		
		for i in KB:
			if x.singular == i.singular:
				x_in_KB = True
				x = i
			if y.singular == i.singular:
				y_in_KB = True
				y = i

		if x_in_KB == False:
			KB.append(x)
		if y_in_KB == False:
			KB.append(y)

		first = x.singular
		second = y.singular

		if singularMatch.group(3) == "not ":
			is_not = True
			if (y.singular in x.not_equivalent_to_singular) or KB[KB.index(y)].plural in KB[KB.index(x)].not_equivalent_to_plural:
				print "I know."
				continue
			ask_plural_or_singular(x,y,first, second, "plural", is_not)
			KB[KB.index(x)].not_equivalent_to_singular.append(y.singular)

			for i in KB:
				if x.singular in i.equivalent_to_singular:
					if y.plural != "" and y.plural not in i.not_equivalent_to_plural and y.plural != i.plural:
						i.not_equivalent_to_plural.append(y.plural)
					if y.singular != "" and y.singular not in i.not_equivalent_to_singular and y.singular != i.singular:
						i.not_equivalent_to_singular.append(y.singular)
				if y.singular == i.singular:			
					if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
						x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
					if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
						x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)
				elif y.plural == i.plural:
					if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
						x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
					if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
						x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)

		else:
			if y.singular in KB[KB.index(x)].equivalent_to_singular or KB[KB.index(y)].plural in KB[KB.index(x)].equivalent_to_plural:
					print "I know."
					continue
			ask_plural_or_singular(x,y,first, second, "plural", is_not)
			KB[KB.index(x)].equivalent_to_singular.append(y.singular)

			for i in KB:
				if x.singular in i.equivalent_to_singular:
					if y.plural != "" and y.plural not in i.equivalent_to_plural and y.plural != i.plural:
						i.equivalent_to_plural.append(y.plural)
					if y.singular != "" and y.singular not in i.equivalent_to_singular and y.singular != i.singular:
						i.equivalent_to_singular.append(y.singular)
				if y.singular == i.singular:				
					if i.equivalent_to_plural not in x.equivalent_to_plural:
						x.equivalent_to_plural.extend(i.equivalent_to_plural)
					if i.equivalent_to_singular not in x.equivalent_to_singular:
						x.equivalent_to_singular.extend(i.equivalent_to_singular)
					if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
						x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
					if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
						x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)

				elif y.plural == i.plural:
					if i.equivalent_to_plural not in x.equivalent_to_plural:
						x.equivalent_to_plural.extend(i.equivalent_to_plural)
					if i.equivalent_to_singular not in x.equivalent_to_singular:
						x.equivalent_to_singular.extend(i.equivalent_to_singular)
					if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
						x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
					if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
						x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)
	#-----------------------------------------------------------------------------------------------------------------------
	elif pluralMatch:
		# For the Anything else validity
		previous = False

		x = Word("", pluralMatch.group(1).lower(), [], [], [], [])
		y = Word("", pluralMatch.group(3).lower(), [], [], [], [])

		
		for i in KB:
			if x.plural == i.plural:# or x.singular == i.singular:
				x_in_KB = True
				x = i
			if y.plural == i.plural:
				y_in_KB = True
				y = i

		if x_in_KB == False:
			KB.append(x)
		if y_in_KB == False:
			KB.append(y)
	

		first = x.plural
		second = y.plural

		if pluralMatch.group(2) == "not ":
			is_not = True
			if y.plural in KB[KB.index(x)].not_equivalent_to_plural or KB[KB.index(y)].singular in KB[KB.index(x)].not_equivalent_to_singular:
				print "I know."
				continue
			ask_plural_or_singular(x,y,first, second, "singular", is_not)
			KB[KB.index(x)].not_equivalent_to_plural.append(y.plural)

			for i in KB:
				if x.plural in i.equivalent_to_plural:
					if y.plural != "" and y.plural not in i.not_equivalent_to_plural and y.plural != i.plural:
						i.not_equivalent_to_plural.append(y.plural)
					if y.singular != "" and y.singular not in i.not_equivalent_to_singular and y.singular != i.singular:
						i.not_equivalent_to_singular.append(y.singular)
				if y.singular == i.singular:			
					if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
						x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
					if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
						x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)
				elif y.plural == i.plural:	
					if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
						x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
					if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
						x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)

		else:
			if y.plural in KB[KB.index(x)].equivalent_to_plural or KB[KB.index(y)].singular in KB[KB.index(x)].equivalent_to_singular:
					print "I know."
					continue

			

			ask_plural_or_singular(x,y,first, second, "singular", is_not)
			KB[KB.index(x)].equivalent_to_plural.append(y.plural)


			for i in KB:
				if x.plural in i.equivalent_to_plural:
					if y.plural != "" and y.plural not in i.equivalent_to_plural and y.plural != i.plural:
						i.equivalent_to_plural.append(y.plural)
					if y.singular != "" and y.singular not in i.equivalent_to_singular and y.singular != i.singular:
						i.equivalent_to_singular.append(y.singular)
				if y.singular == i.singular:				
					if i.equivalent_to_plural not in x.equivalent_to_plural:
						x.equivalent_to_plural.extend(i.equivalent_to_plural)
					if i.equivalent_to_singular not in x.equivalent_to_singular:
						x.equivalent_to_singular.extend(i.equivalent_to_singular)
					if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
						x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
					if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
						x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)
				elif y.plural == i.plural:
					if i.equivalent_to_plural not in x.equivalent_to_plural:
						x.equivalent_to_plural.extend(i.equivalent_to_plural)
					if i.equivalent_to_singular not in x.equivalent_to_singular:
						x.equivalent_to_singular.extend(i.equivalent_to_singular)
					if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
						x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
					if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
						x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)



	elif questionIsMatch:
		# For the Anything else validity
		previous = False

		x = Word(questionIsMatch.group(2).lower(), "", [], [], [], [])
		y = Word(questionIsMatch.group(4).lower(), "", [], [], [], [])

		for i in KB:
			if x.singular == i.singular:
				x_in_KB = True
				x = i
			if y.singular == i.singular:
				y_in_KB = True
				y = i

		if x_in_KB == False:
			KB.append(x)
		if y_in_KB == False:
			KB.append(y)

		first = x.singular
		second = y.singular
		# Need to check if this exists
		if y.singular in KB[KB.index(x)].equivalent_to_singular or KB[KB.index(y)].plural in KB[KB.index(x)].equivalent_to_plural:
			print "Yes."
			is_not = False
			continue
		elif y.singular in KB[KB.index(x)].not_equivalent_to_singular or KB[KB.index(y)].plural in KB[KB.index(x)].not_equivalent_to_plural:
			print "No."
			is_not = True
			continue
		else:
			question = raw_input("I'm not sure, is it?\n")
			if question == "yes":
				is_not = False
				ask_plural_or_singular(x,y,first, second, "plural", is_not)
				KB[KB.index(x)].equivalent_to_singular.append(y.singular)
				for i in KB:
					if x.singular in i.equivalent_to_singular:
						if y.plural != "" and y.plural not in i.equivalent_to_plural and y.plural != i.plural:
							i.equivalent_to_plural.append(y.plural)
						if y.singular != "" and y.singular not in i.equivalent_to_singular and y.singular != i.singular:
							i.equivalent_to_singular.append(y.singular)
					if y.singular == i.singular:				
						if i.equivalent_to_plural not in x.equivalent_to_plural:
							x.equivalent_to_plural.extend(i.equivalent_to_plural)
						if i.equivalent_to_singular not in x.equivalent_to_singular:
							x.equivalent_to_singular.extend(i.equivalent_to_singular)
						if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
							x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
						if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
							x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)

					elif y.plural == i.plural:
						if i.equivalent_to_plural not in x.equivalent_to_plural:
							x.equivalent_to_plural.extend(i.equivalent_to_plural)
						if i.equivalent_to_singular not in x.equivalent_to_singular:
							x.equivalent_to_singular.extend(i.equivalent_to_singular)
						if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
							x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
						if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
							x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)
			
			elif question == "no":
				is_not = True
				ask_plural_or_singular(x,y,first, second, "plural", is_not)
				KB[KB.index(x)].not_equivalent_to_singular.append(y.singular)
				for i in KB:
					if x.singular in i.equivalent_to_singular:
						if y.plural != "" and y.plural not in i.not_equivalent_to_plural and y.plural != i.plural:
							i.not_equivalent_to_plural.append(y.plural)
						if y.singular != "" and y.singular not in i.not_equivalent_to_singular and y.singular != i.singular:
							i.not_equivalent_to_singular.append(y.singular)
					if y.singular == i.singular:			
						if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
							x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
						if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
							x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)
					elif y.plural == i.plural:
						if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
							x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
						if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
							x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)


	elif questionAreMatch:
		# For the Anything else validity
		previous = False

		x = Word("", questionAreMatch.group(1).lower(), [], [], [], [])
		y = Word("", questionAreMatch.group(2).lower(), [], [], [], [])

		for i in KB:
			if x.plural == i.plural:# or x.singular == i.singular:
				x_in_KB = True
				x = i
			if y.plural == i.plural:
				y_in_KB = True
				y = i

		if x_in_KB == False:
			KB.append(x)
		if y_in_KB == False:
			KB.append(y)

		first = x.plural
		second = y.plural
		# Need to check if this exists
		if y.plural in KB[KB.index(x)].equivalent_to_plural or KB[KB.index(y)].singular in KB[KB.index(x)].equivalent_to_singular:
			print "Yes."
			is_not = False
			continue
		elif y.plural in KB[KB.index(x)].not_equivalent_to_plural or KB[KB.index(y)].singular in KB[KB.index(x)].not_equivalent_to_singular:
			print "No."
			is_not = True
			continue
		else:
			question = raw_input("I'm not sure, are they?\n")
			if question == "yes":
				is_not = False
				ask_plural_or_singular(x,y,first, second, "singular", is_not)
				KB[KB.index(x)].equivalent_to_plural.append(questionAreMatch.group(2))
				for i in KB:
					if x.plural in i.equivalent_to_plural:
						if y.plural != "" and y.plural not in i.equivalent_to_plural and y.plural != i.plural:
							i.equivalent_to_plural.append(y.plural)
						if y.singular != "" and y.singular not in i.equivalent_to_singular and y.singular != i.singular:
							i.equivalent_to_singular.append(y.singular)
					if y.singular == i.singular:				
						if i.equivalent_to_plural not in x.equivalent_to_plural:
							x.equivalent_to_plural.extend(i.equivalent_to_plural)
						if i.equivalent_to_singular not in x.equivalent_to_singular:
							x.equivalent_to_singular.extend(i.equivalent_to_singular)
						if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
							x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
						if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
							x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)
					elif y.plural == i.plural:
						if i.equivalent_to_plural not in x.equivalent_to_plural:
							x.equivalent_to_plural.extend(i.equivalent_to_plural)
						if i.equivalent_to_singular not in x.equivalent_to_singular:
							x.equivalent_to_singular.extend(i.equivalent_to_singular)
						if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
							x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
						if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
							x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)

			elif question == "no":
				is_not = True
				ask_plural_or_singular(x,y,first, second, "singular", is_not)
				KB[KB.index(x)].not_equivalent_to_plural.append(questionAreMatch.group(2))
				for i in KB:
					if x.plural in i.equivalent_to_plural:
						if y.plural != "" and y.plural not in i.not_equivalent_to_plural and y.plural != i.plural:
							print "ayyy"
							i.not_equivalent_to_plural.append(y.plural)
						if y.singular != "" and y.singular not in i.not_equivalent_to_singular and y.singular != i.singular:
							print "ah"
							i.not_equivalent_to_singular.append(y.singular)
					if y.singular == i.singular:			
						if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
							x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
						if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
							x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)
					elif y.plural == i.plural:	
						if i.not_equivalent_to_plural not in x.not_equivalent_to_plural:
							x.not_equivalent_to_plural.extend(i.not_equivalent_to_plural)
						if i.not_equivalent_to_singular not in x.not_equivalent_to_singular:
							x.not_equivalent_to_singular.extend(i.not_equivalent_to_singular)

		
		
	

	# What do you know about x?
	elif question2Match:
		# For the Anything else validity
		previous = True
		x = question2Match.group(1).lower()

		# new word different from last one asked
		if x != y:
			counter = 0
			end_of_equivalent_plural = False
			end_of_equivalent_singular = False
			end_of_not_equivalent_plural = False
			end_of_not_equivalent_singular = False

		for i in KB:
			# Asking about proper noun
			if i.singular == x and i.plural == "":
				if end_of_equivalent_singular == False:
					if counter < len(i.equivalent_to_singular):
						if i.equivalent_to_singular[counter] == "a" or i.equivalent_to_singular[counter] == "e" or i.equivalent_to_singular[counter] == "i" or i.equivalent_to_singular[counter] == "o" or i.equivalent_to_singular[counter] == "u":
							print x.title(), "is an", i.equivalent_to_singular[counter]
							counter = counter + 1
							y = x
							continue
						else:
							print x.title(), "is a", i.equivalent_to_singular[counter]
							counter = counter + 1
							y = x
							continue

					counter = 0
					end_of_equivalent_singular = True

				if end_of_not_equivalent_singular == False:
					if counter < len(i.not_equivalent_to_singular):
						if i.not_equivalent_to_singular[counter] == "a" or i.not_equivalent_to_singular[counter] == "e" or i.not_equivalent_to_singular[counter] == "i" or i.not_equivalent_to_singular[counter] == "o" or i.not_equivalent_to_singular[counter] == "u":
							print x.title(), "is not an", i.not_equivalent_to_singular[counter]
							counter = counter + 1
							y = x
							continue
						else:
							print x.title(), "is not a", i.not_equivalent_to_singular[counter]
							counter = counter + 1
							y = x
							continue

					counter = 0
					end_of_not_equivalent_singular = True

				if end_of_equivalent_plural == False:
					if counter < len(i.equivalent_to_plural):
						word = i.equivalent_to_plural[counter]
						if word[len(word)-1] != "s":
						#if j[len(j)-1] != "s":
							print x.title(), "is", i.equivalent_to_plural[counter]
							counter = counter + 1
							y = x
							continue

					counter = 0
					end_of_equivalent_plural = True

				if end_of_not_equivalent_plural == False:
					if counter < len(i.not_equivalent_to_plural):
						word = i.not_equivalent_to_plural[counter]
						if word[len(word)-1] != "s":
							print x.title(), "is not", i.not_equivalent_to_plural[counter]
							counter = counter + 1
							y = x
							continue
					
					counter = 0
					end_of_not_equivalent_plural = True

				if end_of_not_equivalent_plural == True and end_of_equivalent_plural == True and end_of_not_equivalent_singular == True and end_of_equivalent_singular == True:
					print "I don't know anything else about", x

			elif i.singular == x or i.plural == x:

				if end_of_equivalent_plural == False:
					if counter < len(i.equivalent_to_plural):
						print x.title(), "are", KB[KB.index(i)].equivalent_to_plural[counter]
						counter = counter + 1
						y = x
						continue

					counter = 0
					end_of_equivalent_plural = True
				if end_of_not_equivalent_plural == False:
					if counter < len(i.not_equivalent_to_plural):
						print x.title(), "are not", KB[KB.index(i)].not_equivalent_to_plural[counter]
						counter = counter + 1
						y = x
						continue

					counter = 0
					end_of_not_equivalent_plural = True
				if end_of_equivalent_singular == False:
					for j in KB:
						if (x in j.equivalent_to_singular) or (x in j.equivalent_to_plural) and j.plural == "":
							# Removes s from end of
							if x.endswith('s'):
   								x = x[:-1]
   							if x[0] == "a" or x[0] == "e" or x[0] == "i" or x[0] == "o" or x[0] == "u":
								print j.singular.title(), "is an", x
								y = x
								continue
							else:
								print j.singular.title(), "is a", x
								y = x
								continue

					end_of_equivalent_singular = True
					counter = 0
						
				if end_of_not_equivalent_singular == False:
					# No plural so must be proper noun
					for k in KB:
						if (x in k.not_equivalent_to_singular) or (x in k.not_equivalent_to_plural) and k.plural == "":

							if x.endswith('s'):
   								x = x[:-1]
   							if x[0] == "a" or x[0] == "e" or x[0] == "i" or x[0] == "o" or x[0] == "u":
								print k.singular.title(), "is not an", x
								y = x
								continue
							else:
								print k.singular.title(), "is not a", x
								y = x
								continue

						end_of_not_equivalent_singular = True
						counter = 0
					
				if end_of_not_equivalent_plural == True and end_of_equivalent_plural == True and end_of_not_equivalent_singular == True and end_of_equivalent_singular == True:
					print "I don't know anything else about", x
				
	elif response == "Anything else?":
		# For the Anything else validity
		if previous == True:

			# new word different from last one asked
			if x != y:
				counter = 0
				end_of_equivalent_plural = False
				end_of_equivalent_singular = False
				end_of_not_equivalent_plural = False
				end_of_not_equivalent_singular = False

			for i in KB:
				# Asking about proper noun
				if i.singular == x and i.plural == "":
					if end_of_equivalent_singular == False:
						if counter < len(i.equivalent_to_singular):
							if i.equivalent_to_singular[counter] == "a" or i.equivalent_to_singular[counter] == "e" or i.equivalent_to_singular[counter] == "i" or i.equivalent_to_singular[counter] == "o" or i.equivalent_to_singular[counter] == "u":
								print x.title(), "is an", i.equivalent_to_singular[counter]
								counter = counter + 1
								y = x
								continue
							else:
								print x.title(), "is a", i.equivalent_to_singular[counter]
								counter = counter + 1
								y = x
								continue

						counter = 0
						end_of_equivalent_singular = True

					if end_of_not_equivalent_singular == False:
						if counter < len(i.not_equivalent_to_singular):
							if i.not_equivalent_to_singular[counter] == "a" or i.not_equivalent_to_singular[counter] == "e" or i.not_equivalent_to_singular[counter] == "i" or i.not_equivalent_to_singular[counter] == "o" or i.not_equivalent_to_singular[counter] == "u":
								print x.title(), "is not an", i.not_equivalent_to_singular[counter]
								counter = counter + 1
								y = x
								continue
							else:
								print x.title(), "is not a", i.not_equivalent_to_singular[counter]
								counter = counter + 1
								y = x
								continue

						counter = 0
						end_of_not_equivalent_singular = True

					if end_of_equivalent_plural == False:
						if counter < len(i.equivalent_to_plural):
							word = i.equivalent_to_plural[counter]
							if word[len(word)-1] != "s":
							#if j[len(j)-1] != "s":
								print x.title(), "is", i.equivalent_to_plural[counter]
								counter = counter + 1
								y = x
								continue

						counter = 0
						end_of_equivalent_plural = True

					if end_of_not_equivalent_plural == False:
						if counter < len(i.not_equivalent_to_plural):
							word = i.not_equivalent_to_plural[counter]
							if word[len(word)-1] != "s":
							#if j[len(j)-1] != "s":
								print x.title(), "is not", i.not_equivalent_to_plural[counter]
								counter = counter + 1
								y = x
								continue
						
						counter = 0
						end_of_not_equivalent_plural = True

					if end_of_not_equivalent_plural == True and end_of_equivalent_plural == True and end_of_not_equivalent_singular == True and end_of_equivalent_singular == True:
						print "I don't know anything else about", x

				elif i.singular == x or i.plural == x:

					if end_of_equivalent_plural == False:
						if counter < len(i.equivalent_to_plural):
							print x.title(), "are", KB[KB.index(i)].equivalent_to_plural[counter]
							counter = counter + 1
							y = x
							continue

						counter = 0
						end_of_equivalent_plural = True
					if end_of_not_equivalent_plural == False:
						if counter < len(i.not_equivalent_to_plural):
							print x.title(), "are not", KB[KB.index(i)].not_equivalent_to_plural[counter]
							counter = counter + 1
							y = x
							continue

						counter = 0
						end_of_not_equivalent_plural = True
					if end_of_equivalent_singular == False:
						for j in KB:
							if (x in j.equivalent_to_singular) or (x in j.equivalent_to_plural) and j.plural == "":
								# Removes s from end of
								if x.endswith('s'):
	   								x = x[:-1]
	   							if x[0] == "a" or x[0] == "e" or x[0] == "i" or x[0] == "o" or x[0] == "u":
									print j.singular.title(), "is an", x
									y = x
									continue
								else:
									print j.singular.title(), "is a", x
									y = x
									continue

						end_of_equivalent_singular = True
						counter = 0
							
					if end_of_not_equivalent_singular == False:
						# No plural so must be proper noun
						for k in KB:
							if (x in k.not_equivalent_to_singular) or (x in k.not_equivalent_to_plural) and k.plural == "":

								if x.endswith('s'):
	   								x = x[:-1]
	   							if x[0] == "a" or x[0] == "e" or x[0] == "i" or x[0] == "o" or x[0] == "u":
									print k.singular.title(), "is not an", x
									y = x
									continue
								else:
									print k.singular.title(), "is not a", x
									y = x
									continue

							end_of_not_equivalent_singular = True
							counter = 0
						
					if end_of_not_equivalent_plural == True and end_of_equivalent_plural == True and end_of_not_equivalent_singular == True and end_of_equivalent_singular == True:
						print "I don't know anything else about", x
		else:
			print "Invalid Question."
		

	elif response == "Bye.":
		exit()
	else:
		print "I don't understand."


