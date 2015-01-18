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
stationOne = stationTwo = stationOneSensor = stationTwoSensor = doorStation = doorStationSensor = None
tracker = None
taskA = []

#Strings
startingInstructions = """Controls: W = Forward, S = Back, D = Right, A = Left. \nPress the spacebar to continue and follow the instructions given"""
selectPhaseInstructionsGroupA = """Select the blue triangle, this will put it in your backpack. \nThen move to the desk behind you. \nSwap the shape in your backpack with the yellow sphere by clicking with the mouse"""
selectPhaseInstructionsGroupB = """Select the blue triangle, this will put it in your backpack. \nThen move to the desk in the room behind you. \nSwap the shape in your backpack with the yellow sphere by clicking with the mouse"""

#Set up vizard
vr_utils.init(viz, viztracker)

# Setup keyboard/mouse tracker
vr_utils.enableNavigation(tracker, viz)

#Build the scene
vr_utils.buildScene(walls, roof, scale)

#Add the shapes to the scene
vr_utils.makeShapes(viz, vizshape)

#Create proximty sensors/hit boxes
vr_utils.addSensors(stationOne, stationTwo, stationOneSensor, stationTwoSensor, doorStation, doorStationSensor)

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
		door.setPosition([-1,0,0])

	participantInfo.remove()

	# Return participant data
	viztask.returnValue(data)


def pickObject(): 
	while True:
		yield viztask.waitMouseDown(viz.MOUSEBUTTON_LEFT)
		#Check if the mouse is over one of the shapes 
		item = viz.MainWindow.pick( info = True )
		#If there is an intersection 
		if item.valid: 
			#Add mouse over action
			item.object.remove()
			#Print the point where the line intersects the object.
			taskA.append(item.object)
			viz.callback(viz.MOUSEDOWN_EVENT, 0)
			print taskA[0].name
			print taskA[0].getPosition()
			#print taskA[0].size
			#print taskA[0].colour
			print "picked"
			return

def swapObject(): 
	while True:
		yield viztask.waitMouseDown(viz.MOUSEBUTTON_LEFT)
		#Check if the mouse is over one of the shapes 
		item = viz.MainWindow.pick( info = True )
		#If there is an intersection 
		if item.valid: 
			#Add mouse over action
			item.object.remove()
			#Print the point where the line intersects the object.
			taskA.append(item.object)
			viz.callback(viz.MOUSEDOWN_EVENT, 0)
			print taskA
			print "swapped"
			return

def selectPhase(participant):
	global divider
	global door
	panel = vr_utils.displayOnCenterPanel("")
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
		divider.collideNone()
		yield vizproximity.waitEnter(doorStationSensor)
		
		spinToYaw90 = vizact.spinTo(euler=[90,0,0], speed=50)
		door.addAction( spinToYaw90 )
		
		doorAngle = 0;
		door.disable(viz.INTERSECTION)
		#door.collideNone()
		##door.addAction( vizact.spin(0,1,0,90) )
		#while (doorAngle < 90):
			#door.setEuler([doorAngle,0,0])
			#doorAngle +=0.01

	#wait untl ther reach the test table
	yield vizproximity.waitEnter(stationTwo)
	return

def swapPhase(participant):
	#wait until the user selects a shape
	yield swapObject()
	print "Done with waiting for mouse"

	if (participant.group == 'a'):
		panel = vr_utils.displayOnCenterPanel("Great!. Now just move back to the original desk")
	else:
		panel = vr_utils.displayOnCenterPanel("Great!. Now just move back to the original desk in the other room")
			
	panel.visible(viz.ON)
	yield viztask.waitTime(2)
	panel.visible(viz.OFF)

	if (participant.group == 'b'):
		##open the door
		divider.collideNone()
		yield vizproximity.waitEnter(doorStationSensor)
		doorAngle = 0;
		door.addAction( vizact.spin(0,1,0,90) )
		door.collideNone()
		while (doorAngle < 90):
			#door.setEuler([doorAngle,0,0])
			doorAngle +=0.01

	#wait untl ther reach the test table
	yield vizproximity.waitEnter(stationOne)

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