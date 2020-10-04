# -*- coding: utf-8 -*-
from random import randrange


def diceThrow(strForm):
	mem = []
	form = strForm
	if form[0] != "-" and form[0] != "+":
		form = "+"+form
	form = form.replace("+", "s+")
	form = form.replace("-","m-")	
	comp = len(form)	
	result = 0
	for i in range(0,len(form)):	
		if form[i] == "m" or form[i] == "s":
			neg = 1
			if form[i] == "m":
				neg = -1
			numDices = ""
			for j in range(i+2,len(form)):
				if form[j] !='m' and form[j] != 's' and form[j] !='-' and form[j] != '+':
					if form[j] == "d" or form[j] == "D":
						break		
					else:
						numDices= numDices+ form[j]
				else:
					break
			numDices = int(numDices)	
			numFaces = ""
			flag = False	
			for j in range(i+2,len(form)):
				if form[j] == "d" or form[j] == "D":
					flag = True
				if flag == True:	
					if form[j] =='m' or form[j] == 's' or form[j] =='-' or form[j] == '+':
						break
					else:	
						if form[j] != "d" and form[j] != "D":
							numFaces= numFaces+ form[j]
			mod = 0			
			if numFaces == "":
				mod = int(form[i+2:])
				numFaces = "0"
			mult = "1"
			if  numFaces.split("*")[0] != numFaces:
				numFacesTemp =numFaces.split("*")[0] 
				mult = numFaces.split("*")[1]
				numFaces = numFacesTemp
			mult = int(mult)
			numFaces = int(numFaces)
			for dices in range(0, numDices):
				if numFaces == 0:
					value = mod
					if mult !=1:
						idDice = "Mod(*"+str(mult)+")"
					else:
						idDice = "Mod"
					result= result + (neg*value*mult)
					mem.append((idDice,value))	
					break			
				else:
					value = randrange(numFaces)+1
					if mult !=1:
						idDice = str(dices+1) +".D"+str(numFaces)+"(*"+str(mult)+")"
					else:
						idDice = str(dices+1) +".D"+str(numFaces)
					result= result + (neg*value*mult)
					mem.append((idDice,value))
	return result,mem			
def printDice(dice):
	s=dice[0]+": "+str(dice[1])
	return s
def printMem(mem):
	res = ""
	for i in range(0,len(mem)):
		if i != len(mem)-1:
			res =res+printDice(mem[i])+", "	
		else:
			res= res+ printDice(mem[i])
	return res



