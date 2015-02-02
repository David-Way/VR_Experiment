'''
Created by David Way & Emer Mooney
This experiment is used to investigate the effect that crossing a physical boundary can have on memory recall. 
In research previously undertaken utilising virtual environments a decline in memory has been noted while moving between new locations. 
Group A does not walk through boundary/door
Group B walks through boundary/door
'''

import viz
import vizshape
import vizact
import random
import vizinput
import vizcam
import viztask
import vizproximity
import viztracker
import vizfx.postprocess
import vizinfo
import vizshape
import vr_utils

#Variables
scale = 14
walls = roof = divider = door = None
bag1 = bag2 = None
stationOne = stationTwo = stationOneSensor = stationTwoSensor = doorStation = doorStationSensor = None
viewTracker = mouseTracker = None
taskA = []
firstPickObject = secondPickObject = None
#Strings
startingInstructions = """Controls: W = Forward, S = Back, D = Right, A = Left. \nPress the spacebar to continue and follow the instructions given"""
selectPhaseInstructionsGroupA = """Select the Red Cube, this will put it in the bag. \nThen move to the desk behind you. \nSwap the shape in your bag with the blue sphere by clicking with the mouse"""
selectPhaseInstructionsGroupB = """Select the Red Cube, this will put it in the bag. \nThen move to the desk in the room behind you. \nSwap the shape in your bag with the blue sphere by clicking with the mouse"""

#Set up vizard
vr_utils.init(viz, viztracker)

# Setup keyboard/mouse tracker
viewTracker = vr_utils.enableNavigation(viewTracker, mouseTracker, viz, viztracker)
bag1 = vr_utils.makeBag(viewTracker, 1)
bag2 = vr_utils.makeBag(viewTracker, 2)

#Build the scene
vr_utils.buildScene(walls, roof, scale)

#Add the shapes to the scene
vr_utils.makeShapes(viz, vizshape)

def exitStationOne(e):
	global bag1
	#print bag1.getDst().name #returns the bag from the link (bag1)
	bag1.postTrans([0,-0.5,0])

def exitStationTwo(e):
	global bag2
	bag2.postTrans([0,-0.5,0])

def enterStationOne(e):
	global bag1
	bag1.postTrans([0,0.5,0])

def enterStationTwo(e):
	global bag2
	bag2.postTrans([0,0.5,0])

def addSensors():
	global stationOne, stationTwo, stationOneSensor, stationTwoSensor, doorStation, doorStationSensor
	stationOne = viz.addChild('plant.osgb',pos=[0, 0, 10],scale=[1, 1, 1])
	stationOne.disable(viz.PICKING)
	stationOne.disable(viz.RENDERING)
	stationOneSensor = vizproximity.Sensor(vizproximity.Box([3,4,3],center=[0,1.5,1]),source=stationOne)

	doorStation = viz.addChild('plant.osgb',pos=[0, 0, 0],scale=[1,1,1])
	doorStation.disable(viz.PICKING)
	doorStation.disable(viz.RENDERING)
	#doorStationSensor = vizproximity.Sensor(vizproximity.Box([3,4,3],center=[0,1.5,1]),source=doorStation)
	doorStationSensor = vizproximity.Sensor(vizproximity.Box([2.5,2.5,3.5]),source=viz.Matrix.translate(0,1.75,0))

	stationTwo = viz.addChild('plant.osgb',pos=[0, 0, -12],scale=[1, 1, 1])
	stationTwo.disable(viz.PICKING)
	stationTwo.disable(viz.RENDERING)
	stationTwoSensor = vizproximity.Sensor(vizproximity.Box([3,4,3],center=[0,1.5,1]),source=stationTwo)
	target = vizproximity.Target(viz.MainView)

	#Create proximity manager
	manager = vizproximity.Manager()

	#Add destination sensors to manager
	manager.addSensor(stationOneSensor)
	manager.addSensor(stationTwoSensor)
	manager.addSensor(doorStationSensor)

	manager.onExit(stationOneSensor, exitStationOne)
	manager.onExit(stationTwoSensor, exitStationTwo)
	manager.onEnter(stationOneSensor, enterStationOne)
	manager.onEnter(stationTwoSensor, enterStationTwo)
	
	#Add viewpoint target to manager
	manager.addTarget(target)

	#Toggle debug shapes with keypress
	vizact.onkeydown('t',manager.setDebug,viz.TOGGLE)

