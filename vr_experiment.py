'''

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
import vizfx.postprocess
import vizinfo
import vr_utils

scale = 14

viz.setMultiSample(4)
viz.go()
viz.MainWindow.fov(60)
#vizshape.addAxes()

# Setup keyboard/mouse tracker
tracker = vizcam.addWalkNavigate(forward='w', backward='s', left='a', right='d', moveScale=1.0, turnScale=1.0)
tracker.setPosition([0,1.8,10])
viz.link(tracker,viz.MainView)

#build scene
#load room and set scale
walls = viz.addChild('models/new/room_large.osgb')
walls.setScale(scale, scale, scale)
#walls.setEuler( [ 90, 0, 0 ] )
#walls.setPosition([0,0,2.5])
roof = viz.addChild('models/new/roof_large.osgb')
roof.setScale(scale, scale, scale)

#load the diving wall and door, hide them
divider = viz.addChild('models/new/divider_large_2.osgb')
divider.setScale(scale, scale, scale)
divider.setPosition([0,0,20])
door = viz.addChild('models/new/door_large.osgb')
door.setCenter([-0.05, 0, 0])
door.setScale(scale, scale, scale)
door.setPosition([0,0,20])

viz.collision(viz.ON)

memorisationStation = viz.addChild('plant.osgb',pos=[0, 0, 10],scale=[1, 1, 1])
memorisationStation.disable(viz.RENDERING)

doorStation = viz.addChild('plant.osgb',pos=[0, 0, 0],scale=[1, 1, 1]);
doorStation.disable(viz.RENDERING)
doorStationSensor = vizproximity.Sensor(vizproximity.Box([3,4,3],center=[0,1.5,1]),source=doorStation)

testStation = viz.addChild('plant.osgb',pos=[0, 0, -12],scale=[1, 1, 1])
testStation.disable(viz.RENDERING)
testStationSensor = vizproximity.Sensor(vizproximity.Box([3,4,3],center=[0,1.5,1]),source=testStation)
target = vizproximity.Target(viz.MainView)

#Create proximity manager
manager = vizproximity.Manager()

#Add destination sensors to manager
manager.addSensor(testStationSensor)
manager.addSensor(doorStationSensor)
#Add viewpoint target to manager
manager.addTarget(target)

#Toggle debug shapes with keypress
vizact.onkeydown('t',manager.setDebug,viz.TOGGLE)

def openDoor():
	door.addAction( vizact.spin(0,1,0,90) )

vizact.onkeydown('i',openDoor)



#question class
class Question:

	#class variables, shared between all Question objects
	questionCount = 0
	totalTime = 0

	#constructor initialises instance variables
	def __init__(self, statement, possibleAnswers, correctAnswerIndex, timeGiven):
		self.statement = statement
		self. possibleAnswers = possibleAnswers
		self.correctAnswerIndex = correctAnswerIndex
		self.timeGiven = timeGiven
		Question.questionCount += 1
		Question.totalTime += timeGiven

#result class
class Result:
	def __init__(self, correctAnswers):
		self.correctAnswers = correctAnswers

	def __str__(self):
		return self.correctAnswers

#variables
startingInstructions = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Aenean euismod gravida justo, a congue dolor tincidunt quis. 
Aliquam erat volutpat. Nullam egestas dignissim nunc non congue.
Press Space to begin."""

tasks = [] #used to store the question objects

def generateQuestions():
	#statement, possibleAnswers[], correctAnswerIndex, timeGiven
	tasks.append(Question("The door is red", ["The door is blue", "The door is yellow", "The door is red", "The door is green"], 2, 1))
	tasks.append(Question("The cat is behind the door", ["The cat is beside the door", "The cat is behind the door", "The cat is behind the dog", "The cat is red"], 1, 1))
	tasks.append(Question("The dog is in front of the cat", ["The dog is in front of the cat", "The dog is in front of the window", "The dog is in beside of the cat", "The dog is behind the cat"], 0, 1))
	tasks.append(Question("The window is over the door", ["The window is behind the door", "The window is in the door", "The window is beside the door", "The window is over the door"], 3, 1))
	return

def participantInfo():
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
	droplist_age = participantInfo.addLabelItem('Age Group',viz.addDropList())
	ageList = ['10-20','21-30','31-40','41-50','51-60','61-70', '71+']
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
		divider.setPosition([0,0,0])
		door.setPosition([-0.65,0,0])

	participantInfo.remove()

	# Return participant data
	viztask.returnValue(data)

def countDown(countDownLength, info):
	while countDownLength >= 0:
		yield viztask.waitTime(1)
		info.setText("You have " + str(Question.totalTime) + " seconds to memorise the following " + str(Question.questionCount) + " scenes. \n Starting in: " + str(countDownLength))
		countDownLength = countDownLength - 1
	return

def learnPhase(participant):
	#Add vizinfo panel to display instructions
	info = vizinfo.InfoPanel("You have " + str(Question.totalTime) + " seconds to memorise the following " + str(Question.questionCount) + " scenes.")
	info.visible(viz.ON)

	#count the user in
	yield countDown(5, info)

	#question loop
	currentQuestion = 0
	while currentQuestion < len(tasks):
		question= tasks[currentQuestion]

		#display question
		print question.statement
		info.setText("Scene: " + str(currentQuestion + 1))

		#wait for time determined by the question
		yield viztask.waitTime(question.timeGiven)
		currentQuestion += 1 #move on to next question
	info.visible(viz.OFF)

def movePhase(participant):
	info = vizinfo.InfoPanel("")
	info.visible(viz.ON)
	#message dependant on group A or B
	if (participant.group == 'a'):
		info.setText("Memorisation phase complete. \nPlease move to the station behind you, at the other end of the room, to continue.")
	else: 
		info.setText("Memorisation phase complete. \nPlease move to the station behind you, through the door, to continue.")
		##open the door
		divider.collideNone()
		yield vizproximity.waitEnter(doorStationSensor)
		doorAngle = 0;
		door.addAction( vizact.spin(0,1,0,90) )
		door.collideNone()
		while (doorAngle < 90):
			#door.setEuler([doorAngle,0,0])
			doorAngle +=0.01

	info.visible(viz.ON)

	#wait untl ther reach the test table
	yield vizproximity.waitEnter(testStationSensor)

	info.setText("Testing phase started.")
	yield viztask.waitTime(3)
	info.visible(viz.OFF)

def testPhase(participant):
	
	result = Result("1")
	#save the results to a document
	saveResults(participant, result)
	return

#save results into document (userName_currentDateTime.txt)
def saveResults(participant, result):
	print 'Saving results...'
	#Write the data to our file.
	question_data = open('results.txt','a')
	data = "\n############################"
	data += "\nfirst name: " + participant.firstName
	data += "\nlast name: " + participant.lastName
	data += "\ngroup: " + participant.group
	data += "\nage group: " + participant.ageGroup

	data += "\nresults: " + str(result) +"\t"
	question_data.write(data)
	#Flush the internal buffer.
	question_data.flush()
	return

def init():
	generateQuestions()
	#collect participant information
	participant = yield participantInfo()
	panel = vr_utils.displayOnCenterPanel(startingInstructions)
	#Wait for spacebar to begin experiment
	yield viztask.waitKeyDown(' ')
	vr_utils.removeCenterPanel(panel)

	print "learning phase"
	#start the memorisation phase
	yield learnPhase(participant)
	print "move phase"
	#wait for participant to move to testing station
	yield movePhase(participant)
	print "result phase"
	#begin the test phase, store the results, results saved
	result = yield testPhase(participant)
	print 'Experiment Complete.'

viztask.schedule(init)