from selenium import webdriver
from time import sleep
from random import shuffle
from re import sub

def loadMaze():
	browser = webdriver.Firefox()
	browser.get('file:///home/snail/Documents/code/mouse/rooms/room39.html')
	return browser

def chooseDoor(maze,knownRooms):
	doorList = []
	idealDoorList = []
	doorList = maze.find_elements_by_xpath('//a')
	for door in doorList:
		doorURL = door.get_attribute('href')
		doorNumber = sub('^file.*rooms\/room|.html','',doorURL)
		if doorNumber not in knownRooms:
			knownRooms.append(doorNumber)
			idealDoorList.append(door)
	if len(idealDoorList) >= 1:
		print 'Chose ideal door.'
		print idealDoorList[0].get_attribute('href')
		return idealDoorList[0]
	else:
		print 'Chose not ideal door.'
		return doorList[0]

def runMaze(maze):

	knownRooms = []

	exitFound = 0

	moveCounter = 0 #Debugging

	while exitFound == 0:
		roomNumber = maze.find_elements_by_id('roomNumber')
		while len(roomNumber) < 1:
			roomNumber = maze.find_elements_by_id('roomNumber')
		roomNumber = roomNumber[0].text
		roomNumber = roomNumber.replace('Room ','')
		if roomNumber not in knownRooms:
			knownRooms.append(roomNumber)

		messages = maze.find_elements_by_id('message')
		
		if len(messages) > 0:
			message = messages[0].text
		else:
			message = ''

		if message == 'YOU WIN!':
			exitFound = 1
			print message
			print "You escape the maze!"
		else:
			door = chooseDoor(maze,knownRooms)
			moveCounter = moveCounter + 1
			print moveCounter
			door.click()

	maze.close()

maze = loadMaze()
runMaze(maze)
