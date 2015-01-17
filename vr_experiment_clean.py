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
import vizshape


scale = 14

viz.setMultiSample(4)
viz.go()
viz.MainWindow.fov(60)
#vizshape.addAxes()

# Setup keyboard/mouse tracker
tracker = vizcam.addWalkNavigate(forward='w', backward='s', left='a', right='d', moveScale=1.0, turnScale=1.0)
tracker.setPosition([0,1.8,10])
viz.link(tracker,viz.MainView)
viz.MainView.setPosition(2,2,0) 

#build scene
#load room and set scale
walls = viz.addChild('models/new/room_large.osgb')
walls.setScale(scale, scale, scale)
walls.disable(viz.PICKING)
#walls.setEuler( [ 90, 0, 0 ] )
#walls.setPosition([0,0,2.5])
roof = viz.addChild('models/new/roof_large.osgb')
roof.setScale(scale, scale, scale)
roof.disable(viz.PICKING)

#load the diving wall and door, hide them
divider = viz.addChild('models/new/divider_large_2.osgb')
divider.setScale(22, 22, 22)
divider.setPosition([0,0,20])
divider.disable(viz.PICKING)
door = viz.addChild('models/new/door_large.osgb')
door.setCenter([-0.05, 0, 0])
door.setScale(scale, scale, scale)
door.setPosition([0,0,20])
door.disable(viz.PICKING)

#Make Shapes
#make shapes
box1 = vizshape.addBox(size = [0.2,0.2,0.2], color = viz.BLUE)
box1.setPosition([-1,1.35,12])
box1.name = 'BOX_BLUE'
ball1 = vizshape.addSphere(radius=0.1,slices=10,stacks=10, color = viz.YELLOW)
ball1.setPosition([-0.7,1.35,12])
ball1.name = 'SPHERE_YELLOW'
tube1 = vizshape.addCylinder(height=0.2,radius=0.1,topRadius=None,bottomRadius=None,slices=10,bottom=True,top=True, color = viz.GREEN)
tube1.setPosition([-0.4,1.35,12])
tube1.name = 'CYLINDER_GREEN'
tri1 = vizshape.addPyramid(base=(0.2,0.2),height=0.2, color = viz.PURPLE)
tri1.setPosition([-0.1,1.25,12])
tri1.name = 'TRIANGLE_PURPLE'
box2 = vizshape.addBox(size = [0.2,0.2,0.2], color = viz.RED)
box2.setPosition([0.2,1.35,12])
box2.name = 'BOX_RED'
ball2 = vizshape.addSphere(radius=0.1,slices=10,stacks=10, color = viz.GREEN)
ball2.setPosition([0.6,1.35,12])
ball2.name = 'BALL_GREEN'
tube2 = vizshape.addCylinder(height=0.2,radius=0.1,topRadius=None,bottomRadius=None,slices=10,bottom=True,top=True, color = viz.BLUE)
tube2.setPosition([0.9,1.35,12])
tube2.name = 'CYCLINDER_BLUE'
tri2 = vizshape.addPyramid(base=(0.2,0.2),height=0.2, color = viz.YELLOW)
tri2.setPosition([1.2,1.25,12])
tri2.name = 'TRIANGLE_YELLOW'
box3 = vizshape.addBox(size = [0.2,0.2,0.2], color = viz.GREEN)
box3.setPosition([-1,1.35,-12])
box3.name = 'BOX_GREEN'
ball3 = vizshape.addSphere(radius=0.1,slices=10,stacks=10, color = viz.BLUE)
ball3.setPosition([-0.7,1.35,-12])
ball3.name = 'SPHERE_BLUE'
tube3 = vizshape.addCylinder(height=0.2,radius=0.1,topRadius=None,bottomRadius=None,slices=10,bottom=True,top=True, color = viz.RED)
tube3.setPosition([-0.4,1.35,-12])
tube3.name = 'CYLINDER_RED'
tri3 = vizshape.addPyramid(base=(0.2,0.2),height=0.2, color = viz.YELLOW)
tri3.setPosition([-0.1,1.25,-12])
tri3.name = 'TRIANGLE_YELLOW'
box4 = vizshape.addBox(size = [0.2,0.2,0.2], color = viz.PURPLE)
box4.setPosition([0.2,1.35,-12])
box4.name = 'BOX_PURPLE'
ball4 = vizshape.addSphere(radius=0.1,slices=10,stacks=10, color = viz.BLUE)
ball4.setPosition([0.6,1.35,-12])
ball4.name = 'SPHERE_BLUE'
tube4 = vizshape.addCylinder(height=0.2,radius=0.1,topRadius=None,bottomRadius=None,slices=10,bottom=True,top=True, color = viz.YELLOW)
tube4.setPosition([0.9,1.35,-12])
tube4.name = 'CYCLINDER_YELLOW'
tri4 = vizshape.addPyramid(base=(0.2,0.2),height=0.2, color = viz.GREEN)
tri4.setPosition([1.2,1.25,-12])
tri4.name = 'TRIANGLE_GREEN'