#Create proximty sensors/hit boxes
##addSensors(stationOne, stationTwo, stationOneSensor, stationTwoSensor, doorStation, doorStationSensor)
addSensors()
#Result class
class Result:
	def __init__(self, correctAnswers):
		self.correctAnswers = correctAnswers

	def __str__(self):
		return self.correctAnswers

def getParticipantInfo():
	global divider, door, scale
	#Add an InfoPanel with a title bar
	participantInfo = vizinfo.InfoPanel('',title='Participant Information', align=viz.ALIGN_CENTER, icon=False)

	#Add name and ID fields
	textbox_first = participantInfo.addLabelItem('First Name',viz.addTextbox())
	textbox_last = participantInfo.addLabelItem('Last Name',viz.addTextbox())
	textbox_group = participantInfo.addLabelItem('Group (A/B)',viz.addTextbox())
	participantInfo.addSeparator(padding=(20,20))

	#Add gender and age fields
	radiobutton_male = participantInfo.addLabelItem('Male',viz.addRadioButton(0))
	radiobutton_female = participantInfo.addLabelItem('Female',viz.addRadioButton(0))
	droplist_age = participantInfo.addLabelItem('Age',viz.addDropList())
	ageList = ['18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33', '34', '35', '36', '37', '38', '39', '40+']
	droplist_age.addItems(ageList)
	participantInfo.addSeparator(padding=(20,20))

	#Add submit button aligned to the right and wait until it's pressed
	submitButton = participantInfo.addItem(viz.addButtonLabel('Submit'),align=viz.ALIGN_RIGHT_CENTER)
	yield viztask.waitButtonUp(submitButton)

	#Collect participant data
	data = viz.Data()
	data.lastName = textbox_last.get()
	data.firstName = textbox_first.get()
	data.group = textbox_group.get().lower()
	data.ageGroup = ageList[droplist_age.getSelection()]

	if radiobutton_male.get() == viz.DOWN:
		data.gender = 'male'
	else:
		data.gender = 'female'

	#if the person is a menber of the group B
	if (data.group == 'b'):
		#load the diving wall and door, hide them
		divider = viz.addChild('models/new/divider_large_2.osgb')
		divider.setScale(scale, scale, scale)
		divider.setPosition([0,0,20])
		divider.disable(viz.PICKING)
		door = viz.addChild('models/new/door_large.osgb')
		door.setCenter([-0.05, 0, 0])
		door.setScale(scale, scale, scale)
		door.setPosition([0,0,20])
		door.disable(viz.PICKING)
		divider.setPosition([0,0,0])
		door.setPosition([-0.6,0,0])
	participantInfo.remove()
	# Return participant data
	viztask.returnValue(data)

def pickObject(): 
	global firstPickObject
	while True:
		yield viztask.waitMouseDown(viz.MOUSEBUTTON_LEFT)
		#Check if the mouse is over one of the shapes 
		item = viz.MainWindow.pick( info = True )
		#If there is an intersection 
		if item.valid: 
			#Add mouse over action
			bag1Position = bag1.getDst().getPosition()
			aboveBag1 = [bag1Position[0], bag1Position[1]+0.6, bag1Position[2]]
			inThaBag1up = vizact.moveTo(aboveBag1,speed=5)
			inThaBag1down = vizact.moveTo(bag1.getDst().getPosition(),speed=5)
			item.object.addAction(inThaBag1up)
			item.object.addAction(inThaBag1down)
			firstPickObject = item.object
			
			yield viztask.waitTime(1.6) 
			firstPickObject.visible((viz.OFF))
			
			#Print the point where the line intersects the object.
			taskA.append(item.object)
			viz.callback(viz.MOUSEDOWN_EVENT, 0)
			print taskA[0].name
			#print taskA[0].getPosition()
			#print taskA[0].size
			#print taskA[0].colour
			print "picked"
			return

def swapObject():
	global firstPickObject, bag2 , secondPickOject
	while True:
		yield viztask.waitMouseDown(viz.MOUSEBUTTON_LEFT)
		#Check if the mouse is over one of the shapes 
		item = viz.MainWindow.pick( info = True )
		#If there is an intersection 
		if item.valid: 
			#Add mouse over action
			bag2Position = bag2.getDst().getPosition()
			firstPickObject.visible(viz.ON)
			firstPickObject.setPosition(bag2Position)
			aboveBag2 = [bag2Position[0], bag2Position[1]+0.6, bag2Position[2]]
			
			outtaThaBag2up = vizact.moveTo(aboveBag2,speed=5)
			outtaThaBag2down = vizact.moveTo(item.object.getPosition(),speed=5)
			firstPickObject.addAction(outtaThaBag2up)
			firstPickObject.addAction(outtaThaBag2down)

			inThaBag2up = vizact.moveTo(aboveBag2,speed=5)
			inThaBag2down = vizact.moveTo(bag2.getDst().getPosition(),speed=5)
			item.object.addAction(inThaBag2up)
			item.object.addAction(inThaBag2down)
			secondPickOject = item.object
			
			yield viztask.waitTime(1.6) 
			firstPickObject.visible(viz.ON)
			secondPickOject.visible((viz.OFF))

			#Print the point where the line intersects the object.

			taskA.append(item.object)
			viz.callback(viz.MOUSEDOWN_EVENT, 0)
			print taskA[0].name
			print "swapped"
			return

