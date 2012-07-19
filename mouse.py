from selenium import webdriver
from time import sleep
from random import shuffle
from re import sub
from random import randrange

def loadMaze():
	browser = webdriver.Firefox()
	browser.get('file:///home/snail/Documents/code/mouse/rooms/room957.html')
	return browser

def chooseDoor(maze,knownRooms):
	def identifyDoors(door):
		doorURL = door.get_attribute('href')
		doorNumber = sub('^file.*rooms\/room|.html','',doorURL)
		if doorNumber not in knownRooms:
			unknownDoorList.append(door)
		else:
			knownDoorList.append(door)
	def chooseUnknown(unknownDoorList):
		print 'Chose unknown door.' #Debugging
		return unknownDoorList[0]
	def chooseKnown(knownDoorList):
		print 'Chose known door.' #Debugging
		shuffle(knownDoorList)
		return knownDoorList[0]
	def chooseMixed(knownDoorList,unknownDoorList):
		if randrange(1,4) != 2:
			return chooseUnknown(unknownDoorList)
		else:
			return chooseKnown(knownDoorList)
	doorList = []
	knownDoorList = []
	unknownDoorList = []
	
	doorList = maze.find_elements_by_xpath('//a')

	[identifyDoors(door) for door in doorList]

	if len(unknownDoorList) and len(knownDoorList) != 0:
		print 'Mixed doors.' #Debugging
		return chooseMixed(knownDoorList,unknownDoorList)
	else:
		if len(unknownDoorList) == 0:
			print 'Only known doors.' #Debugging
			return chooseKnown(knownDoorList)
		else:
			print 'Only unknown doors.' #Debugging
			return chooseUnknown(unknownDoorList)

def runMaze(maze):
	knownRooms = []
	exitFound = 0
	moveCounter = 0 #Debugging

	while exitFound == 0:
		roomNumber = maze.find_elements_by_id('roomNumber')
		while len(roomNumber) < 1:
			roomNumber = maze.find_elements_by_id('roomNumber')
		roomNumber = roomNumber[0].text.replace('Room ','')
		if roomNumber not in knownRooms:
			knownRooms.append(roomNumber)

		messages = maze.find_elements_by_id('message')
		
		if 'YOU WIN!' in messages:
			exitFound = 1
			print message
			print "You escape the maze!"
		else:
			moveCounter = moveCounter + 1 #Debugging
			print moveCounter #Debugging
			door = chooseDoor(maze,knownRooms)
			door.click()
	
	print knownRooms.sort() #Debugging
	maze.close()

maze = loadMaze()
runMaze(maze)