viz.collision(viz.ON)

memorisationStation = viz.addChild('plant.osgb',pos=[0, 0, 10],scale=[1, 1, 1])
memorisationStation.disable(viz.PICKING)
memorisationStation.disable(viz.RENDERING)
memorisationStationSensor = vizproximity.Sensor(vizproximity.Box([3,4,3],center=[0,1.5,1]),source=memorisationStation)

doorStation = viz.addChild('plant.osgb',pos=[0, 0, 0],scale=[1,1,1])
doorStation.disable(viz.PICKING)
doorStation.disable(viz.RENDERING)
doorStationSensor = vizproximity.Sensor(vizproximity.Box([3,4,3],center=[0,1.5,1]),source=doorStation)

testStation = viz.addChild('plant.osgb',pos=[0, 0, -12],scale=[1, 1, 1])
testStation.disable(viz.PICKING)
testStation.disable(viz.RENDERING)
testStationSensor = vizproximity.Sensor(vizproximity.Box([3,4,3],center=[0,1.5,1]),source=testStation)
target = vizproximity.Target(viz.MainView)

#Create proximity manager
manager = vizproximity.Manager()

#Add destination sensors to manager
manager.addSensor(memorisationStationSensor)
manager.addSensor(testStationSensor)
manager.addSensor(doorStationSensor)
#Add viewpoint target to manager
manager.addTarget(target)

#Toggle debug shapes with keypress
vizact.onkeydown('t',manager.setDebug,viz.TOGGLE)

#result class
class Result:
	def __init__(self, correctAnswers):
		self.correctAnswers = correctAnswers

	def __str__(self):
		return self.correctAnswers

#variables
startingInstructions = """
W = UP, , S = DOWN, D = RIGHT, A = LEFT. \nPress the spacebar to continue and follow the instructions given"""

taskA = []

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
			print taskA[0].size
			print taskA[0].colour
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
		door.setPosition([-1,0,0])

	participantInfo.remove()

	# Return participant data
	viztask.returnValue(data)

def selectPhase(participant):
	panel = vr_utils.displayOnCenterPanel("")
	#Add vizinfo panel to display instructions
	if (participant.group == 'a'):
		panel.setText("Select the blue triangle, this will put it in your backpack. \nThen move to the desk behind you. \nSwap the shape in your backpack with the yellow shpere by clicking with the mouse")
	else:
		panel.setText("Select the blue triangle, this will put it in your backpack. \nThen move to the desk in the room behind you. \nSwap the shape in your backpack with the yellow shpere by clicking with the mouse")	

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
		doorAngle = 0;
		door.addAction( vizact.spin(0,1,0,90) )
		door.collideNone()
		while (doorAngle < 90):
			#door.setEuler([doorAngle,0,0])
			doorAngle +=0.01

	#wait untl ther reach the test table
	yield vizproximity.waitEnter(testStationSensor)

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
	yield vizproximity.waitEnter(memorisationStationSensor)

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
	#collect participant information
	participant = yield participantInfo()
	panel = vr_utils.displayOnCenterPanel(startingInstructions)
	#Wait for spacebar to begin experiment
	yield viztask.waitKeyDown(' ')
	vr_utils.removeCenterPanel(panel)

	print "select phase"
	#start the memorisation phase
	yield selectPhase(participant)
	print "swap phase"
	#wait for participant to move to testing station
	yield swapPhase(participant)
	print "result phase"
	#begin the test phase, store the results, results saved
	result = yield testPhase(participant)
	print 'Experiment Complete.'

viztask.schedule(init)