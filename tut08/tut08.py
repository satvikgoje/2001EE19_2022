try:
	from platform import python_version
	import os
	import pandas as pd

	from datetime import datetime
	start_time = datetime.now()

	# Help
	def scorecard():

		try:
			# reading 1st innings input file text varible
			text = open("pak_inns1.txt", "r").read()

			#deleting the content already existing in file
			isExist = os.path.isfile(r'Scorecard.txt')
			if(isExist):
				f = open('Scorecard.txt', "r+") 
				f.truncate()
				
			sentence_1 = []

			for row in text.split("\n"):
				sentence_1.append(row)  # making a list for each list2 of the commentary

			while ("" in sentence_1):
				sentence_1.remove("")  # removing empty characters in sentence_1 list

			for i in range(62):

				sentence_1[i] = sentence_1[i][:3]+","+sentence_1[i][3:]

			for i in range(62, 123):  # adding extra comma after every ball number

				sentence_1[i] = sentence_1[i][:4]+","+sentence_1[i][4:]

			l = len(sentence_1)  # finding lenght of the list

			list2 = []

			list1 = []

			for i in range(l):
				list1 = sentence_1[i].split(',')
				list2.append(list1)        # splitting each list2 of commentary @ ','

			lx = len(list2)
			batsman = [] #of pakistan players
			bowlers = []

			for i in range(lx):
				players = list2[i][1].split('to')
				# appending all batsman and bowler names into respective lists
				bowlers.append(players[0])
				batsman.append(players[1])
			batsman = list(dict.fromkeys(batsman))  # removing duplicates
			bowlers = list(dict.fromkeys(bowlers))

			# creating a dataframe 'mybatsman' with required column and row names and initializing with 0's
			mybatsman = pd.DataFrame(0, batsman, ['status', 'R', 'B', '4s', '6s', 'SR'])

			mybatsman['status'] = 'not out'  # initializing staus column with 'not out'

			# creating a dataframe 'mybatsman' with required column and row names and initializing with 0's
			mybowlers = pd.DataFrame(
				0, bowlers, ['O', 'M', 'R', 'W', 'NB', 'WD', 'EC', 'B'])

			extra = 0
			wide = 0
			score = 0
			wickets = 0
			noball = 0
			bytes = 0
			leg_bye = 0
			fall = ''

			content = []

			for i in range(lx):  # iterating through every ball
				ball_no = list2[i][0]
				players = list2[i][1].split('to')
				batsname = players[1]  # finding batsamn and bowler names for every deliery
				bowler = players[0]

				# converting the verdict of the delivery into lower case
				list2[i][2] = list2[i][2].lower()

				if list2[i][2] == " wide":  # if the delivery is wide
					wide = wide+1  # adding +1 to wide variable
					score = score+1
					# updating bowler's runs
					mybowlers.loc[bowler, 'R'] = mybowlers.loc[bowler, 'R']+1
					# Updating count of wides
					mybowlers.loc[bowler, 'WD'] = mybowlers.loc[bowler, 'WD']+1

				# if the verdict of the delivery if '4'
				elif list2[i][2] == " four" or list2[i][2] == ' 4' or list2[i][2] == ' 4 runs':
					mybatsman.loc[batsname, 'R'] = mybatsman.loc[batsname, 'R']+4
					mybatsman.loc[batsname, '4s'] = mybatsman.loc[batsname, '4s']+1
					mybatsman.loc[batsname, 'B'] = mybatsman.loc[batsname, 'B']+1
					mybowlers.loc[bowler, 'B'] = mybowlers.loc[bowler, 'B']+1
					mybowlers.loc[bowler, 'R'] = mybowlers.loc[bowler, 'R']+4
					score = score+4

				# if the verdict of the ball is '6'
				elif list2[i][2] == ' six' or list2[i][2] == ' 6' or list2[i][2] == ' 6 runs':
					mybatsman.loc[batsname, '6s'] = mybatsman.loc[batsname, '6s'] + 1
					mybatsman.loc[batsname, 'R'] = mybatsman.loc[batsname, 'R'] + 6
					mybatsman.loc[batsname, 'B'] = mybatsman.loc[batsname, 'B'] + 1

					mybowlers.loc[bowler, 'B'] = mybowlers.loc[bowler, 'B'] + 1
					mybowlers.loc[bowler, 'R'] = mybowlers.loc[bowler, 'R'] + 6
					score = score + 6

				elif list2[i][2] == ' 1 run' or list2[i][2] == ' 1':  # if the verdict of the ball is'1' run
					mybatsman.loc[batsname, 'R'] = mybatsman.loc[batsname, 'R'] + 1
					mybatsman.loc[batsname, 'B'] = mybatsman.loc[batsname, 'B'] + 1

					mybowlers.loc[bowler, 'B'] = mybowlers.loc[bowler, 'B'] + 1
					mybowlers.loc[bowler, 'R'] = mybowlers.loc[bowler, 'R'] + 1
					score = score + 1

				# it the verdict of the ball is '2' runs
				elif list2[i][2] == ' 2 runs' or list2[i][2] == ' 2 run' or list2[i][2] == ' 2':
					mybatsman.loc[batsname, 'R'] = mybatsman.loc[batsname, 'R'] + 2
					mybatsman.loc[batsname, 'B'] = mybatsman.loc[batsname, 'B'] + 1

					mybowlers.loc[bowler, 'B'] = mybowlers.loc[bowler, 'B'] + 1
					mybowlers.loc[bowler, 'R'] = mybowlers.loc[bowler, 'R'] + 2
					score = score + 2

				# it the verdict of the ball is '3' runs
				elif list2[i][2] == ' 3 runs' or list2[i][2] == ' 3 run' or list2[i][2] == ' 3':
					mybatsman.loc[batsname, 'R'] = mybatsman.loc[batsname, 'R'] + 3
					mybatsman.loc[batsname, 'B'] = mybatsman.loc[batsname, 'B'] + 1

					mybowlers.loc[bowler, 'B'] = mybowlers.loc[bowler, 'B'] + 1
					mybowlers.loc[bowler, 'R'] = mybowlers.loc[bowler, 'R'] + 3
					score = score + 3
				elif list2[i][2] == ' no run' or list2[i][2] == ' no':  # if delivery is a dot and legal
					mybatsman.loc[batsname, 'B'] = mybatsman.loc[batsname, 'B'] + 1
					mybowlers.loc[bowler, 'B'] = mybowlers.loc[bowler, 'B'] + 1

				elif list2[i][2] == ' leg byes':  # if delivery verdict is leg byes
					mybatsman.loc[batsname, 'B'] = mybatsman.loc[batsname, 'B'] + 1
					mybowlers.loc[bowler, 'B'] = mybowlers.loc[bowler, 'B'] + 1

					if list2[i][3] == ' four' or list2[i][3] == ' 4' or list2[i][3] == ' 4 runs':  # for 4 leg byes
						leg_bye = leg_bye + 4
						score = score + 4

					if list2[i][3] == ' 1 run' or list2[i][3] == ' 1':  # for 1leg bye
						leg_bye = leg_bye + 1
						score = score + 1

				elif list2[i][2] == ' byes':  # if delivery verdict is bye
					mybatsman.loc[batsname, 'B'] = mybatsman.loc[batsname, 'B'] + 1
					mybowlers.loc[bowler, 'B'] = mybowlers.loc[bowler, 'B'] + 1

					if list2[i][3] == ' 1 run' or list2[i][3] == ' 1':  # for 1bye
						bytes = bytes + 1
						score = score + 1
				else:  # if the verdict of the delivery is a wicket
					mybatsman.loc[batsname, 'B'] = mybatsman.loc[batsname, 'B'] + 1
					mybowlers.loc[bowler, 'B'] = mybowlers.loc[bowler, 'B'] + 1
					wickets = wickets + 1  # increasing wicket count
					# adding to the the fall of wickets string
					add = str(score) + '-' + str(wickets) + \
						'(' + batsname + ',' + ball_no + ')'
					fall = fall+add
					fall = fall+" "

					content = list2[i][2].split('!')  # spltting @ '!'

					if content[0] == ' out bowled':  # if the wicket is by 'bowled'
						mybatsman.loc[batsname, 'status'] = 'bytes ' + bowler
						mybowlers.loc[bowler, 'W'] = mybowlers.loc[bowler, 'W'] + 1
					elif content[0] == ' out lbw':  # if wicket is by lbw
						mybatsman.loc[batsname, 'status'] = 'lbw ' + bowler
						mybowlers.loc[bowler, 'W'] = mybowlers.loc[bowler, 'W'] + 1
					else:  # if the wicket is by 'caught out'
						content2 = content[0].split('by')
						mybatsman.loc[batsname, 'status'] = 'c ' + content2[1] + \
							' bytes ' + bowler  # updating status of the batsman
						mybowlers.loc[bowler, 'W'] = mybowlers.loc[bowler, 'W'] + 1

				# strike rate of the batsman
				mybatsman.loc[batsname, 'SR'] = int(
					(mybatsman.loc[batsname, 'R'] / mybatsman.loc[batsname, 'B']) * 100)
				mybowlers.loc[bowler, 'O'] = (mybowlers.loc[bowler, 'B']//6)+(
					(mybowlers.loc[bowler, 'B'] % 6)*0.1)  # overs bowled by the bowler

				mybowlers.loc[bowler, 'EC'] = mybowlers.loc[bowler, 'R'] / \
					(mybowlers.loc[bowler, 'B']/6)  # economy of the bowler

			extra = leg_bye + bytes + wide  # total extra's of the innings

			# writing the scorecard of the first innings into scorecard.txt file
			with open('Scorecard.txt', 'a') as f:
				f.write('SCORECARD')
				f.write('\n')
				f.write('Pakistan innings')
				f.write('\n')
				df = mybatsman.to_string(header=True, index=True)
				f.write(df)
				f.write('\nExtras\t\t' + str(extra) + '(bytes ' + str(bytes) + ', leg_bye ' +
						str(leg_bye) + ', w ' + str(wide) + ', nb ' + str(noball) + ')')
				f.write('\n')
				f.write('\nTotal\t\t' + str(score) + ' (' + str(wickets) +
						' wkts, ' + str(mybowlers['O'].sum()) + ' Ov)\n')
				f.write('\n')
				f.write('fall of wickets')
				f.write('\n')
				f.write(fall)
				f.write('\n')
				f.write('bowler')
				f.write('\n')
				df1 = mybowlers.to_string(header=True, index=True)
				f.write(df1)
				f.write('\n')

			# reading 2nd innings input file into 'text2'
			text2 = open("india_inns2.txt", "r").read()

			sent2 = []

			for row in text2.split("\n"):
				sent2.append(row)

			while ("" in sent2):
				sent2.remove("")

			for i in range(61):

				sent2[i] = sent2[i][:3]+","+sent2[i][3:]

			for i in range(61, 124):

				sent2[i] = sent2[i][:4]+","+sent2[i][4:]

			l = len(sent2)

			line2 = []

			list12 = []

			for i in range(l):
				list12 = sent2[i].split(',')
				line2.append(list12)

			lx = len(line2)
			batsman2 = []
			bowlers2 = []
			cnt = 0

			for i in range(lx):
				players2 = line2[i][1].split('to')
				bowlers2.append(players2[0])
				batsman2.append(players2[1])
			batsman2 = list(dict.fromkeys(batsman2))
			bowlers2 = list(dict.fromkeys(bowlers2))

			mybatsman2 = pd.DataFrame(
			    0, batsman2, ['status', 'R', 'B', '4s', '6s', 'SR'])

			mybatsman2['status'] = 'not out'

			mybowlers2 = pd.DataFrame(
			    0, bowlers2, ['O', 'M', 'R', 'W', 'NB', 'WD', 'EC', 'B'])

			extra2 = 0
			wide2 = 0
			score2 = 0
			wickets2 = 0
			noball2 = 0
			b2 = 0
			leg_bye = 0
			fall2 = ''

			content3 = []

			for i in range(lx):
				ball_no = line2[i][0]
				players = line2[i][1].split('to')
				batsname = players[1]
				bowler = players[0]

				line2[i][2] = line2[i][2].lower()
				if line2[i][2] == " wide":
					wide2 = wide2+1
					score2 = score2+1
					mybowlers2.loc[bowler, 'R'] = mybowlers2.loc[bowler, 'R']+1
					mybowlers2.loc[bowler, 'WD'] = mybowlers2.loc[bowler, 'WD']+1
				elif line2[i][2] == ' 3 wides':
					wide2 = wide2+3
					score2 = score2+3
					mybowlers2.loc[bowler, 'R'] = mybowlers2.loc[bowler, 'R']+3
					mybowlers2.loc[bowler, 'WD'] = mybowlers2.loc[bowler, 'WD']+3
				elif line2[i][2] == ' 2 wides':
					wide2 = wide2+2
					score2 = score2+2
					mybowlers2.loc[bowler, 'R'] = mybowlers2.loc[bowler, 'R']+2
					mybowlers2.loc[bowler, 'WD'] = mybowlers2.loc[bowler, 'WD']+2
				elif line2[i][2] == " four" or line2[i][2] == ' 4' or line2[i][2] == ' 4 runs':
					mybatsman2.loc[batsname, 'R'] = mybatsman2.loc[batsname, 'R']+4
					mybatsman2.loc[batsname, '4s'] = mybatsman2.loc[batsname, '4s']+1
					mybatsman2.loc[batsname, 'B'] = mybatsman2.loc[batsname, 'B']+1
					mybowlers2.loc[bowler, 'B'] = mybowlers2.loc[bowler, 'B']+1
					mybowlers2.loc[bowler, 'R'] = mybowlers2.loc[bowler, 'R']+4
					score2 = score2+4

				elif line2[i][2] == ' six' or line2[i][2] == ' 6' or line2[i][2] == ' 6 runs':
					mybatsman2.loc[batsname, '6s'] = mybatsman2.loc[batsname, '6s'] + 1
					mybatsman2.loc[batsname, 'R'] = mybatsman2.loc[batsname, 'R'] + 6
					mybatsman2.loc[batsname, 'B'] = mybatsman2.loc[batsname, 'B'] + 1

					mybowlers2.loc[bowler, 'B'] = mybowlers2.loc[bowler, 'B'] + 1
					mybowlers2.loc[bowler, 'R'] = mybowlers2.loc[bowler, 'R'] + 6
					score2 = score2 + 6

				elif line2[i][2] == ' 1 run' or line2[i][2] == ' 1':
					mybatsman2.loc[batsname, 'R'] = mybatsman2.loc[batsname, 'R'] + 1
					mybatsman2.loc[batsname, 'B'] = mybatsman2.loc[batsname, 'B'] + 1

					mybowlers2.loc[bowler, 'B'] = mybowlers2.loc[bowler, 'B'] + 1
					mybowlers2.loc[bowler, 'R'] = mybowlers2.loc[bowler, 'R'] + 1
					score2 = score2 + 1

				elif line2[i][2] == ' 2 runs' or line2[i][2] == ' 2 run' or line2[i][2] == ' 2':
					mybatsman2.loc[batsname, 'R'] = mybatsman2.loc[batsname, 'R'] + 2
					mybatsman2.loc[batsname, 'B'] = mybatsman2.loc[batsname, 'B'] + 1

					mybowlers2.loc[bowler, 'B'] = mybowlers2.loc[bowler, 'B'] + 1
					mybowlers2.loc[bowler, 'R'] = mybowlers2.loc[bowler, 'R'] + 2
					score2 = score2 + 2

				elif line2[i][2] == ' 3 runs' or line2[i][2] == ' 3 run' or line2[i][2] == ' 3':
					mybatsman2.loc[batsname, 'R'] = mybatsman2.loc[batsname, 'R'] + 3
					mybatsman2.loc[batsname, 'B'] = mybatsman2.loc[batsname, 'B'] + 1

					mybowlers2.loc[bowler, 'B'] = mybowlers2.loc[bowler, 'B'] + 1
					mybowlers2.loc[bowler, 'R'] = mybowlers2.loc[bowler, 'R'] + 3
					score2 = score2 + 3
				elif line2[i][2] == ' no run' or line2[i][2] == ' no':
					mybatsman2.loc[batsname, 'B'] = mybatsman2.loc[batsname, 'B'] + 1
					mybowlers2.loc[bowler, 'B'] = mybowlers2.loc[bowler, 'B'] + 1

				elif line2[i][2] == ' leg byes':

					if line2[i][3] == ' four' or line2[i][3] == ' FOUR' or line2[i][3] == ' 4 runs':
						leg_bye = leg_bye + 4
						score2 = score2 + 4
						mybowlers2.loc[bowler,
									'B'] = mybowlers2.loc[bowler, 'B'] + 1
					if line2[i][3] == ' 1 run' or line2[i][3] == ' 1':
						leg_bye = leg_bye + 1
						score2 = score2 + 1
						mybowlers2.loc[bowler,
									'B'] = mybowlers2.loc[bowler, 'B'] + 1
				elif line2[i][2] == ' byes':
					mybatsman2.loc[batsname, 'B'] = mybatsman2.loc[batsname, 'B'] + 1
					mybowlers2.loc[bowler, 'B'] = mybowlers2.loc[bowler, 'B'] + 1

					if line2[i][3] == ' 1 run' or line2[i][3] == ' 1':
						b2 = b2 + 1
						score2 = score2 + 1
				else:
					mybatsman2.loc[batsname, 'B'] = mybatsman2.loc[batsname, 'B'] + 1
					mybowlers2.loc[bowler, 'B'] = mybowlers2.loc[bowler, 'B'] + 1
					wickets2 = wickets2 + 1
					add = str(score2) + '-' + str(wickets2) + \
						'(' + batsname + ',' + ball_no + ')'
					fall2 = fall2+add
					fall2 = fall2+" "

					content3 = line2[i][2].split('!')

					if content3[0] == ' out bowled':
						mybatsman2.loc[batsname, 'status'] = 'bytes ' + bowler
						mybowlers2.loc[bowler,
									'W'] = mybowlers2.loc[bowler, 'W'] + 1
					elif content3[0] == ' out lbw':
						mybatsman2.loc[batsname, 'status'] = 'lbw ' + bowler
						mybowlers2.loc[bowler,
									'W'] = mybowlers2.loc[bowler, 'W'] + 1
					else:
						content4 = content3[0].split('by')
						mybatsman2.loc[batsname, 'status'] = 'c ' + \
							content4[1] + ' bytes ' + bowler
						mybowlers2.loc[bowler,
									'W'] = mybowlers2.loc[bowler, 'W'] + 1

				mybatsman2.loc[batsname, 'SR'] = int(
					(mybatsman2.loc[batsname, 'R'] / mybatsman2.loc[batsname, 'B']) * 100)
				mybowlers2.loc[bowler, 'O'] = (
					mybowlers2.loc[bowler, 'B']//6)+((mybowlers2.loc[bowler, 'B'] % 6)*0.1)

				mybowlers2.loc[bowler, 'EC'] = mybowlers2.loc[bowler,
																'R']/(mybowlers2.loc[bowler, 'B']/6)

			extra2 = leg_bye + b2 + wide2

			# mybatsman2.to_csv('Scorecard1.txt')
			

			with open('Scorecard.txt', 'a') as f:
				f.write('\n')
				f.write('India innings')
				f.write('\n')
				df = mybatsman2.to_string(header=True, index=True)
				f.write(df)
				f.write('\n')
				f.write('\nExtras\t\t' + str(extra2) + '(bytes ' + str(b2) + ', leg_bye ' +
						str(leg_bye) + ', w ' + str(wide2) + ', nb ' + str(noball2) + ')')
				f.write('\n')
				f.write('\nTotal\t\t' + str(score2) + ' (' + str(wickets2) +
						' wkts, ' + str(mybowlers2['O'].sum()) + ' Ov)\n')
				f.write('\n')
				f.write('Did not bat         Bhuvneshwar Kumar , Avesh Khan , Yuzvendra Chahal , Arshdeep Singh')
				f.write('\n')
				f.write('\n')
				f.write('fall of wickets')
				f.write('\n')
				f.write(fall2)
				f.write('\n')
				f.write('\n')
				f.write('bowler')
				f.write('\n')
				df1 = mybowlers2.to_string(header=True, index=True)
				f.write(df1)

		except FileNotFoundError:
			print("Error : Input File Not Found")
		except PermissionError:
			print("Error: Dont have the permission ,Close the output file and run code again")
		except ZeroDivisionError:
			print("Check if the strike rate/economy calculation")	

except:
    print("Error:Install Pandas library ")

scorecard()


# This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