def selectPhase(participant):
	global divider, door, bag1, bag2, vizact
	panel = vr_utils.displayOnCenterPanel("")
	panel.fontSize(24)
	#Add vizinfo panel to display instructions
	if (participant.group == 'a'):
		panel.setText(selectPhaseInstructionsGroupA)
	else:
		panel.setText(selectPhaseInstructionsGroupB)

	panel.visible(viz.ON)
	#count the user in
	yield viztask.waitTime(2)

	panel.visible(viz.OFF)

	yield pickObject()
	print "Done with waiting for mouse"

	if (participant.group == 'b'):
		##open the door
		#divider.collideNone()
		yield vizproximity.waitEnter(doorStationSensor)
		
		spinToYaw90 = vizact.spinTo(euler=[90,0,0], speed=50)
		door.addAction( spinToYaw90 )
		
		#lowerBag = vizact.move(0,-1,0,3)
		#bag1.addAction(lowerBag)
		#bag1.postTrans([0,-0.5,0])
		
		doorAngle = 0;
		door.disable(viz.INTERSECTION)
		#door.collideNone()
		##door.addAction( vizact.spin(0,1,0,90) )
		#while (doorAngle < 90):
			#door.setEuler([doorAngle,0,0])
			#doorAngle +=0.01
	#else :
		#yield vizproximity.waitEnter(doorStationSensor)
		#bag1.postTrans([0,-0.5,0])

	#wait until they reach the test table
	yield vizproximity.waitEnter(stationTwoSensor)
	print "at station 2"
	return



def swapPhase(participant):

	print "waiting to click item"
	#loopin
	#yield swapClick()

	#wait until the user selects a shape
	yield swapObject()
	print "Done with waiting for mouse"
	panel.fontSize(70)
	if (participant.group == 'a'):
		panel = vr_utils.displayOnCenterPanel("Great! Now just move back to the original desk")
	else:
		panel = vr_utils.displayOnCenterPanel("Great! Now just move back to the original desk in the other room")
			
	panel.visible(viz.ON)
	yield viztask.waitTime(2)
	panel.visible(viz.OFF)

	if (participant.group == 'b'):
		##open the door
		#divider.collideNone()
		yield vizproximity.waitEnter(doorStationSensor)
		doorAngle = 0;
		door.addAction( vizact.spin(0,1,0,90) )
		#door.collideNone()
		while (doorAngle < 90):
			#door.setEuler([doorAngle,0,0])
			doorAngle +=0.01

	#wait untl ther reach the test table
	yield vizproximity.waitEnter(stationOneSensor)
	return

def testPhase(participant):
	panel = vr_utils.displayOnCenterPanel("")
	panel.setText("Click on the shape you currently have in your backpack.")
	panel.visible(viz.ON)
	#count the user in
	yield viztask.waitTime(2)
	panel.visible(viz.OFF)
	yield pickObject()
	print "Done with waiting for mouse"
	result = Result("1")
	#save the results to a document
	viztask.returnValue(result)

def runExperiment():
	global divider, door, scale
	#tool.setUpdateFunction(updateGrabber)
	#Collect and store participant information
	participant = yield getParticipantInfo()
	panel = vr_utils.displayOnCenterPanel(startingInstructions)
	print "divider>"
	print divider
	#Wait for spacebar to begin experiment
	yield viztask.waitKeyDown(' ')
	vr_utils.removeCenterPanel(panel)

	print "select phase"
	#Start the select phase/phase one
	yield selectPhase(participant)
	print "swap phase"
	#wait for participant to move to testing station
	yield swapPhase(participant)
	print "result phase"
	#begin the test phase, store the results, results saved
	result = yield testPhase(participant)
	vr_utils.saveResults(participant, result)
	print 'Experiment Complete.'

viztask.schedule(runExperiment)